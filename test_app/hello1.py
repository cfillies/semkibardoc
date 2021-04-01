# import spacy
import pymongo
import os



# uri = "mongodb+srv://semtation:SemTalk3!@cluster0.pumvg.mongodb.net/kibardoc?retryWrites=true&w=majority" 

uri = "mongodb://localhost:27017"
myclient = pymongo.MongoClient(uri)
myclient._topology_settings

mydb = myclient["kibardoc"]
collist = mydb.list_collection_names()

