
from pymongo import MongoClient
from pymongo.errors import CollectionInvalid


def getDBHandler(dbName):
    # code to set up mongo connection
    # return handle on DB
    connection = MongoClient('localhost', 27017)
    db = connection[dbName]
    return db

def getCollectionHandler(db, collectionName):
        try:    
            return db.create_collection(collectionName, capped=True, size=100000)
        except CollectionInvalid:
            print(db[collectionName].options())
            if db[collectionName].options()['capped']:
                return db[collectionName]
            else:
                db.drop_collection(collectionName);
                return db.create_collection(collectionName, capped=True, size=100000)
            
def enqueue(msg, database, collectionName):
    if msg == None or database == None or collectionName == None :
        return None
    
    db = getDBHandler(database)
    collection = getCollectionHandler(db, collectionName)
    objId = collection.insert({"log": msg})
    return objId


def dequeue(database, collectionName):
    if database == None or collectionName == None :
        return None

    db = getDBHandler(database)
    collection = getCollectionHandler(db, collectionName)
    
    cursor = collection.find({})
    try:
        while cursor.alive:
            if next(cursor) != None:
                print(next(cursor)['log'])
        
                
    except StopIteration:
        return 'Empty queue'

    return 'complete'
            
        
    
    

