from enum import Enum
from http import HTTPStatus


class Weekday(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


if __name__ == '__main__':
    print(Color.RED)
    print(Color.RED.name)
    print(Color.RED.value)