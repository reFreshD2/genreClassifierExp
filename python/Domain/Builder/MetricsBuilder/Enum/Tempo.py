from enum import Enum


class Tempo(str, Enum):
    UNDEFINED = 0
    SLOWLY = 1
    ANDANTE = 2
    LIVELY = 3
    FAST = 4
