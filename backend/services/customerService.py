from backend.repositories.repository import Repository
class CustomerService:
    def __init__(self):
        self.customerRepository = Repository(collectionName = "customers")

    def createCustomer(self, customer):
        return self.customerRepository.insertOne(customer.toDict())

    def getCustomer(self, customerId):
        print(customerId)

        query = {'customerId': customerId}
        return self.customerRepository.findOne(query)

    def updateCustomer(self, customerId, customer):
        query = {"customerId": customerId}
        replace = customer.toDict()
        return self.customerRepository.replaceOne(query, replace)

    def deleteCustomer(self, customerId):
        query = f"{{'customerId': '{customerId}'}}"
        return self.customerRepository.deleteOne(query)