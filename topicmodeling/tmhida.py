import pymongo
import os
from dotenv import load_dotenv
load_dotenv()
uri = os.getenv("MONGO_CONNECTION")
# uri = "mongodb://localhost:27017"

myclient = pymongo.MongoClient(uri)
mydb = myclient["kibardoc"]

def extractHidaText(path: str, hidaname: str):
    hida_col = mydb[hidaname]
    for doc in hida_col.find():
        if "OBJ-Dok-Nr" in doc:
            id = doc["OBJ-Dok-Nr"]
            textfile = open(path + "\\" + id + "_file.txt", "w", encoding='utf-8')
            if "Listentext" in doc:
                textfile.write(doc["Listentext"] + "\n")
            if "K-Begründung" in doc:
                textfile.write(doc["K-Begründung"])            
            textfile.close()
# extractHidaText("C:\\Data\\test\\KIbarDok\\hida", "hida")       

def extractMetaText(path: str, metaname: str):
    col = mydb[metaname]
    for doc in col.find():
            id: str = doc["docid"]
            textfile = open(path + "\\" + str(id) + "_file.txt", "w", encoding='utf-8')
            if "text" in doc:
                textfile.write(doc["text"] + "\n")
            textfile.close()

extractMetaText("C:\\Data\\test\\KIbarDok\\txt3", "metadata")       
 