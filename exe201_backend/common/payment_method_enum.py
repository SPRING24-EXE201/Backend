from enum import IntEnum, unique


@unique
class PaymentMethod(IntEnum):
    PAYOS = 1
