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
from collections import defaultdict

class AmoebotManager(Manager):
    r""" 
    Manages sequential and/or asynchronous task assignment to agents of 
    individual amoebots.

    Attributes

        __nmap (defaultdict) :: a dictionary of dictionaries used to index nodes
                        using x and y co-odrinates.
        amoebots (dict) :: dcitionary of amoebot objects indexed by identifiers.
                        tracker
        tracker (StateTracker) :: instance of `StateTracker` for data handling. 
        config_num (str) :: identifier number for the json configuration file,
                        required here for multiprocessing picklers.
    """

    def __init__(self, nmap:object, config_num:str=None):
        r"""
        Attributes

            __nmap (defaultdict) :: a dictionary of dictionaries used to index 
                            nodes using x and y co-odrinates.
            amoebots (dict) :: dcitionary of amoebot objects indexed by 
                            identifiers.
            tracker (StateTracker) :: instance of `StateTracker` for data 
                            handling. 
            config_num (str) :: identifier number for the json configuration 
                            file, required here for multiprocessing picklers.
        """
        # `nmap` object of the `NodeManager`
        self.__nmap:defaultdict = nmap

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

        self.amoebots[__id] = agent_of_amoebot.pickled

    def exec_async(self, n_cores:int, max_iter:int, buffer_len:int=None):
        r"""
        The function is originally intended as a fully asynchronous, distributed
        manager for the amoebots. To simplify implementation we put a GIL on the
        function.

        NOTE a [WIP] is available in branch `mp-test`

        Attributes

            n_cores (int) :: number of processor cores to use.
            max_iter (int) :: maximum number of iterations before 
                            termination.
            buffer_len (int) default: None :: maximum length of the i/o buffer.
        """

        _exec_async_with_interpreter_lock()

    def exec_sequential(self, max_iter:int) -> dict:
        r"""
        """
        for _ in range(max_iter):
            for __id, amoebot in self.amoebots.items():
                self.amoebots[__id] = _exec_one_step(amoebot=amoebot)

def _exec_async_with_interpreter_lock():
    r"""
    """
    raise NotImplementedError

def _exec_one_step(amoebot:Agent, algorithm:str=None) -> object:
    r""" 
    Execute one step of `action` for the given agent.

    Attributes

        amoebot (Agent) :: an object of class `Agent` that handles `action` 
                        execution.
        algorithm (str) :: algorithm being performed in current step, one of
                        "random_move", "compress"
    """
    # execute the amoebot algorithm(s) and update activation status
    amoebot, _ = amoebot.execute()
    return amoebot