from enum import Enum


class Tempo(str, Enum):
    UNDEFINED = 'Неопределенный'
    SLOWLY = 'Медленный'
    ANDANTE = 'Умеренный'
    LIVELY = 'Оживленный'
    FAST = 'Быстрый'
