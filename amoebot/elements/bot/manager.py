import logging
import numpy as np
import multiprocessing

from collections import defaultdict
from numpy import array, ndarray, uint8

from .agent import Agent
from ..manager import Manager
from ..tracker import StateTracker
from ...extras.structures import AnonList, PersistentStore

class AmoebotManager(Manager):
    r""" manages thread assignment to agents and allocates functionals to bots
    """

    def __init__(self, config_num:str):
        # holds all `Amoebot` objects created anonymously
        self.amoebots: object = AnonList()

        # object of class `StateTracker`
        self.tracker: object = StateTracker(config_num)

        # persistent storage for asynchronous read/write
        self.store = PersistentStore(config_num)

    def exec_async(self, n_cores:int) -> dict:
        r"""
        Set up asynchronous calls for bot execution and create a queueing 
        manager for writing the state configuration file.

        returns (dict) : execution status
        """

        mp_manager = multiprocessing.Manager()
        queue = mp_manager.Queue()

        # mp_logger = multiprocessing.log_to_stderr()
        # mp_logger.setLevel(multiprocessing.SUBDEBUG)

        with multiprocessing.Pool(processes=n_cores - 1) as pool:
            
            # load the persistent storage
            self.store.read()

            # create a listener process that handles queued writes
            _ = pool.apply_async(self._queueing_manager, (queue,))

            # execute algorithm on aynchronous agents
            for __bot_id, _ in enumerate(self.amoebots):
                job = pool.apply_async(self._exec_step, 
                                            (__bot_id, queue)
                                    )

                # collect results from the pool
                job.get()

            # kill the listener process
            queue.put(['ps-kill', '', ''])

            pool.close()
            pool.join()

    def exec_sequential(self) -> dict:
        r"""
        """
        for __bot_id, _ in enumerate(self.amoebots):
            self._exec_step(__bot_id)

    def _exec_step(self, __bot_id:int, queue:object=None):
        r""" execute one step of `elements.bots.core.Amoebot.execute()`
        """
        # for asynchronous function calls
        if queue is not None: 
            if not self.store.persistent[__bot_id]:
                self.store.persistent[__bot_id] = self.amoebots[__bot_id]

            # read amoebot data from persistent state
            amoebot = self.store.persistent[__bot_id]
            
            # execute the amoebot algorithm(s) and update execution status
            amoebot, actv_status = amoebot.execute()

            queue.put([__bot_id, amoebot, actv_status])
        
        else: amoebot, actv_status = self.amoebots[__bot_id].execute()

    def _queueing_manager(self, queue:object):
        while True:
            # pop the leading entry in the queue
            response = queue.get()

            # exit the listener process
            if response[0] == 'ps-kill': break
            
            __bot_id, amoebot, actv_status = response

            self.store.persistent[__bot_id] = amoebot

            state = (amoebot.head, amoebot.tail, amoebot.clock)

            # if there was an activation for this bot
            if actv_status:
                # call `StateTracker.update` to update the configuration
                self.tracker.update(__bot_id, state)

        self.store.write()


    def _add_bot(self, __bot_id:int, node:object):
        r""" adds individual particles to the (partially anonymous) `AnonList`
        """
        bot = Agent(__bot_id, head=node)
        self.amoebots.insert(bot, __bot_id)
