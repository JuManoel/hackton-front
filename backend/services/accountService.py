from backend.repositories.repository import Repository
class AccountService:
    def __init__(self):
        self.accountRepository = Repository(collectionName = "accounts")

    def getAccount(self, customerId):
        print(customerId)

        query = {'customerId': customerId}
        return self.accountRepository.findOne(query)

    def updateAccount(self, customerId, customer):
        query = {"customerId": customerId}
        replace = customer.toDict()
        return self.accountRepository.replaceOne(query, replace)