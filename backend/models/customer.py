class Customer:
    """
    __init__(self, id=0, customerId="", name="", age=18, currentPlan=Plans("Basic"), phoneNumber="")
        Initializes a new instance of the Customer class.
    """
    def __init__(self, customerId = "", name = "", age = "", phoneNumber = ""):
        self.customerId = str(customerId)
        self.name = str(name)
        self.age = age
        self.phoneNumber = str(phoneNumber)
    
    def toDict(self):
        """
        Converts the Customer object to a dictionary.

        Returns
        -------
        dict
            A dictionary representation of the Customer object.
        """
        return {
            "customerId": self.customerId,
            "name": self.name,
            "age": self.age,
            "phoneNumber": self.phoneNumber
        }
    @classmethod
    def fromDict(cls, data):
        """
        Creates a Customer object from a dictionary.

        Parameters
        ----------
        data : dict
            A dictionary containing the customer data.

        Returns
        -------
        Customer
            A Customer object created from the dictionary data.
        """
        return cls(
            customerId=data.get("customerId", ""),
            name=data.get("name", ""),
            age=data.get("age", ""),
            phoneNumber=data.get("phoneNumber", "")
        )