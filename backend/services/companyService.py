from backend.repositories.repository import Repository
from backend.models.company import Company
class CompanyService:
    def __init__(self, uri, database):
        self.companyRepository = Repository(uri, database, "Company")

    def getCompanyById(self, companyId):
        query = f"{{'companyId': '{companyId}'}}"
        return self.companyRepository.findOne(query)

    def createCompany(self, company):
        query = f"{{'companyId': '{company.companyId}'}}"
        return self.companyRepository.insert(query)

    def updateCompany(self, companyId, company):
        query = f"{{'companyId': '{companyId}'}}"
        replace = company.toDict()
        return self.companyRepository.updateOne(query, replace)

    def deleteCompany(self, companyId):
        query = f"{{'companyId': '{companyId}'}}"
        return self.companyRepository.deleteOne(query)