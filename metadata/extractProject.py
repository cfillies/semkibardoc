from pymongo.collection import Collection
from metadata.support import logEntry

def getProject(text: str):
    vorhaben_bezeichnung = "Vorhaben:"
    start_vorhaben = text.find(vorhaben_bezeichnung)
    delimit = '\n'

    if start_vorhaben == -1:
        vorhaben_bezeichnung = "Maßnahme (Kurzbeschreibung):"
        start_vorhaben = text.find(vorhaben_bezeichnung)
        delimit = '\t'
        if start_vorhaben == -1:                    
            vorhaben_bezeichnung = "Denkmalschutzrechtliche Genehmigung zum Bauvorhaben:"
            start_vorhaben = text.find(vorhaben_bezeichnung)
            delimit = '\n'
            if start_vorhaben == -1:     
                return '', delimit

    vorhaben = ''

    index_vorhaben = start_vorhaben + len(vorhaben_bezeichnung) + 1            
    delimLine = 0
    while len(vorhaben) <= 1:
        vorhaben = text[index_vorhaben:].split(delimit)[delimLine].replace('\n','')
        delimLine += 1         
        
    return vorhaben.strip(), delimit  

def findProject(col: Collection):
    dlist = []
    for doc in col.find():
        dlist.append(doc)
    i = 0
    dlist = []
    for doc in col.find():
        dlist.append(doc)

    for doc in dlist:
        i = i+1
        text = doc["text"]
        lt = len(text)
        if  i > 0:
            topic, sep = getProject(text)
            if len(topic)>0:
                if not logEntry(["Vorhaben: ", i, " " , doc["file"], topic]):
                    return
                col.update_one({"_id": doc["_id"]}, { "$set": {"vorhaben": topic}})
            else:
                col.update_one({"_id": doc["_id"]}, { "$set": {"vorhaben": "Kein Vorhaben gefunden"}})

