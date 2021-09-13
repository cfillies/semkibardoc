# import spacy
import certifi
import json
import os
from pathlib import Path
import pymongo
from pymongo.collection import Collection
import random
from dotenv import load_dotenv

import metadata
from metadata.extractText import extract_contents
from metadata.support import initSupport
from metadata.extractAddress import findAddresses
from metadata.findMonuments import findMonuments
from metadata.findDocType import findDocType
from metadata.extractDates import findDates
from metadata.extractProject import findProject
from metadata.extractIntents import extractintents


# from tmtest import tm_test, tm_test2


def color_generator(number_of_colors):
    color = ["#" + ''.join([random.choice('0123456789ABCDEF') for _ in range(6)])
             for _ in range(number_of_colors)]
    return color


def loadArrayCollection(database_, filename: str, colname: str):
    """
    Replaces a collection `colname` of `database_` with the contents of `filename`.
    """
    col: Collection = database_[colname]
    with open(filename, encoding='utf-8') as f:
        items = json.loads(f.read())
    col.delete_many({})
    col.insert_many(items)


def loadDictCollection(database_, filename: str, colname: str):
    """
    Replaces a collection `colname` of `database_` with a single item of the contents of `filename`.
    """
    col: Collection = database_[colname]
    with open(filename, encoding='utf-8') as f:
        item = json.loads(f.read())
    col.delete_many({})
    col.insert_one(item)


def patchHida(database_, filename: str, hidaname: str):
    """
    Takes a local hida json file and adds it to the mongoDB "hida" collection.

    Removes periods from each AdresseDict entry if present (why?)
    """
    with open(filename, encoding='utf-8') as f:
        hida0: dict = json.loads(f.read())
    monuments = []
    for hid in hida0:
        monument = hida0[hid]
        # if "K-Begründung" in monument:
        #     del monument["K-Begründung"]
        if "AdresseDict" in monument:
            adict = monument["AdresseDict"]
            keys = [x for x in adict]
            for s in keys:
                if "." in s:
                    str2 = s.replace(".", "")
                    adict[str2] = adict[s]
                    del adict[s]
                    continue
        monuments.append(monument)
    hida_col = database_[hidaname]
    hida_col.delete_many({})
    hida_col.insert_many(monuments)


def patchResolved(database_, resolvedname: str, filename: str, hidaname: str):
    hida_col = database_[hidaname]
    resolved_col = database_[resolvedname]
    with open(filename, encoding='utf-8') as f:
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
                                        #             hida[hidaid]= { "hidaid": hidaid,
                                        #                             "treffer": objnr["treffer"]}
                                        #     else:
                                        #             hida[hidaid]= { "hidaid": hidaobjl,
                                        #                             "treffer": objnr["treffer"]}
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
        # print(resolved)


def projectMetaDataHida(database_, metadataname: str, hidaname: str):
    hida_col = database_[hidaname]
    metadata_col = database_[metadataname]
    for doc in metadata_col.find():
        if "hidas" in doc:
            hida = {}
            sachbegriff = set([])
            denkmalart = set([])
            denkmalname = set([])
            for hidaid in doc["hidas"]:
                hidaobj = hida_col.find_one(
                    {"OBJ-Dok-Nr": hidaid})
                if not hidaobj:
                    hidaobj = hida_col.find_one(
                        {"Teil-Obj-Dok-Nr": hidaid})
                if "Denkmalname" in hidaobj:
                    s = hidaobj["Denkmalname"]
                    denkmalname.update(s)

                if "Denkmalart" in hidaobj:
                    s: str = hidaobj["Denkmalart"]
                    denkmalart.add(s)

                sachbegriffh = hidaobj["Sachbegriff"]
                sachbegriff.update(sachbegriffh)

                hida[hidaid] = hidaobj
            metadata_col.update_one(
                {"_id": doc["_id"]}, {
                    "$set": {"hida": hida,
                             "Sachbegriff": list(sachbegriff),
                             "Denkmalart": list(denkmalart),
                             "Denkmalname": list(denkmalname)}
                })


def setMetaDataDistrict(database_, metadataname: str, district: str):
    metadata_col = database_[metadataname]
    for doc in metadata_col.find():
        if not "district" in doc:
            metadata_col.update_one(
                {"_id": doc["_id"]}, {
                    "$set": {"district": district}
                })


def patchDir(database_, resolvedname: str, folders: str, path: str):
    folders_col = database_[folders]
    resolved_col = database_[resolvedname]
    for folder in folders_col.find():
        for file in folder["files"]:
            dir = folder["dir"]
            dir = dir.replace(path, "")
            f = file
            if f.endswith(".doc"):
                f = f.replace(".doc", ".docx")
            if f.endswith(".docx"):
                print(dir, f)
                resolved_col.update_many(
                    {"file": f}, {"$set": {"dir": dir}})


def patchKeywords(database_, resolvedname: str, topicsname: str):
    topics_col = database_[topicsname]
    resolved_col = database_[resolvedname]
    for topic in topics_col.find():
        # print(topic["file"])
        hidas = []
        sachbegriff = []
        denkmalart = []
        denkmalname = []
        if "hida" in topic:
            for hida0 in topic["hida"]:
                hidas.append(hida0)
                # ????? weder hidas noch die attributaggregation wird weiter verwendet....
                sachbegriff += hida0["Sachbegriff"]
                denkmalart += hida0["Denkmalart"]
                denkmalname += hida0["Denkmalname"]

        for theme in topic["keywords"]:
            resolved_col.update_many(
                {"file": topic["file"]}, {"$set": {
                    theme: topic["keywords"][theme]
                }})
        # resolved_col.update_many(
        #     {"file": topic["file"]}, {"$set": {
        #         "html": topic["html"]
        #     }})


def projectMetaDataKeywords(database_, metadataname: str):
    col = database_[metadataname]
    for doc in col.find():
        if "topic" in doc:
            topic = doc["topic"]
            for theme in topic["keywords"]:
                col.update_many(
                    {"_id": doc["_id"]}, {"$set": {
                        theme: topic["keywords"][theme]
                    }})
        # resolved_col.update_many(
        #     {"file": topic["file"]}, {"$set": {
        #         "html": topic["html"]
        #     }})


def unprojectMetaDataKeywords(database_, metadataname: str):
    col = database_[metadataname]
    for doc in col.find():
        if "topic" in doc:
            topic = doc["topic"]
            for theme in topic["keywords"]:
                col.update_one({"_id": doc["_id"]}, {"$unset": {theme: None}})


def patchText(database_, resolvedname: str, textname: str):
    text_col = database_[textname]
    resolved_col = database_[resolvedname]
    for text in text_col.find():
        f = text["file"]
        t = text["text"]
        t = t.replace('\n', ' ')
        t = t.replace('\u2002', ' ')
        print(text["file"])
        resolved_col.update_many(
            {"file": f}, {"$set": {
                "text": t
            }})


def projectHida(database_, resolvedname: str):
    resolved_col = database_[resolvedname]
    for reso0 in resolved_col.find():
        print(reso0["file"])
        hidas = []
        sachbegriff = []
        denkmalart = []
        denkmalname = []
        if "hida" in reso0:
            for hida0 in reso0["hida"]:
                hidas.append(hida0)
                sachbegriff += reso0["hida"][reso0]["Sachbegriff"]
                denkmalart.append(reso0["hida"][reso0]["Denkmalart"])
                denkmalname += reso0["hida"][reso0]["Denkmalname"]
            resolved_col.update_one(
                {"file": reso0["file"]}, {
                    "$set": {"hidas": hidas, "Sachbegriff": list(set(sachbegriff)),
                             "Denkmalart": list(set(denkmalart)),
                             "Denkmalname": list(set(denkmalname))}
                })


def patchVorhaben(database_, resolvedname: str):
    resolved_col = database_[resolvedname]
    for reso1 in resolved_col.find():
        if "vorhaben" in reso1 and len(reso1["vorhaben"]) == 1 and reso1["vorhaben"][0] \
                == 'Errichtung einer Mega-Light-Werbeanlage':
            print(reso1["file"])
            resolved_col.update_one(
                {"file": reso1["file"]}, {
                    "$set": {"vorhaben": []}
                })


def patchCategories(database_, words: str, categoriesname: str):
    categories = []
    if words in database_.list_collection_names():
        vorhabeninv_col = database_[words]
        vorhabeninv = vorhabeninv_col.find()
        for v in vorhabeninv:
            for wor in v["words"]:
                if len(v["words"][wor]) == 0:
                    categories.append(wor)
    catcolors = {}
    color = color_generator(len(categories))
    for i in range(len(categories)):
        catcolors[categories[i]] = {
            "color": color[i], "label": categories[i].upper()}

    cat_col = database_[categoriesname]
    cat_col.delete_many({})
    cat_col.insert_one(catcolors)


def loadEmbddings(database_, filename: str, colname: str):
    col: Collection = database_[colname]
    items: any = []
    with open(filename, encoding='utf-8') as f:
        mlist = json.loads(f.read())
        for m in mlist:
            items.append({"word": m, "match": mlist[m], "correct": True})
    col.delete_many({})
    col.insert_many(items)


def loadNoMatches(database_, filename: str, colname: str):
    col: Collection = database_[colname]
    items: any = []
    with open(filename, encoding='utf-8') as f:
        mlist = json.loads(f.read())
        for m in mlist:
            items.append({"word": m, "count": mlist[m]})
    col.delete_many({})
    col.insert_many(items)


def patchInvTaxo(database_, resolvedname: str, invtaxo: str):
    resolved_col = database_[resolvedname]
    resol = resolved_col.find()
    for reso2 in resol:
        invtaxo_col = database_[invtaxo]
        sblist = []
        if "Sachbegriff" in reso2:
            sblist = reso2["Sachbegriff"]
        if len(sblist) > 0:
            sl = sblist
            for sb in sblist:
                for plist in invtaxo_col.find({"name": sb}):
                    for pa in plist["parents"]:
                        if (pa != "ARCHITEKTUR" and pa != "FUNKTION" and pa != "BAUAUFGABE"
                                and pa not in sl):
                            sl.append(pa)
            resolved_col.update_one({"_id": reso2["_id"]}, {
                "$set": {"Sachbegriff": sl}})


def projectHidaInvTaxo(database_, hidaname: str, invtaxo: str):
    hida_col = database_[hidaname]
    invtaxo_col = database_[invtaxo]
    hidal = hida_col.find()
    for hida in hidal:
        invtaxo_col = database_["invtaxo"]
        sblist = hida["Sachbegriff"]
        if len(sblist) > 0:
            sl = sblist
            for sb in sblist:
                for plist in invtaxo_col.find({"name": sb}):
                    for pa in plist["parents"]:
                        if (pa != "ARCHITEKTUR" and pa != "FUNKTION" and pa != "BAUAUFGABE"
                                and pa not in sl):
                            sl.append(pa)
            hida_col.update_one({"_id": hida["_id"]}, {
                "$set": {"Sachbegriff": sl}})


def mongo_export(database_,
                 ispattern=False, ishida=False, isresolved=False,
                 ismetadatahida=False,
                 isfolders=False, isfolders_rel=False, isbadlist=False,
                 isvorhaben=False, isvorhaben_inv=False,
                 istaxo=False, istopics=False,
                 ispatch_dir=False, iskeywords=False,
                 ismetadatakeywords=False,
                 ismetadatanokeywords=False,
                 isupdatehida=False, isupdatevorhaben=False,
                 istext=False, isupdatetext=False,
                 iscategories=False,
                 isemblist=False, isnoemblist=False,
                 isinvtaxo=False, isupdatetaxo=False,
                 isupdatehidataxo=False):
    metadata = "metadata"
    hida = "hida"
    cwd = Path().cwd()

    if ispattern:
        loadArrayCollection(database_, cwd / "static/pattern.json", "pattern")
    if ishida:
        patchHida(database_, cwd / "static/hida.json", hida)
    if isresolved:
        patchResolved(database_, metadata, cwd / "resolved.json", hida)
    if ismetadatahida:
        projectMetaDataHida(database_, metadata, hida)
    if isfolders:
        loadArrayCollection(database_, cwd / "files.json", "folders")
    if isbadlist:
        loadArrayCollection(database_, cwd / "static/badlist.json", "badlist")
    if isvorhaben:
        loadArrayCollection(database_, cwd / "static/vorhaben.json", "vorhaben")
    if isvorhaben_inv:
        loadDictCollection(database_, cwd / "static/vorhaben_inv.json", "vorhaben_inv")
    if istaxo:
        loadArrayCollection(database_, cwd / "static/taxo.json", "taxo")
    if istopics:
        loadArrayCollection(database_, cwd / "topics3a.json", "topics")
    if ispatch_dir or isresolved:
        patchDir(database_, metadata, "folders", r"C:\Data\test\KIbarDok")
    if isresolved or istopics or iskeywords:
        patchKeywords(database_, metadata, "topics")
    if ismetadatakeywords:
        projectMetaDataKeywords(database_, metadata)
    if ismetadatanokeywords:
        unprojectMetaDataKeywords(database_, metadata)
    # if istext:
    #     loadArrayCollection(r"..\static\text3.json", "text")
    # if isresolved or isupdatetext:
    #     patchText("resolved", "text")
    if isresolved or isupdatehida:
        projectHida(database_, metadata)
    if isresolved or isupdatevorhaben:
        patchVorhaben(database_, metadata)
    if iscategories or isvorhaben_inv:
        patchCategories(database_, cwd / "static/vorhaben_inv", "categories")
    if isemblist:
        loadEmbddings(database_, cwd / "static/all_matches.json", "emblist")
    if isnoemblist:
        loadNoMatches(database_, cwd / "static/no_matches.json", "noemblist")
    if isinvtaxo:
        loadArrayCollection(database_, cwd / "static/taxo_inv.json", "invtaxo")
    if isresolved or isupdatetaxo or ismetadatahida:
        patchInvTaxo(database_, metadata, "invtaxo")
    if ishida or isupdatehidataxo:
        projectHidaInvTaxo(database_, "hida", "invtaxo")


def mongo_export_folder_structure(database_, toplvl_datafolder_name, collection_name):
    cwd = Path().cwd()
    loadArrayCollection(database_,
                        cwd / f"static/folder_struc_{toplvl_datafolder_name}.json",
                        collection_name)


def prepare_database(database_):
    """ Uploads all required collections to the `database_`. """

    collist = database_.list_collection_names()
    required_collections = ['istaxo', 'isinvtaxo', 'isvorhaben', 'isvorhaben_inv',
                            'ispattern', 'isbadlist']
    required_collections = {col: (False if col[2:] in collist else True)
                            for col in required_collections}
    mongo_export(database_, **required_collections)

    if "hida" not in collist:
        mongo_export(database_, ishida=True)
        mongo_export(database_, isupdatehidataxo=True)


def extract_metadata(database_, data_dir_, tika_url="http://localhost:9998", district_='Treptow'):
    hida: Collection = database_["hida"]
    support: Collection = database_["support"]
    metadata_: Collection = database_["metadata"]
    initSupport(support, hida)

    for filep in metadata.extractText.get_all_files_in_dir(data_dir_):
        txt, met = extract_contents(filep, tika_url)
        metadata_.find_one_and_update(
            filter={"path": str(filep.relative_to(data_dir)),
                    "file": filep.stem, "ext": filep.suffix},
            update={"$set": {"district": district_, "meta": met, "text": txt}},
            upsert=True)

    findAddresses(metadata_, support, "de")
    findMonuments(metadata_, hida, support, "de")
    mongo_export(database, ismetadatahida=True)
    findDocType(metadata_)
    findDates(metadata_)
    findProject(metadata_)

    vorhabeninv_col = database_["vorhaben_inv"]
    pattern_col = database_["pattern"]
    badlist_col = database_["badlist"]
    all_col = database_["emblist"]
    no_col = database_["noemblist"]
    extractintents(metadata_, vorhabeninv_col, pattern_col, badlist_col, all_col, no_col)
    mongo_export(database, ismetadatakeywords=True)


if __name__ == '__main__':
    # load_dotenv()
    # Username and password are saved as environment variables (may need to restart IDE)
    # uri = "mongodb://localhost:27017"
    DB_USERNAME = os.getenv('KIBARDOC_USERNAME')
    DB_PASSWORD = os.getenv('KIBARDOC_PASSWORD')
    # mongoDB URI with Cluster set up by Jonas
    uri = (f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@kibardoc0.9hxcv.mongodb.net/admin"
           f"?retryWrites=true")
    # mongoDB URI with Cluster set up by Christian
    # uri = ("mongodb+srv://klsuser:Kb.JHQ-.HrCs6Fw@cluster0.7qi8s.mongodb.net/test"
    #        "?authSource=admin&replicaSet=atlas-o1jpuq-shard-0&readPreference=primary"
    #        "&appname=MongoDB%20Compass&ssl=true")

    mongo_client = pymongo.MongoClient(uri, tlsCAFile=certifi.where())
    # myclient._topology_settings

    database = mongo_client["kibardoc"]

    data_folder = 'Test'
    data_dir = Path(r'C:\Users\koenij\Projekte\KIbarDok\Daten') / data_folder
    mongo_export_folder_structure(database,
                                  toplvl_datafolder_name=data_folder,
                                  collection_name=f"folders_{data_folder}")
    prepare_database(database)
    extract_metadata(database, data_dir, district_=data_folder)
    # setMetaDataDistrict("metadata", "Treptow")
    # mongo_export(ismetadatanokeywords=True)

    # mongo_export(database, ishida=True)
    # mongo_export(database, ispattern=True, ishida=True, isresolved=True, isfolders=True,
    #              isbadlist=True, isvorhaben=True, isvorhaben_inv=True, istaxo=True,
    #              istopics=True, ispatch_dir=True, iskeywords=True)
    # mongo_export(database, iskeywords=True)
    # mongo_export(database, isresolved=True)
    # mongo_export(database, istext=True)
    # mongo_export(database, isupdatetext=True)
    # mongo_export(database, istopics=True)
    # mongo_export(database, isfolders=True, isbadlist=True, iscategories=True, isvorhaben=True)
    # mongo_export(database, isupdatevorhaben=True)
    # mongo_export(database, isvorhaben_inv=True)
    # mongo_export(database, isemblist=True)
    # mongo_export(database, isnoemblist=True)
    # mongo_export(database, isinvtaxo=True)
    # mongo_export(database, isupdatetaxo=True)
    # mongo_export(database, isupdatehidataxo=True)
    # mongo_export(database, iscategories=True)
    # mongo_export(database, ispatch_dir=True)
