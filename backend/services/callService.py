from backend.repositories.repository import Repository
from backend.models.call import Call
from bson.objectid import ObjectId

class CallService:
    def __init__(self):
        self.callRepository = Repository(collectionName = "calls")

    def createCall(self, call):
        return self.callRepository.insertOne(call.toDict())
        
    def getCall(self, callId):
        query = {"_id": ObjectId(callId)}
        return Call.fromDict(self.callRepository.findOne(query))
        
    def updateCustomerId(self, callId, customerId):
        query = {"_id": ObjectId(callId)}
        update = {"$set": {"customerId": customerId}}
        return self.callRepository.updateOne(query, update)
    
    def addMessage(self, callId, message):
        query = {"_id": ObjectId(callId)}
        update = {"$push": {"messages": message.toDict()}}
        return self.callRepository.updateOne(query, update)
        
    def deleteCall(self, callId):
        query = f"{{'callId': '{callId}'}}"
        return self.callRepository.deleteOne(query)