# -*- coding: utf-8 -*-

""" elements/bot/agent.py
"""

from .core import Amoebot
from .functional import compress_agent_sequential
from ...utils.graphs import GraphAlgorithms

import numpy as np
from collections import defaultdict

ALGORITHMS = ['random_move', 'compress']


class Agent(Amoebot):
    r"""
    Inherits from class `Amoebots`. Each amoebot launches an `Agent` at each 
    round of activation that performs one step of the desired algorithm.
    """

    def __init__(self, __id:np.uint8, head:np.ndarray, tail: np.ndarray=None):
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

    def execute(
                    self,
                    __node_array:defaultdict,
                    algorithm:str='random_move',
                    async_mode:bool=True,
                ) -> tuple:
        r"""
        Worker function for each amoebot. Intended to manage parallelisation 
        between agents and attach algorithmic modules to the amoebot.

        Attributes

            __node_array (numpy.ndarray) ::
            algorithm (str) default: 'random_move' :: algorithm being performed 
                            in current step, one of "random_move", "compress" 
                            ...
            async_mode (bool) default: True :: if True, execute the local, 
                            distributed, asynchronous algorithm for compression 
                            else run sequential algorithm.

        Return (numpy.ndarray): 
        """

        # make sure `algorithm` is available
        assert algorithm in ALGORITHMS, \
            LookupError(f'{algorithm} not in list of allowed algorithms.')

        # self.generate_neighbourhood_map(__node_array)

        # get the function handler for `algorithm` from the dictionary
        if algorithm == 'random_move':
            # run one step of an elementary algorithm
            __node_array = self._move(__node_array)

        elif algorithm == 'compress':
            __node_array = self._compress(__node_array, async_mode=async_mode)

        else:
            return (self, __node_array)

        # self.generate_neighbourhood_map(__node_array)

        return (self, __node_array)

    def _move(
                self,
                __node_array:np.ndarray,
                port:np.uint8=None,
                backward:bool=False
            ) -> np.ndarray:
        r"""
        Simple (random) movement algorithm for the amoebot model.

        Attributes

            __node_array (numpy.ndarray) :: 
            port (numpy.uint8) default: None :: port number to move to; if no 
                            value provided, one of two things can happen:

                    if particle is contracted:  expands to occupy random 
                                                position
                    if particle is expanded:    contracts to head or tail,
                                                depending on `backward` flag.
            backward (bool) default: False :: contract to tail if true, else 
                            contract to head.

        Returns (numpy.ndarray): 
        """

        raise NotImplementedError

    def _compress(
                    self,
                    __node_array:np.ndarray, 
                    async_mode:bool=True,
                ) -> np.ndarray:
        r"""
        Compression agorithm for the amoebot model based on 

        Sarah Cannon, Joshua J. Daymude, Dana Randall, and Andréa W. Richa
        A Markov chain algorithm for compressionin self-organizing particle 
        systems (2016); full text at arxiv.org/abs/1603.07991

        Attributes

            agent (Core) :: instance of class `Agent`
            __node_array (numpy.ndarray) :: 
            points_dict (dict) :: 
            async_mode (bool) default: True :: if True, execute the local, 
                        distributed, asynchronous algorithm for compression else
                        run sequential algorithm.

        Returns (numpy.ndarray): 
        """

        # execute the sequential Markov Chain algorithm M
        if not async_mode:
            __node_array = compress_agent_sequential(
                                                        self, 
                                                        __node_array, 
                                                        __id=self.__id
                                                    )

        # execute the asynchronous algorithm for compression
        else:
            if self._is_contracted:
                __node_array = compress_agent_async_contracted(
                                                                self, 
                                                                __node_array
                                                            )
            else:
                __node_array = compress_agent_async_expanded(
                                                                self, 
                                                                __node_array
                                                            )

        return __node_array
