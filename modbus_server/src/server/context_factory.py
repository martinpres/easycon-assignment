from pymodbus.datastore import ModbusSlaveContext, ModbusSequentialDataBlock, ModbusServerContext


def get_context():
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0]),
        co=ModbusSequentialDataBlock(0, [0]),
        hr=ModbusSequentialDataBlock(0, [0]),
        ir=ModbusSequentialDataBlock(0, [0] * 8)
    )

    return ModbusServerContext(slaves=store, single=True)
