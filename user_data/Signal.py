class Signal:
    optimize = True
    min_value = 0
    max_value = 100
    default_value = 0
    type = ''
    name = ''

    def __init__(self, name: str, test, overridable: bool = True, min_value: int = 0, max_value: int = 100,
                 default_value: int = 0):
        self.optimize = overridable
        self.min_value = min_value
        self.max_value = max_value
        self.test = test
        self.default_value = default_value
        self.name = name


class BuySignal(Signal):
    type = 'buy'
    pass


class SellSignal(Signal):
    type = 'sell'
    pass
