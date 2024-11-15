
class Company:
    """
    A class used to represent a Company.

    Attributes
    ----------
    id : int
        The unique identifier for the company.
    companyName : str
        The name of the company.
    companyInfo : str
        Information about the company.
    companyPlan : str
        The plan or strategy of the company.

    Methods
    -------
    __init__(self, id=0, companyName="", companyInfo="", companyPlan="")
        Initializes the Company with the provided id, companyName, companyInfo, and companyPlan.
    """
    def __init__(self, id = 0, companyName = "", companyInfo = "", companyPlan = ""):
        self.id = int(id)
        self.companyName = str(companyName)
        self.companyInfo = str(companyInfo)
        self.companyPlan = str(companyPlan)
    def toDict(self):
        """
        Converts the Company object to a dictionary.

        Returns
        -------
        dict
            A dictionary representation of the Company object.
        """
        return {
            "id": int(self.id),
            "companyName": self.companyName,
            "companyInfo": self.companyInfo,
            "companyPlan": self.companyPlan
        }
    @classmethod
    def fromDict(cls, dict):
        """
        Creates a Company object from a dictionary.

        Parameters
        ----------
        dict : dict
            A dictionary containing the company information.

        Returns
        -------
        Company
            A Company object created from the dictionary.
        """
        return cls(
            id=dict.get("id", 0),
            companyName=dict.get("companyName", ""),
            companyInfo=dict.get("companyInfo", ""),
            companyPlan=dict.get("companyPlan", "")
        )