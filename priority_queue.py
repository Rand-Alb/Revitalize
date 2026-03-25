"""
-------------------------------------------------------
[priority_queue.py]
-------------------------------------------------------
Author:  Ali Al-Khazraji
ID:      169106570
Email:   alk6570@mylaurier.ca
__updated__ = "2026-03-25"
-------------------------------------------------------
"""
# Imports
from copy import deepcopy

class Priority_Queue:

    def __init__(self):
        self._values = []
        self._first = None

    def is_empty(self):
        return len(self._values) == 0

    def __len__(self):
        return len(self._values)

    def insert(self, value):
        self._values.append(deepcopy(value))
        self._set_first()

    def peek(self):
        assert len(self._values) > 0, "Nobody is in the waiting room."
        return deepcopy(self._values[self._first])

    def remove(self):
        assert len(self._values) > 0, "Nobody is in the waiting room."
        value = self._values.pop(self._first)
        self._set_first()
        return value

    def _set_first(self):
        if len(self._values) == 0:
            self._first = None
        else:
            self._first = 0
            for i in range(1, len(self._values)):
                if self._values[i] < self._values[self._first]:
                    self._first = i