from backend.models.pago import Pago
class Cuenta():
    """
    Enum representing different subscription plans.

    Attributes:
        NONE (str): Represents no subscription plan.
        BASIC (str): Represents the basic subscription plan.
        STANDARD (str): Represents the standard subscription plan.
        PREMIUM (str): Represents the premium subscription plan.

    Methods:
        getPlanByPrice(price):
            Determines the subscription plan based on the given price.

            Args:
                price (float): The price to determine the subscription plan.

            Returns:
                Plans: The corresponding subscription plan based on the price.
    """
    def __init__(self, customerId = "", montoDeuda = 0, fechaCorte = "", historial = []):
        self.customerId = str(customerId)
        self.montoDeuda = float(montoDeuda)
        self.fechaCorte = fechaCorte
        self.historial = list(historial)
    
    def toDict(self):
        return {
            "customerId": self.customerId,
            "totalDeuda": self.montoDeuda,
            "fechaCorte": self.fechaCorte,
            "historialPagos": [pago.toDict() for pago in self.historial]
        }

    @classmethod
    def fromDict(cls, dict):
        pagos = [Pago.fromDict(pago) for pago in dict.get("historialPagos", [])]
        return cls(dict.get("customerId"), 
                   dict.get("montoDeuda"),
                   dict.get("fechaCorte"),
                   pagos)