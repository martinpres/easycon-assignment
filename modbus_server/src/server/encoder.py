from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder


class FloatValueEncoder:

    @staticmethod
    def encode(values):
        builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.BIG)
        for value in values:
            builder.add_32bit_float(value)

        return builder.to_registers()
