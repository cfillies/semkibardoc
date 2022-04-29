from pymongo.collection import Collection
# import metadata.extractDocType as eVorgang
# efindVorgang = eVorgang.findVorgang
# efindNotVorgang = eVorgang.findNotVorgang

from metadata.extractDocType import allPositiveMatches, matchFileName, allPositiveDocTypes, setDocTypePattern
from metadata.support import logEntry

def postDocTypeProcessingMatch(match: dict):
    # key: str = next(iter(match))
    # val: dict = match[key]
    # keys= val.keys()
    # val: List[str] = match[key]
    keys = list(match.keys())
    keyscnt = len(keys)

    if keyscnt > 1:
        # Anfrage=question, Nachforderung=claim can contain information about Versagung or Genehmgigung. However, it is still a question or a claim.
        if keyscnt > 1 and ('Anfrage' in keys or 'Nachforderung' in keys):
            for key in keys:
                if key != 'Anfrage' and key != 'Nachforderung' and key in match:
                    del match[key]
        if 'Eingang' in keys and keyscnt > 1:
            for key in list(keys):
                if key != 'Eingang' and key in match:
                    del match[key]
        # Anhörung includes also Versagung but not reverse
        if keyscnt == 2 and 'Anhörung' in keys and 'Versagung' in keys:
            del match['Versagung']
        if keyscnt == 2 and 'Genehmigung' in keys and 'Versagung' in keys:
            del match['Genehmigung']
        if keyscnt == 3 and 'Genehmigung' in keys and 'Versagung' in keys and 'Anhörung' in keys:
            del match['Genehmigung']
            del match['Versagung']
        # Bauverfahren is relatively uncertain. It appiers mostly with Genehmigung.Genehmigung is more certain
        if 'Bauverfahren' in match:
            del match['Bauverfahren']
    return match


def findDocType(col: Collection, doctypes: Collection):
    dlist = []
    for doc in col.find():
        dlist.append(doc)
    i = 0

    # dlist=dlist[10000:]

    doc_pattern = {}
    for dt in doctypes.find():
        doc_pattern[dt["name"]] = { "file": dt["file"], "pos": dt["pos"], "neg": dt["neg"]}
    setDocTypePattern(doc_pattern)    

    for doc in dlist:
        i = i+1

        match: dict = {}
        considerDocName: bool = True
        fname: str = doc["file"].lower()
        # Begin - Analyse the file name
        if considerDocName and fname.count(' ') < 5:
            # if 'anfr' in fname:
            #     match = {'Anfrage': ['Dateiname']}
            # elif (('anhö' in fname) or ('anhoe' in fname) or ('anhorung' in fname)):
            #     match = {'Anhörung': ['Dateiname']}
            # elif ('versag' in fname) or ('versg' in fname) or ('negativ' in fname):
            #     match = {'Versagung': ['Dateiname']}
            # elif ('geneh' in fname):
            #     match = {'Genehmigung': ['Dateiname']}
            # elif 'zustim' in fname:
            #     match = {'Genehmigung': ['Dateiname']}
            # elif (('stellung' in fname) or ('stelln' in fname)):
            #     match = {'Stellungnahme': ['Dateiname']}
            # elif 'kein denkmal' in fname:
            #     match = {'Kein Denkmal': ['Dateiname']}
        
            match = matchFileName(fname)
            if len(match)>0:
                dtype = next(iter(match))
                col.update_one({"_id": doc["_id"]}, {
                               "$set": {"doctype": dtype, "match": match}})
                continue

        # End - Analyse the file name
        text = doc["text"]
        lt = len(text)
        if i > 0:
            if lt < 10:
                col.update_one({"_id": doc["_id"]}, {
                               "$set": {"doctype": "< 10 Zeichen"}})
            else:
                if lt > 10000:
                    dtype = "zu groß: "
                    if not logEntry(["Dokumenttyp: ",i, " ", doc["file"], dtype, lt]):
                        return
                    col.update_one({"_id": doc["_id"]}, {
                                   "$set": {"doctype": "> 10000 Zeichen"}})
                    continue
                if len(match) == 0:
                    # match = efindVorgang(text).all()
                    match = allPositiveMatches(text)
                    # match = allPositiveDocTypes(text)
                    if match:
                        match = postDocTypeProcessingMatch(match)
                    else:
                        pass
                        # noMatch =  allNegativeMatches

                        # noMatch = efindNotVorgang(text).negativAllList()
                        # nomatchval = noMatch[next(iter(noMatch))]
                        # print(doc["file"],'noMatch: ', noMatch)
                        # kl = list (noMatch.keys())
                        # if len(kl) > 0 and len(noMatch[kl[0]])>0:
                        #     if 'Nicht-Genehmigung' in kl:
                        #         match={'Versagung': noMatch['Nicht-Genehmigung']}
                if match:
                    dtype = next(iter(match))
                    if not logEntry(["Dokumenttyp: ", i, " ", doc["file"], dtype]):
                        return
                else:
                    dtype = "Kein Dokumenttyp gefunden"
                    if not logEntry(["Dokumenttyp: ", i, " ", doc["file"], dtype]):
                        return
                col.update_one({"_id": doc["_id"]}, {
                               "$set": {"doctype": dtype, "match": match}})
