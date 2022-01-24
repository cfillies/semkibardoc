from pymongo.collection import Collection
from .extractDate import getDates
from metadata.support import logEntry


def convertDates(dateslist):
    dtConvert = []
    for dl in dateslist:
        if dl.year > 1950:
            dtConvert.append(dl.strftime('%d/%m/%Y'))
            
    if dtConvert == []:
        dtConvert = ['']
    
    return dtConvert

def findDates(col: Collection):
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
        if  i > 0  and lt>10:
            dates = getDates(text)
            if len(dates)>0:
                dates = convertDates(dates)
                logEntry([i, " ", doc["file"], dates])
                col.update_one({"_id": doc["_id"]}, { "$set": {"dates": dates}})
