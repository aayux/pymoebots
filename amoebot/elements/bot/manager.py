import time
import logging
import numpy as np
import multiprocessing

from pathlib import Path
from multiprocessing import managers
from numpy import array, ndarray, uint8

from .agent import Agent
from ..manager import Manager
from ..tracker import StateTracker

class AmoebotManager(Manager):
    r""" 
    Manages sequential and/or asynchronous task assignment to agents of 
    individual amoebots.
    """

    def __init__(self, config_num:str):
        # holds all `Amoebot` objects created anonymously
        self.amoebots: list = list()

        # object of class `StateTracker`
        self.tracker: object = StateTracker(config_num)

        # configuration identifier for logging
        self.config_num = config_num

    def exec_async(self, n_cores:int, max_iter:int, buffer_len:int=None):
        r"""
        """
        # cast list to numpy array type
        self.amoebots = array(self.amoebots)
        

        # initialise DEBUG level logging
        logger = self._init_logging(to_console=True)

        # create a process safe queue
        mp_manager = multiprocessing.Manager()
        ip_buffr = mp_manager.Queue()
        op_buffr = mp_manager.Queue()

        # create a lock for the shared region
        lock = mp_manager.Lock()

        # System V like shared memory block
        shared = multiprocessing.shared_memory.SharedMemory(
                                        create=True, size=self.amoebots.nbytes
                                    )
        id_shared = shared.name

        # shared numpy array of amoebot objects
        sh_amoebots = np.ndarray(self.amoebots.shape, 
                                dtype=self.amoebots.dtype, 
                                buffer=shared.buf)
        sh_amoebots[:] = self.amoebots[:]

        _exec_async(self.tracker, ip_buffr, op_buffr, logger, sh_amoebots,
                    id_shared, n_cores, max_iter, buffer_len, lock)

        shared.close()
        shared.unlink()

    def exec_sequential(self, max_iter:int) -> dict:
        r"""
        """
        for _ in range(max_iter):
            for __id, _ in enumerate(self.amoebots):
                self.amoebots[__id] = _exec_step(amoebot=self.amoebots[__id])

    def _add_bot(self, __id:int, node:object):
        r""" adds individual particles to the (partially anonymous) `AnonList`
        """
        agent_of_amoebot = Agent(__id, head=node)
        self.amoebots.insert(__id, agent_of_amoebot)

    def _init_logging(
                        self, 
                        store:str='./.dumps/logs', 
                        to_console:bool=False
                    ) -> logging.RootLogger:
        r""" set up logging at DEBUG level by default
        """

        # create hidden space for logs
        Path(store).mkdir(parents=True, exist_ok=True)

        # set up logging to file
        logging.basicConfig(
                        level=logging.DEBUG, 
                        format='[%(levelname)s] %(asctime)s :: %(message)s', 
                        datefmt='%m-%d %H:%M:%S', 
                        filename=f'{store}/run-{self.config_num}.log', 
                        filemode='w'
                    )

        logger = logging.getLogger()

        if to_console:
            # create a console handler
            console_logger = logging.StreamHandler()

            # log at the higher ERROR level
            console_logger.setLevel(logging.ERROR)

            # add the handlers to the logger
            logger.addHandler(console_logger)

        return logger


def _exec_async(
                tracker:StateTracker, 
                ip_buffr:multiprocessing.managers.AutoProxy, 
                op_buffr:multiprocessing.managers.AutoProxy, 
                logger:logging.RootLogger, 
                sh_amoebots:array, 
                id_shared:str, 
                n_cores:int, 
                max_iter:int, 
                buffer_len:int, 
                lock:multiprocessing.managers.AcquirerProxy=None
            ):
    r"""
    Set up asynchronous calls for bot execution and create a queueing 
    manager for writing the state configuration file.

    returns (dict) : execution status
    """

    with multiprocessing.Pool(processes=n_cores) as pool:
        # listener process that handles queued writes
        _ = pool.apply_async(_queueing_manager, (
                                                    op_buffr, 
                                                    logger, 
                                                    tracker, 
                                                ))

        # generate an initial list of jobs to be completed
        jobs_init = [[__id] for __id, _ in enumerate(sh_amoebots)]
        for job in jobs_init: ip_buffr.put(job)

        results = list()

        # execute jobs on agents for fixed number of activations
        while True:
            results.append(pool.apply_async(_exec_step, (
                                                        ip_buffr, 
                                                        op_buffr, 
                                                        logger, 
                                                        sh_amoebots, 
                                                        id_shared, 
                                                        lock
                                                    )))

            # break if maximum iterations have been reached
            if len(results) >= max_iter: break

            # TODO flush the queue if buffer_len reached

        # collect all results from the pool
        for result in results: result.get()

        # exit using the listener process
        op_buffr.put(['ps-kill', 0])

        # log exit status
        cpname = multiprocessing.current_process().name
        log_message = f'{cpname} :: All connections closed. Exiting.'
        logging.info(log_message)


def _exec_step(
                ip_buffr:multiprocessing.managers.AutoProxy=None, 
                op_buffr:multiprocessing.managers.AutoProxy=None, 
                logger:logging.RootLogger=None, 
                sh_amoebots:array=None, 
                id_shared:str=None, 
                lock:multiprocessing.managers.AcquirerProxy=None, 
                amoebot:Agent=None
            ):
    r""" execute one step of `elements.bots.core.Amoebot.execute()`
    """

    # asynchronous execution mode
    if ip_buffr is not None:
        __id = ip_buffr.get()[0]

        # attach to the existing shared memory block
        sh_attached = multiprocessing.shared_memory.SharedMemory(name=id_shared)

        _sh_amoebots = np.ndarray(sh_amoebots.shape, 
                                dtype=sh_amoebots.dtype, 
                                buffer=sh_attached.buf)

        # execute the amoebot algorithm(s) and update activation status
        _sh_amoebots__id, actv_status = _sh_amoebots[__id].execute(logger=logger)

        # lock the shared address space for safe write
        lock.acquire(blocking=True)

        try: _sh_amoebots[__id] = _sh_amoebots__id
        finally: lock.release()

        state = (
            _sh_amoebots[__id].head, 
            _sh_amoebots[__id].tail, 
            _sh_amoebots[__id].clock
        )

        # push to output queue if there was an activation for this amoebot
        if actv_status: op_buffr.put([state, __id])

        # get the current process name for logging
        cpname = multiprocessing.current_process().name

        # generate a log message
        log_message = (
                        f'post/{cpname} :: < agent {__id} {_sh_amoebots[__id]} '
                        f'clock {state[2]} active {actv_status}>\n'
                        f'\thead {state[0]} at {state[0].position}\n'
                        f'\ttail {state[1]} at {state[1].position}.'
                    )

        # log the state information
        logging.info(log_message)

        # give other amoebots a chance to catch up
        time.sleep(.2)

        # push the bot id and status information to the queues
        ip_buffr.put([__id])

        # close access to the shared memory from this instance
        sh_attached.close()

        return (__id, actv_status)

    # sequential execution mode
    else:
        # execute the amoebot algorithm(s) and update activation status
        amoebot, _ = amoebot.execute()
        return amoebot

def _queueing_manager(
                        op_buffr:multiprocessing.managers.AutoProxy, 
                        logger:logging.RootLogger, 
                        tracker:StateTracker
                    ):
    while True:
        # pop the leading entry in the queue
        response = op_buffr.get()

        # reset or exit the listener process
        if response[0] == 'ps-kill': break

        # colelct information from output buffer
        state, __id = response

        # log the state information
        cpname = multiprocessing.current_process().name
        log_message = (
                        f'track/{cpname} :: < agent {__id} clock {state[2]} >\n'
                        f'\thead {state[0]} at {state[0].position}\n'
                        f'\ttail {state[1]} at {state[1].position}.'
                    )
        logging.info(log_message)

        # call `StateTracker.update` to update the configuration
        tracker.update(__id, state)