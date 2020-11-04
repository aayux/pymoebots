# -*- coding: utf-8 -*-

""" elements/bot/manager.py
"""

from .agent import Agent
from ..manager import Manager
from ..tracker import StateTracker
from ...utils.shared_objects import SharedObjects

import os
import time
import numpy as np
from pathlib import Path
from functools import partial
from concurrent import futures
from collections import defaultdict

class AmoebotManager(Manager):
    r""" 
    Manages sequential and/or asynchronous task assignment to agents of 
    individual amoebots.

    Attributes

        __nmap (defaultdict) :: a dictionary of dictionaries used to index nodes
                        using x and y co-ordinates.
        amoebots (dict) :: dcitionary of amoebot objects indexed by identifiers.
                        tracker
        shared (SharedObjects) :: a custom shared memory object for pickling
                        and unpickling the data dumps. Useful in true 
                        multiprocessing implementations.
        tracker (StateTracker) :: instance of `StateTracker` for data handling. 
        config_num (str) :: identifier number for the json configuration file,
                        required here for multiprocessing picklers.
    """

    def __init__(self, __nmap:object, config_num:str=None):
        r"""
        Attributes

            __nmap (defaultdict) :: a dictionary of dictionaries used to index 
                            nodes using x and y co-ordinates.
            amoebots (dict) :: dcitionary of amoebot objects indexed by 
                            identifiers.
            tracker (StateTracker) :: instance of `StateTracker` for data 
                            handling. 
            config_num (str) :: identifier number for the json configuration 
                            file, required here for multiprocessing picklers.
        """
        # `nmap` object of the `NodeManager`
        self.__nmap:defaultdict = __nmap

        # map of all `Amoebot` objects
        self.amoebots:dict = dict()

        # object of class `StateTracker`
        self.tracker:object = StateTracker(config_num)

        # configuration identifier for logging
        self.config_num = config_num

    def _add_bot(
                    self, 
                    __id:np.uint8, 
                    head:np.ndarray, 
                    tail:np.ndarray=None
                ):
        r""" 
        Adds individual particles to the dictionary of amoebots.

        Attributes

            __id (numpy.uint8) :: unique particle identifier.
            head (numpy.ndarray) :: position (x and y co-ordinates) of amoebot 
                            head.
            tail (numpy.ndarray) default: None :: position (x and y 
                            co-ordinates) of amoebot tail.
        """
        agent_of_amoebot = Agent(__id, head=head, tail=tail)

        # update the node map for current particle
        if np.all(head == tail) or (tail is None):
            self.__nmap[head[0]][head[1]].place_particle('body')
        else:
            # place the head and tail on different grid positions
            self.__nmap[tail[0]][tail[1]].place_particle('body')
            self.__nmap[head[0]][head[1]].place_particle('head')

        # call to orient the amoebot
        # NOTE how nmap is only shared when needed
        agent_of_amoebot.orient(self.__nmap)

        # store a serialized objects for efficiency
        self.amoebots[__id] = agent_of_amoebot.pickled

    def exec_async(
                    self, 
                    n_cores:int, 
                    max_rnds:int, 
                    buffer_len:int=None,
                    algorithm:str=None
                ):
        r"""
        The function is originally intended as a fully asynchronous, distributed
        manager for the amoebots. To simplify implementation we put a GIL on the
        function.

        NOTE a [WIP] is available in branch `mp-test`

        Attributes

            n_cores (int) :: number of processor cores to use.
            max_rnds (int) :: maximum number of full rounds before termination.
            buffer_len (int) default: None :: maximum length of the i/o buffer.
            algorithm (str) default: None :: algorithm being performed in 
                        current step, one of "random_move", "compress"
        """

        # dump the amoebot dictionary into a pickle(d) database
        self.shared = SharedObjects(self.config_num, data=self.amoebots)

        # call the psuedo-async method for execution
        self._exec_async_with_interpreter_lock(n_cores, max_rnds, 
                                               buffer_len, algorithm)

    def exec_sequential(
                            self, 
                            max_rnds:int, 
                            algorithm:str=None
                        ):
        r"""
        Sequentially execute the `algorithm`.

        Attributes

            shared (SharedObjects) :: a custom shared memory object for pickling
                        and unpickling the data dumps. Useful in true 
                        multiprocessing implementations.
            max_rnds (int) :: maximum number of full rounds before termination.
            algorithm (str) default: None :: algorithm being performed in 
                        current step, one of "random_move", "compress" ...
        """

        # dump the amoebot dictionary into a pickle(d) database
        self.shared = SharedObjects(self.config_num, data=self.amoebots)

        # iteratively execute the algorithm over each amoebot for fixed rounds
        for _ in range(max_rnds):
            exec_seq = list(self.amoebots.keys())
            np.random.shuffle(exec_seq)
            for __id in exec_seq:
                amoebot_t = (__id, self.amoebots[__id])
                self.amoebots[__id] = self._exec_one_step(amoebot_t, algorithm)

    def _exec_async_with_interpreter_lock(
                                            self, 
                                            n_cores:int, 
                                            max_rnds:int, 
                                            buffer_len:int=None, 
                                            algorithm:str=None
                                        ):
        r"""
        Call the "asynchronous" function on the amoebots using 
        `ThreadPoolExecutor` which uses a global lock on the Python interpreter.
        The resulting calls are therefore not truly concurrent.

        Attributes

            n_cores (int) :: number of processor cores to use.
            max_rnds (int) :: maximum number of full rounds before termination.
            buffer_len (int) default: None :: maximum length of the i/o buffer.
            algorithm (str) default: None :: algorithm being performed in 
                        current step, one of "random_move", "compress" ...
        """

        # define partial function with pre-specified algorithm
        _exec_one_step_algorithm = partial(
                                            self._exec_one_step, 
                                            shared=self.shared, 
                                            algorithm=algorithm
                                        )

        # zip identifier to amoebot objects for `map` function
        amoebots_z = zip(self.amoebots.keys(), self.amoebots.values())

        for _ in range(max_rnds):
            # set up the asynchronous caller with GIL
            with futures.ThreadPoolExecutor(max_workers=n_cores) as executor:
                # map amoebots to the executor function and run asynchronously
                executor.map(self._exec_one_step, amoebots_z)

    def _exec_one_step(
                        self, 
                        amoebot_t:tuple, 
                        algorithm:str=None
                    ) -> Agent:
        r""" 
        Execute one step of `algorithm` for the given agent.

        Attributes

            amoebot_t (tuple) :: a tuple with `Agent` and its respective 
                        identifier.
            algorithm (str) default: None :: algorithm being performed in 
                        current step, one of "random_move" and "compress"...
        """

        # unpack the 2-tuple
        __id, _ = amoebot_t

        # fetch and unpickle the instance of amoebot
        amoebot = Agent.unpickled(self.shared.ifetch(__id))

        # execute the amoebot algorithm(s) and update activation status
        amoebot, self.__nmap = amoebot.execute(self.__nmap, algorithm)

        # write back to data dump
        self.shared.iwrite(__id, amoebot.pickled)

        # create state tuple if activated in this round
        state = (
                    amoebot.head, 
                    amoebot.tail, 
                    amoebot.tau
                )

        self.tracker.update(__id, state)

        return amoebot