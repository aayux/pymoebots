import psutil
import numpy as np
import multiprocessing

from collections import defaultdict
from numpy import array, ndarray, uint8

from .core import Amoebot

from ..node.core import Node
from ..manager import Manager

from ...functional.tracker import StateTracker
from ...extras.structures import AnonList
from ...extras.exceptions import InitializationError

N_CORES = psutil.cpu_count(logical=True)

class AmoebotManager(Manager):
    r"""
    manages thread assignment to agents and allocates functionals to bots
    """

    def __init__(self, config_num):
        # holds all `Amoebot` objects created anonymously
        self.amoebots: object = AnonList()

        # truth values signalling execution status of each bot, 1 when complete
        self.status: dict = {0: list(), 1: list()}

        # object of class `StateTracker`
        self.tracker: object = StateTracker(self, config_num)

    def m_activate(self) -> uint8:
        r"""
        Sets up parallel calls to activation methods for all bots.

        returns: np.uint8:   execution status
        """
        activate = self._activate

        mp_manager = multiprocessing.Manager()
        queue = mp_manager.Queue()

        with multiprocessing.Pool(processes=N_CORES) as pool:
            
            # create a listener process that handles queued writes
            _ = pool.apply_async(self._queue_manager, (queue,))

            # activate aynchronous agents
            jobs = list()
            for amoebot in self.amoebots:
                job = pool.apply_async(activate, (amoebot, queue))
                jobs.append(job)
            
            # collect results from the pool
            for job in jobs: 
                job.get()

            # kill the listener process
            queue.put(['-9', 'ps-kill'])

            pool.close()
            pool.join()

        status = self.status

        # return 1 if everything ran successfully
        if len(status[0]) == 0: return uint8(1)

        return uint8(0)

    def _add_bot(self, __bot_id, node:Node):
        r"""
        adds individual particles to the (partially anonymous) `AnonList`
        """

        bot = Amoebot(__bot_id, head=node)
        self.amoebots.insert(bot, __bot_id)

    def _activate(self, amoebot:Amoebot, queue:object):
        r"""
        execute one timestep of `elements.bots.core.Amoebot.execute()`
        """
        # TODO: required? copy variables and methods to avoid contention
        status = self.status

        try:
            # execute the amoebot algorithms and update execution status
            status[amoebot.execute()] = amoebot

            # collect state information from this bot
            self.tracker.collect_states(amoebot.__bot_id)
        
        except IndexError:
            raise InitializationError(
                                f"Amoebots have not been initialized ",
                                f"correctly, check file and retry. Exiting!"
            )

        self.status = status

    def _queue_manager(self, queue:object):
        while True:
            # pop the leading entry in the queue
            (__bot_id, config) = queue.get()

            # escape from the listener
            if (__bot_id == -9) and (config == 'ps-kill'): break

            # call `StateTracker.update` to write and
            # overwrite the amoebot data
            self.amoebots[__bot_id].head.position, 
            self.amoebots[__bot_id].tail.position, 
            self.amoebots[__bot_id].port_labels = self.tracker.update(__bot_id, 
                                                                      config)
