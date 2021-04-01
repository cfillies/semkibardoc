# import spacy
import pymongo
import json


uri = "mongodb+srv://semtation:SemTalk3!@cluster0.pumvg.mongodb.net/kibardoc?retryWrites=true&w=majority" 

# uri = "mongodb://semtalk-cosmos-mongo:XM09lEM9ptbh8o1cHDOQnpgjJ4nZ19Hm1BvdnKTubsizIZJeqGlE56n8BZwDkuJEhTsyHweVEH8T0adJkm50bQ==@semtalk-cosmos-mongo.documents.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb"
# uri = "mongodb://localhost:27017"
myclient = pymongo.MongoClient(uri)
myclient._topology_settings

mydb = myclient["kibardoc"]
collist = mydb.list_collection_names()

