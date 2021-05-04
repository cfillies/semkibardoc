# import spacy
import pymongo
import json
# import os
from intent import extractTopicsAndPlaces, prepareWords, preparePattern
# import asyncio
# from bson.objectid import ObjectId
import random 
#
uri = "mongodb+srv://semtation:SemTalk3!@cluster0.pumvg.mongodb.net/kibardoc?retryWrites=true&w=majority"
# uri = "mongodb://localhost:27017"

myclient = pymongo.MongoClient(uri)
myclient._topology_settings

mydb = myclient["kibardoc"]
collist = mydb.list_collection_names()
pattern_col = mydb["pattern"]
hida_col = mydb["hida"]
resolved_col = mydb["resolved"]
folders_col = mydb["folders"]
topics_col = mydb["topics"]
text_col = mydb["text"]
cat_col = mydb["categories"]

def color_generator(number_of_colors):
        color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
                 for i in range(number_of_colors)]
        return color

def mongoExport(ispattern=False, ishida=False, isresolved=False,
                isfolders=False, isbadlist=False,
                isvorhaben=False, isvorhabeninv=False,
                istaxo=False, istopics=False,
                ispatch_dir=False, iskeywords=False,
                isupdatehida=False, isupdatevorhaben=False,
                istext=False, isupdatetext=False,
                iscategories=False):
    if ispattern:
        with open("pattern.json", encoding='utf-8') as f:
            pattern = json.loads(f.read())
        pattern_col.delete_many({})
        pattern_col.insert_many(pattern)

    if ishida:
        with open("hida.json", encoding='utf-8') as f:
            hida = json.loads(f.read())
            monuments = []
            for hid in hida:
                monument = hida[hid]
                # if "K-Begründung" in monument:
                #     del monument["K-Begründung"]
                if "AdresseDict" in monument:
                    adict = monument["AdresseDict"]
                    keys = [x for x in adict]
                    for str in keys:
                        if "." in str:
                            str2 = str.replace(".", "")
                            adict[str2] = adict[str]
                            del adict[str]
                            continue
                monuments.append(monument)
            hida_col.delete_many({})
            hida_col.insert_many(monuments)

    if isresolved:
        with open("resolved.json", encoding='utf-8') as f:
            resolvedjs = json.loads(f.read())
            resolved = []
            for directory in resolvedjs:
                el = resolvedjs[directory]
                if "datei" in el:
                    filesjs = el["datei"]
                    for file in filesjs:
                        # print(directory, file)
                        obj = filesjs[file]
                        vorhaben = obj["vorhaben"]
                        if len(vorhaben) == 1:
                            if vorhaben[0] == "Errichtung einer Mega-Light-Werbeanlage":
                                vorhaben = []
                        vorgang = obj["vorgang"]
                        objnr = obj["objnr"]
                        hida = {}
                        if "method" in objnr:
                            meth = objnr["method"]
                            if len(meth) > 0:
                                for o in objnr:
                                    if o != "method" and o != "behoerde" and o != "hausnummer":
                                        if meth == 'inhalt_direct' and o == "treffer":
                                            treflist = objnr["treffer"][meth]
                                            tref = treflist[0]
                                            hidaid = tref[0]
                                            hidaobj = hida_col.find_one(
                                                {"OBJ-Dok-Nr": hidaid})
                                            listentext = hidaobj["Listentext"]
                                            denkmalname = hidaobj["Denkmalname"]
                                            denkmalart = hidaobj["Denkmalart"]
                                            sachbegriff = hidaobj["Sachbegriff"]
                                            hida[hidaid] = {
                                                "hidaid": hidaid,
                                                "Listentext": listentext,
                                                "Denkmalart": denkmalart,
                                                "Denkmalname": denkmalname,
                                                "Sachbegriff": sachbegriff}
                                            #     if isinstance(hidaobjl, list):
                                            #         for hidaid in hidaobjl:
                                            #             hida[hidaid]= { "hidaid": hidaid, "treffer": objnr["treffer"]}
                                            #     else:
                                            #             hida[hidaid]= { "hidaid": hidaobjl, "treffer": objnr["treffer"]}
                                        else:
                                            denkmal = objnr[o]
                                            # print(denkmal)
                                            for hidaobj in denkmal["treffer"][meth]:
                                                hidaid = hidaobj[0]
                                                hidaobj = hida_col.find_one(
                                                    {"OBJ-Dok-Nr": hidaid})
                                                listentext = hidaobj["Listentext"]
                                                denkmalname = hidaobj["Denkmalname"]
                                                denkmalart = hidaobj["Denkmalart"]
                                                sachbegriff = hidaobj["Sachbegriff"]
                                                hida[hidaid] = {
                                                    "hidaid": hidaid,
                                                    "Listentext": listentext,
                                                    "Denkmalart": denkmalart,
                                                    "Denkmalname": denkmalname,
                                                    "Sachbegriff": sachbegriff}

                        resolved.append({"file": file, "dir": directory,
                                         "vorgang": vorgang,
                                         "vorhaben": vorhaben,
                                         "hida": hida,
                                         "obj": obj})
            resolved_col.delete_many({})
            resolved_col.insert_many(resolved)
            print(resolved)

    if isfolders:
        with open("files.json", encoding='utf-8') as f:
            fileslist = json.loads(f.read())
            folders_col.insert_many(fileslist)

    if isbadlist:
        badlist_col = mydb["badlist"]
        with open("badlist.json", encoding='utf-8') as f:
            fileslist = json.loads(f.read())
            badlist_col.delete_many({})
            badlist_col.insert_many(fileslist)

    if isvorhaben:
        vorhaben_col = mydb["vorhaben"]
        with open("vorhaben.json", encoding='utf-8') as f:
            vorhaben = json.loads(f.read())
            vorhaben_col.delete_many({})
            vorhaben_col.insert_many(vorhaben)

    if isvorhabeninv:
        vorhabeninv_col = mydb["vorhaben_inv"]
        with open("vorhaben_inv.json", encoding='utf-8') as f:
            vorhabeninv = json.loads(f.read())
            vorhabeninv_col.delete_many({})
            vorhabeninv_col.insert_one(vorhabeninv)

    if istaxo:
        taxo_col = mydb["taxo"]
        with open("taxo.json", encoding='utf-8') as f:
            topics = json.loads(f.read())
            taxo_col.delete_many({})
            taxo_col.insert_many(topics)

    if istopics:
        with open("topics3a.json", encoding='utf-8') as f:
            topics = json.loads(f.read())
            topics_col.delete_many({})
            topics_col.insert_many(topics)

    if ispatch_dir or isresolved:
        for folder in folders_col.find():
            for file in folder["files"]:
                dir = folder["dir"]
                dir = dir.replace(r"C:\Data\test\KIbarDok", "")
                f = file
                if f.endswith(".doc"):
                    f = f.replace(".doc", ".docx")
                if f.endswith(".docx"):
                    print(dir, f)
                    resolved_col.update_many(
                        {"file": f}, {"$set": {"dir": dir}})

    if isresolved or istopics or iskeywords:
        for topic in topics_col.find():
            print(topic["file"])
            hidas = []
            sachbegriff = []
            denkmalart = []
            denkmalname = []
            if "hida" in topic:
                for hida in topic["hida"]:
                    hidas.append(hida)
                    sachbegriff += hida["Sachbegriff"]
                    denkmalart += hida["Denkmalart"]
                    denkmalname += hida["Denkmalname"]

            for theme in topic["keywords"]:
                resolved_col.update_many(
                    {"file": topic["file"]}, {"$set": {
                        theme: topic["keywords"][theme]
                    }})
            # resolved_col.update_many(
            #     {"file": topic["file"]}, {"$set": {
            #         "html": topic["html"]
            #     }})

    if istext:
        with open("text3.json", encoding='utf-8') as f:
            textlist = json.loads(f.read())
            text_col.insert_many(textlist)

    if isresolved or isupdatetext:
        for text in text_col.find():
            f = text["file"]
            t = text["text"]
            print(text["file"])
            resolved_col.update_many(
                {"file": f}, {"$set": {
                    "text": t
                }})

    if isresolved or isupdatehida:
        for reso in resolved_col.find():
            print(reso["file"])
            hidas = []
            sachbegriff = []
            denkmalart = []
            denkmalname = []
            if "hida" in reso:
                for hida in reso["hida"]:
                    hidas.append(hida)
                    sachbegriff += reso["hida"][hida]["Sachbegriff"]
                    denkmalart.append(reso["hida"][hida]["Denkmalart"])
                    denkmalname += reso["hida"][hida]["Denkmalname"]
                resolved_col.update_one(
                    {"file": reso["file"]}, {
                        "$set": {"hidas": hidas, "Sachbegriff": list(set(sachbegriff)), 
                                  "Denkmalart": list(set(denkmalart)), 
                                  "Denkmalname": list(set(denkmalname))}
                    })

    if isresolved or isupdatevorhaben:
        for reso in resolved_col.find():
            if "vorhaben" in reso and len(reso["vorhaben"]) == 1 and reso["vorhaben"][0] == 'Errichtung einer Mega-Light-Werbeanlage':
                print(reso["file"])
                resolved_col.update_one(
                    {"file": reso["file"]}, {
                        "$set": {"vorhaben": []}
                    })

    if isvorhabeninv:
        vorhabeninv_col = mydb["vorhaben_inv"]
        with open("vorhaben_inv.json", encoding='utf-8') as f:
            vorhabeninv = json.loads(f.read())
    
    if iscategories or isvorhabeninv:
        categories=[]
        if "vorhaben_inv" in collist:
            vorhabeninv_col = mydb["vorhaben_inv"]
            vorhabeninv = vorhabeninv_col.find()
            for v in vorhabeninv:
                for wor in v["words"]:
                    if len(v["words"][wor])==0:
                        categories.append(wor);
        catcolors = {}
        color = color_generator(len(categories))
        for i in range(len(categories)):
            catcolors[categories[i]] = { "color": color[i], "label": categories[i].upper()} 
                
        cat_col = mydb["categories"]
        cat_col.delete_many({})
        cat_col.insert_one(catcolors)

# mongoExport(ispattern=True,ishida=True,isresolved=True,isfolders=True,isbadlist=True,isvorhaben=True,
                #  isvorhabeninv=True, istaxo=True,istopics=True, ispatch_dir=True, iskeywords=True)
# mongoExport(iskeywords=True)
# mongoExport(isresolved=True)
# mongoExport(isupdatetext=True)
# mongoExport(istopics=True)
# mongoExport(iscategories=True)
mongoExport(isupdatevorhaben=True)


def extractintents():

    wvi = {}

    if "vorhaben_inv" in collist:
        vorhabeninv_col = mydb["vorhaben_inv"]
        vorhabeninv = vorhabeninv_col.find()
        for v in vorhabeninv:
            for wor in v["words"]:
                wvi[wor] = v["words"][wor]
    words, wordlist = prepareWords(wvi)

    categories=[]

    if "categories" in collist:
        cat_col = mydb["categories"]
        catobj = cat_col.find_one()
        for cat in catobj:
            if cat != '_id':
                categories.append(cat)

    patternjs = []
    if "pattern" in collist:
        pattern_col = mydb["pattern"]
        pattern = pattern_col.find()
        for v in pattern:
            patternjs.append({"paragraph": v["paragraph"]})
    plist = preparePattern(patternjs)

    badlistjs = []
    if "badlist" in collist:
        badlist_col = mydb["badlist"]
        badlist = badlist_col.find()
        for v in badlist:
            badlistjs.append({"paragraph": v["paragraph"]})

    bparagraph = True

    res = extractTopicsAndPlaces(
        words, wordlist, categories, plist, badlistjs, bparagraph, "")
    # topics_col = mydb["topics"]
    # topics_col.delete_many({})
    # topics_col.insert_many(res)
    return res

# extractintents()

# taxo_col = mydb["taxo"]
# for taxo in taxo_col.find({'topic': 'Klostermauer'}):
#     print(taxo)

# hida_col = mydb["hida"]
# for mon in hida_col.find({"Bezirk": "Treptow-Köpenick"}, {"OBJ-Dok-Nr": 1, "Denkmalname": 1, "Sachbegriff": 1}):
#     if len(mon["Denkmalname"]) > 0:
#         if "Sachbegriff" in mon:
#             print(mon["OBJ-Dok-Nr"], mon["Denkmalname"][0], mon["Sachbegriff"])
#         else:
#             print(mon["OBJ-Dok-Nr"], mon["Denkmalname"][0])
