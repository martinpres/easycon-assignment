class DataConsumer:

    def __init__(self, context, value_encoder):
        self._context = context
        self._value_encoder = value_encoder

    def consume(self, data):
        self._context[0].setValues(0x4, 0x00, self._value_encoder.encode(data))
