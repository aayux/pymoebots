# -*- coding: utf-8 -*-

""" elements/manager.py
"""

from abc import ABC

class Manager(ABC):
    r""" abstract base class for element manager objects.
    """
    __slots__ = ['__weakref__']
    def __init__(self): pass