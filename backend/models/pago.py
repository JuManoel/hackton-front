class Pago:
    def __init__(self, monto, fechaAPagar):
        self.monto = monto
        self.fechaAPagar = fechaAPagar

    def to_dict(self):
        return {
            'monto': self.monto,
            'fechaAPagar': self.fechaAPagar
        }
    @classmethod
    def from_dict(cls, data):
        return cls(
            monto=data.get('monto'),
            fechaAPagar=data.get('fechaAPagar')
        )