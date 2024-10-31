from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder


class FloatValueDecoder:

    @staticmethod
    def decode(registers):
        number_count = int(len(registers) / 2)
        decoder = BinaryPayloadDecoder.fromRegisters(registers, byteorder=Endian.BIG, wordorder=Endian.BIG)
        return [round(decoder.decode_32bit_float(), 1) for _ in range(number_count)]
