from backend.models.customer import Customer
from datetime import datetime
from backend.models.message import Message
import uuid
class Call:
    def __init__(self, messages = [], customerId = 0, recordDate = None):
        self.messages = list(messages)
        self.customerId = customerId
        self.recordDate = recordDate or datetime.now().strftime("%Y-%m-%dT%H:%M")

    def toDict(self):
        return {
            "messages": [message.toDict() for message in self.messages],
            "customerId": self.customerId,
            "recordDate": self.recordDate
        }
    
    @classmethod
    def fromDict(cls, data):
        messages = [Message.fromDict(msg) for msg in data.get("messages", [])]
        customerId = data.get("customerId", 0)
        recordDate = data.get("recordDate", datetime.now().strftime("%Y-%m-%dT%H:%M"))
        return cls(messages=messages, customerId=customerId, recordDate=recordDate)
