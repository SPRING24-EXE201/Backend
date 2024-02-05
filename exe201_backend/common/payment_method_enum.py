from enum import IntEnum, unique


@unique
class PaymentMethod(IntEnum):
    VNPAY = 1,
    MOMO = 2
