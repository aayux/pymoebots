import logging
import numpy as np
import multiprocessing

from numpy import array, ndarray, uint8
from multiprocessing import managers

from .agent import Agent
from ..manager import Manager
from ..tracker import StateTracker

from ...extras.structures import AnonList

class AmoebotManager(Manager):
    r""" 
    Manages sequential and/or asynchronous task assignment to agents of 
    individual amoebots.
    """

    def __init__(self, config_num:str):
        # holds all `Amoebot` objects created anonymously
        self.amoebots: object = AnonList()

        # object of class `StateTracker`
        self.tracker: object = StateTracker(config_num)

    def exec_async(self, n_cores:int, max_iter:int, buffer_len:int=10):
        # create a process safe queue
        mp_manager = multiprocessing.Manager()
        ip_buffr = mp_manager.Queue()
        op_buffr = mp_manager.Queue()

        # start the process that manages the shared memory blocks
        shared = mp_manager.Namespace()

        # create a lock for the shared namespace
        lock = mp_manager.Lock()

        # create a shared list of amoebots
        shared.amoebots = self.amoebots

        # uncomment for stdout logging
        # mp_logger = multiprocessing.log_to_stderr()
        # mp_logger.setLevel(multiprocessing.SUBDEBUG)

        _exec_async(self.tracker, ip_buffr, op_buffr, shared, 
                    lock, n_cores, max_iter, buffer_len)

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
        self.amoebots.insert(agent_of_amoebot, __id)


def _exec_async(
                tracker:object, 
                ip_buffr:object, 
                op_buffr:object, 
                shared:object, 
                lock:object, 
                n_cores:int, 
                max_iter:int, 
                buffer_len:int
            ):
    r"""
    Set up asynchronous calls for bot execution and create a queueing 
    manager for writing the state configuration file.

    returns (dict) : execution status
    """

    with multiprocessing.Pool(processes=n_cores) as pool:
        # create a listener process that handles queued writes
        _ = pool.apply_async(_queueing_manager, (op_buffr, shared, tracker, ))

        # generate an initial list of jobs to be completed
        jobs_init = [[__id] for __id, _ in enumerate(shared.amoebots)]
        for job in jobs_init: ip_buffr.put(job)

        results = list()

        # execute jobs on agents for fixed number of activations
        while not ip_buffr.empty():
            results.append(pool.apply_async(_exec_step, (
                                                    ip_buffr, op_buffr, 
                                                    shared, lock
                                                )))

            # break if maximum iterations have been reached
            if len(results) >= max_iter: break

            # flush the queue if buffer_len reached
            # elif not (len(results) % buffer_len):

            #     # collect results from the pool
            #     for result in results: result.get()

            #     # clear the queue using the listener process
            #     op_buffr.put(['ps-reset', 0])

            #     # empty the results list and decrement max_iter
            #     results = list()
            #     max_iter -= buffer_len

        # collect remaining results from the pool
        for result in results: result.get()

        # exit using the listener process
        op_buffr.put(['ps-kill', 0])


def _exec_step(
        ip_buffr:multiprocessing.managers.AutoProxy=None, 
        op_buffr:multiprocessing.managers.AutoProxy=None, 
        shared:multiprocessing.managers.NamespaceProxy=None, 
        lock:multiprocessing.managers.AcquirerProxy=None, 
        amoebot:Agent=None
    ):
    r""" execute one step of `elements.bots.core.Amoebot.execute()`
    """

    # asynchronous execution mode
    if shared is not None:
        __id = ip_buffr.get()[0]
        
        # copy the correct reference to current amoebot object
        amoebot = shared.amoebots[__id]

        # execute the amoebot algorithm(s) and update activation status
        amoebot, actv_status = amoebot.execute()

        # protect the shared memory from accidental overwrites
        lock.acquire(blocking=True)

        # write the returned reference back to shared memory
        shared_amoebots = shared.amoebots
        shared_amoebots[__id] = amoebot
        shared.amoebots = shared_amoebots

        lock.release()

        # push the status information to the queues
        ip_buffr.put([__id])
        op_buffr.put([__id, actv_status])

    # sequential execution mode
    else:
        # execute the amoebot algorithm(s) and update activation status
        amoebot, _ = amoebot.execute()
        return amoebot

def _queueing_manager(op_buffr:object, shared:object, tracker:object):
    while True:
        # pop the leading entry in the queue
        response = op_buffr.get()
        
        # reset or exit the listener process
        if response[0] == 'ps-kill': break
        # elif response[0] == 'ps-reset': return

        __id, actv_status = response

        # copy the reference to current amoebot object
        amoebot = shared.amoebots[__id]

        # load state information
        state = (amoebot.head, amoebot.tail, amoebot.clock)

        # if there was an activation for this amoebot
        if actv_status:
            # call `StateTracker.update` to update the configuration
            tracker.update(__id, state)