import logging
import numpy as np
import multiprocessing

from collections import defaultdict
from numpy import array, ndarray, uint8

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
        q_in = mp_manager.Queue()
        q_out = mp_manager.Queue()

        # start the process that manages the shared memory blocks
        shared_mem = mp_manager.Namespace()

        # create a shared list of amoebots
        shared_mem.amoebots = self.amoebots

        # uncomment for stdout logging
        # mp_logger = multiprocessing.log_to_stderr()
        # mp_logger.setLevel(multiprocessing.SUBDEBUG)

        _exec_async(self.tracker, q_in, q_out, shared_mem, 
                    n_cores, max_iter, buffer_len)

    def exec_sequential(self, max_iter:int) -> dict:
        r"""
        """
        for _ in range(max_iter):
            for __id, _ in enumerate(self.amoebots):
                self.amoebots[__id] = _exec_step(amoebots=self.amoebots[__id])

    def _add_bot(self, __id:int, node:object):
        r""" adds individual particles to the (partially anonymous) `AnonList`
        """
        agent_of_amoebot = Agent(__id, head=node)
        self.amoebots.insert(agent_of_amoebot, __id)


def _exec_async(
                tracker:object, 
                q_in:object, 
                q_out:object, 
                shared_mem:object, 
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
        _ = pool.apply_async(_queueing_manager, (q_out, shared_mem, tracker, ))

        # generate an initial list of jobs to be completed
        jobs_init = [[__id] for __id, _ in enumerate(shared_mem.amoebots)]
        for job in jobs_init: q_in.put(job)

        results = list()
        # execute jobs on agents for fixed number of activations
        while not q_in.empty():
            results.append(pool.apply_async(_exec_step, 
                                                (q_in, q_out, shared_mem))
                                            )

            # break if maximum iterations have been reached
            if len(results) >= max_iter: break

            # flush the queue if buffer_len reached
            # elif not (len(results) % buffer_len):

            #     # collect results from the pool
            #     for result in results: result.get()

            #     # clear the queue using the listener process
            #     q_out.put(['ps-reset', 0])

            #     # empty the results list and decrement max_iter
            #     results = list()
            #     max_iter -= buffer_len

        # collect remaining results from the pool
        for result in results: result.get()

        # exit using the listener process
        q_out.put(['ps-kill', 0])

        pool.close()
        pool.join()


def _exec_step(
                q_in:object=None, 
                q_out:object=None, 
                shared_mem:object=None, 
                amoebots:object=None
            ):
    r""" execute one step of `elements.bots.core.Amoebot.execute()`
    """

    # asynchronous mode
    if shared_mem is not None:
        __id = q_in.get()[0]
        
        # copy the correct reference to current amoebot object
        amoebot = shared_mem.amoebots[__id]

        # execute the amoebot algorithm(s) and update activation status
        amoebot, actv_status = amoebot.execute()

        # write the returned reference back to shared memory
        shared_mem_amoebots = shared_mem.amoebots
        shared_mem_amoebots[__id] = amoebot
        shared_mem.amoebots = shared_mem_amoebots

        # push the status information to the queues
        q_in.put([__id])
        q_out.put([__id, actv_status])

    # sequential mode
    else:
        # execute the amoebot algorithm(s) and update activation status
        amoebot, _ = amoebot.execute()
        return amoebot

def _queueing_manager(q_out:object, shared_mem:object, tracker:object):
    while True:
        # pop the leading entry in the queue
        response = q_out.get()

        # reset or exit the listener process
        # if response[0] == 'ps-reset': return
        # elif response[0] == 'ps-kill': break
        if response[0] == 'ps-kill': break

        __id, actv_status = response

        # copy the reference to current amoebot object
        amoebot = shared_mem.amoebots[__id]

        # load state information
        state = (amoebot.head, amoebot.tail, amoebot.clock)

        # if there was an activation for this amoebot
        if actv_status:
            # call `StateTracker.update` to update the configuration
            tracker.update(__id, state)