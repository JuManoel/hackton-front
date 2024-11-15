from datetime import datetime

class Message:
    """
    A class to represent a message.

    Attributes:
    -----------
    role : str
        The role of the message sender (default is "system").
    content : str
        The content of the message (default is "Bienvenido a la llamada").
    urlAudio : str
        The URL of the audio message (currently commented out).

    Methods:
    --------
    __str__():
        Returns a string representation of the message.
    toDict():
        Converts the message to a dictionary format.
    """
    def __init__(self, role="system", content="Bienvenido a la llamada", date=None):
        self.role = role
        self.content = content
        self.date = date or datetime.now().strftime("%Y-%m-%dT%H:%M")
        
    def toDict(self):
        return {"role":self.role,
                "content":self.content,
                "date":self.date
                }
    
    def toDictChat(self):
        return {"role":self.role,
                "content":self.content}
    @classmethod
    def fromDict(cls, data):
        return cls(role=data.get("role", "system"), 
                   content=data.get("content", "Bienvenido a la llamada"),
                   date=data.get("date", datetime.now().strftime("%Y-%m-%dT%H:%M")))