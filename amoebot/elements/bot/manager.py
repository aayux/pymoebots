import os
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
from ...utils.shared_objects import SharedObjects

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

        # initialise DEBUG level logging
        logger = self._init_logging(to_console=True)

        # create a process safe queue
        mp_manager = multiprocessing.Manager()
        ip_buffr = mp_manager.Queue()
        op_buffr = mp_manager.Queue()

        # create a lock for the shared region
        lock = mp_manager.Lock()

        # binarized SharedObjects data file
        shared = SharedObjects(self.config_num, datalist=self.amoebots)

        _exec_async(self.tracker, ip_buffr, op_buffr, logger, shared, 
                    n_cores, max_iter, buffer_len, lock)

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

        # configure generic handler
        logging.basicConfig(
                        level=logging.DEBUG, 
                        format='[%(levelname)s %(asctime)s]\t%(message)s', 
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
                shared:SharedObjects, 
                n_cores:int, 
                max_iter:int, 
                buffer_len:int, 
                lock:multiprocessing.managers.AcquirerProxy=None
            ):
    r"""
    Set up asynchronous calls for bot execution and create a queueing 
    manager for writing the state configuration file.
    """

    with multiprocessing.Pool(processes=n_cores) as pool:
        # listener process that handles queued writes
        _ = pool.apply_async(_queueing_manager, (
                                                    op_buffr, 
                                                    logger, 
                                                    tracker, 
                                                ))

        # generate an initial list of jobs to be completed
        jobs_init = [[__id] for __id in range(shared.length)]
        for job in jobs_init: ip_buffr.put(job)

        results = list()

        # execute jobs on agents for fixed number of activations
        while True:
            results.append(pool.apply_async(_exec_step, (
                                                        ip_buffr, 
                                                        op_buffr, 
                                                        logger, 
                                                        shared,
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
                shared:SharedObjects=None, 
                lock:multiprocessing.managers.AcquirerProxy=None, 
                amoebot:Agent=None
            ) -> object:
    r""" execute one step of `elements.bots.core.Amoebot.execute()`
    """

    # asynchronous execution mode
    if amoebot is None:
        __id = ip_buffr.get()[0]

        # safely fetch the object at current index position
        lock.acquire(blocking=True)

        try:
            _sh_amoebot = shared.ifetch(__id)
        finally: lock.release()

        # reseed in each process to make sure the pseudo-random streams 
        # are independent of one another
        np.random.seed(int.from_bytes(os.urandom(4), byteorder='little'))

        # execute the amoebot algorithm(s) and update activation status
        _sh_amoebot, actv_status = _sh_amoebot.execute(logger=logger)

        state = (
            _sh_amoebot.head, 
            _sh_amoebot.tail, 
            _sh_amoebot.clock
        )

        if actv_status: 
            # push to output queue if there was an activation for this amoebot
            op_buffr.put([state, __id])

        # safely write to the shared file
        lock.acquire(blocking=True)
        
        try:
            shared.iwrite(__id, _sh_amoebot)
        finally: lock.release()

        # get the current process name for logging
        cpname = multiprocessing.current_process().name

        # generate a log message
        log_message = (
                        f'post/{cpname} :: < agent {__id} {_sh_amoebot} '
                        f'clock {state[2]} active {actv_status} >\n'
                        f'\thead {state[0]} at {state[0].position}\n'
                        f'\ttail {state[1]} at {state[1].position}.'
                    )

        # log the state information
        logging.info(log_message)

        # give other amoebots a chance to catch up
        time.sleep(.2)

        # push the bot id and status information to the queues
        ip_buffr.put([__id])

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
                        f'pop/{cpname} :: < agent {__id} clock {state[2]} >\n'
                        f'\thead {state[0]} at {state[0].position}\n'
                        f'\ttail {state[1]} at {state[1].position}.'
                    )
        logging.info(log_message)

        # call `StateTracker.update` to update the configuration
        tracker.update(__id, state)