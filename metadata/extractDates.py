from pymongo.collection import Collection
from extractDate import getDates


def convertDates(dates):
    """
    Reformats a list of datetime object to a list of string dates of dd/mm/YYYY format.

    :param dates: A list of datetime objects
    :return: A list of reformatted string dates, or a list containing a single empty string
    """
    date_strings = []
    for date in dates:
        if date.year > 1950:
            date_strings.append(date.strftime('%d/%m/%Y'))
            
    if not date_strings:
        date_strings = ['']
    
    return date_strings

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
                print(i, " ", doc["file"], dates)
                col.update_one({"_id": doc["_id"]}, { "$set": {"dates": dates}})
