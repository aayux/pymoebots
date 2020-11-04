# -*- coding: utf-8 -*-

""" elements/bot/agent.py
"""

import .functional as F
from .core import Amoebot
from ...utils.graphs import GraphAlgorithms

import numpy as np
from collections import defaultdict

ALGORITHMS = ['random_move', 'compress']

class Agent(Amoebot):
    r"""
    Inherits from class `Amoebots`. Each amoebot launches an `Agent` at each 
    round of activation that performs one step of the desired algorithm.
    """

    def __init__(self, __id:np.uint8, head:np.ndarray, tail:np.ndarray=None):
        r"""
        Attributes

            __id (numpy.uint8) :: unique particle identifier.
            head (numpy.ndarray) :: position (x and y co-ordinates) of amoebot 
                            head.
            tail (numpy.ndarray) default: None :: position (x and y co-ordinates) 
                            of amoebot tail.
        """

        # initialise the super class
        super().__init__(__id, head, tail)

        # does not share id with super class
        self.__id = __id

    def execute(self, __nmap:defaultdict, algorithm:str='random_move') -> tuple:
        r"""
        Worker function for each amoebot. Intended to manage parallelisation 
        between agents and attach algorithmic modules to the amoebot.

        Attributes

            __nmap (defaultdict) :: a dictionary of dictionaries used to index 
                            nodes using x and y co-ordinates.
            algorithm (str) default: 'random_move' :: algorithm being performed 
                            in current step, one of "random_move", "compress" 
                            ...

        Return (defaultdict): udpated `__nmap` dictionary.
        """

        # make sure `algorithm` is available
        assert algorithm in ALGORITHMS, \
                LookupError(f'{algorithm} not in list of allowed algorithms.')

        # get the function handler for `algorithm` from the dictionary
        if algorithm == 'random_move':
            _algorithm = self._move

        elif _algorithm == 'compress':
            _algorithm = self._compress

        else:
            return (self, __nmap)

        # run one step of an elementary algorithm
        __nmap = _algorithm(__nmap)

        self.generate_neighbourhood_map(__nmap)

        return (self, __nmap)
    
    def _move(
                self, 
                __nmap:defaultdict, 
                port:np.uint8=None, 
                backward:bool=False
            ):
        r"""
        Simple (random) movement algorithm for the amoebot model.

        Attributes

            __nmap (defaultdict) :: a dictionary of dictionaries used to index 
                                    nodes using x and y co-ordinates.
            port (numpy.uint8) default: None :: port number to move to; if no 
                            value provided, one of two things can happen:

                    if particle is contracted:  expands to occupy random 
                                                position
                    if particle is expanded:    contracts to head or tail,
                                                depending on `backward` flag.
            backward (bool) default: False :: contract to tail if true, else 
                            contract to head.
        """

        # contract an expanded particle
        if  not self._is_contracted:
            __nmap = F.contract_particle(self, __nmap, backward)

        # expand a contracted particle
        else:
            __nmap = F.expand_particle(self, __nmap, port)

        return __nmap

    def compress(
                self, 
                __nmap:defaultdict, 
                async_mode:bool=True
            ) -> defaultdict:
        r"""
        Compression agorithm for the amoebot model based on 

        Sarah Cannon, Joshua J. Daymude, Dana Randall, and Andréa W. Richa
        A Markov chain algorithm for compressionin self-organizing particle 
        systems (2016); full text at arxiv.org/abs/1603.07991

        Attributes

            agent (Core) :: instance of class `Agent`
            __nmap (defaultdict) :: a dictionary of dictionaries used to index nodes 
                        using x and y co-ordinates.
            async_mode (bool) :: if True, execute the local, distributed, 
                        asynchronous algorithm for compression else run sequential 
                        algorithm.

        Return (defaultdict): the updated `__nmap` dictionary.
        """

        # execute the sequential Markov Chain algorithm M
        if not async_mode: __nmap = F.compress_agent_sequential()

        # execute the asynchronous algorithm for compression
        else:
            if self._is_contracted: 
                __nmap = F.compress_agent_async_contracted(__nmap)
            else: __nmap = F.compress_agent_async_expanded(__nmap)

        return __nmap