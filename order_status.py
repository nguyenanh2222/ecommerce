from enum import Enum


class EOrderStatus(str, Enum):
    OPEN_ORDER = "OPEN"
    CONFIRMED_ORDER = "CONFIRMED"
    COMPLICATED_ORDER = "COMPLICATED"
    CANCELLED_ORDER = "CANCELLED"
