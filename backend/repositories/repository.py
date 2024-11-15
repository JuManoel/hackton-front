import pymongo
from pymongo import MongoClient

class Repository:
    """
    A class to interact with a MongoDB collection.
    Attributes:
    ----------
    uri : str
        The URI for the MongoDB connection.
    client : MongoClient
        The MongoDB client.
    database : Database
        The MongoDB database.
    collection : Collection
        The MongoDB collection.
    Methods:
    -------
    findOne(queryFilter):
        Finds a single document in the collection that matches the query filter.
    findMany(queryFilter):
        Finds multiple documents in the collection that match the query filter.
    insert(listInsert):
        Inserts multiple documents into the collection.
    updateMany(filter, operation):
        Updates multiple documents in the collection that match the filter.
    updateOne(filter, operation):
        Updates a single document in the collection that matches the filter.
    replaceOne(queryFilter, replaceDocument):
        Replaces a single document in the collection that matches the query filter.
    deleteOne(queryFilter):
        Deletes a single document in the collection that matches the query filter.
    deleteMany(queryFilter):
        Deletes multiple documents in the collection that match the query filter.
    """

    URI = "mongodb+srv://juanocampo38402:12345@cluster0.qtzt0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    DATABASE_NAME = "DB_Assistant"

    def __init__(self, collectionName):
        try:
            self.client = MongoClient(self.URI)
            self.database = self.client[self.DATABASE_NAME]
            self.collection = self.database[collectionName]
            print("Connected to MongoDB")
        except pymongo.errors.ConnectionFailure as e:
            print(f"Error: {e}")
            self.client = None
            self.database = None
    
    def findOne(self, queryFilter):
        return self.collection.find_one(queryFilter)
    
    def findMany(self, queryFilter):
        return list(self.collection.find(queryFilter))

    def insertOne(self, document):
        result = self.collection.insert_one(document)
        return result
    
    def insertMany(self, listInsert):
        result = self.collection.insert_many(listInsert)
        return result.acknowledged
    
    def updateMany(self, filter, operation):
        result = self.collection.update_many(filter, operation)
        return result.modified_count
    
    def updateOne(self, filter, operation):
        result = self.collection.update_one(filter, operation)
        return result.modified_count
    
    def replaceOne(self, queryFilter, replaceDocument):
        result = self.collection.replace_one(queryFilter, replaceDocument)
        return result.modified_count
    
    def deleteOne(self, queryFilter):
        result = self.collection.delete_one(queryFilter)
        return result.deleted_count   

    def deleteMany(self, queryFilter):
        result = self.collection.delete_many(queryFilter)
        return result.deleted_count 