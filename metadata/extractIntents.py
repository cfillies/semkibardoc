# from typing import List, Dict
from pymongo.collection import Collection
from metadata.extractTopics import _extractIntents, prepareWords, preparePattern, getSpacyVectors, extractText
from metadata.support import logEntry

def prepareList(vorhabeninv_col: Collection, pattern_col: Collection, badlist_col: Collection):
    # if "vorhaben_inv" in collist:
    # vorhabeninv_col = mydb["vorhaben_inv"]
    vorhabeninv: dict = vorhabeninv_col.find_one()
    wvi: dict[str, list[str]] = {}
    wvi = vorhabeninv["words"]
    # v: Dict[str,List[str]] = vorhabeninv["words"]
    # for wor in v:
    #     wvi[wor] = v[wor]

    words, wordlist = prepareWords(wvi)
    categories: list[str] = []
    # if "categories" in collist:
    #     cat_col = mydb["categories"]
    #     catobj = cat_col.find_one()
    #     for cat in catobj:
    #         if cat != '_id':
    #             categories.append(cat)

    patternjs: list[str] = []
    # if "pattern" in collist:
    # pattern_col = mydb["pattern"]
    pattern = pattern_col.find()
    for v in pattern:
        patternjs.append(v["paragraph"])
    plist: list[dict[str, str]] = preparePattern(patternjs)

    badlistjs: list[str] = []
    # if "badlist" in collist:
    #     badlist_col = mydb["badlist"]
    badlist = badlist_col.find()
    for v in badlist:
        badlistjs.append(v["paragraph"])

    return words, wordlist, categories, plist, badlistjs


def extractTopics(col: Collection, pattern_topic: str, 
                  word_dimension: dict[str, dict[str, any]],
                  word_supers: dict[str, list[str]],
                  pattern: list[str], badlist: list[str],
                  bparagraphs: bool,
                  dist: float,
                  corpus: str):
    tlist: list[dict] = []
    all_matches: dict[str, dict] = {}
    no_matches: dict[str, int] = {}
    i = 0
    dlist = []
    for doc in col.find():
        dlist.append(doc)

    for doc in dlist:
        i = i+1
        text = doc["text"]
        lt = len(text)
        if i > 0 and lt > 10:
            t: dict = _extractIntents(doc["file"], pattern_topic, 
                                      word_dimension, 
                                      word_supers, 
                                      pattern, badlist, 
                                      bparagraphs, text, 
                                      all_matches, no_matches,
                                      dist,
                                      corpus)
            if t != {}:
                if not logEntry(["Topics: ", i, " ", doc["file"], t["keywords"]]):
                    return
                col.update_one({"_id": doc["_id"]}, {"$set": {"topic": t}})
    return tlist, all_matches, no_matches


def extractintents(metadata: Collection, vorhabeninv_col: Collection, pattern_col: Collection,
                   badlist_col: Collection, all_col: Collection, no_col: Collection,
                   dist: float,
                   corpus: str):

    words, wordlist, categories, plist, badlistjs = prepareList(
        vorhabeninv_col, pattern_col, badlist_col)

    bparagraph = True

    # metadata = mydb["metadata"]
    res, all_matches, no_matches = extractTopics(
        metadata,
        "Vorhaben:", 
        words, wordlist, 
        plist, badlistjs, bparagraph, dist, corpus)

    # topics_col = mydb["topics"]
    # topics_col.delete_many({})
    # topics_col.insert_many(res)

    # all_col = mydb["emblist"]
    # all_col.delete_many({})
    # all_col.insert_one(all_matches)

    # no_col = mydb["noemblist"]
    # no_col.delete_many({})
    # no_col.insert_one(no_matches)

    return res, all_matches, no_matches


def extractTexts(col: Collection, vorhabeninv_col: Collection, 
                 pattern_col: Collection, 
                 badlist_col: Collection, 
                 metadataname: str,
                 corpus: str):
    words, wordlist, categories, plist, badlistjs = prepareList(
        vorhabeninv_col, pattern_col, badlist_col)
    #  wird nur benutzt um texte ohne textbausteine auszuleiten

    i = 0
    dlist = []
    for doc in col.find():
        dlist.append(doc)

    for doc in dlist:
        i = i+1
        text = doc["text"]
        lt = len(text)
        if i > 0 and lt > 10:
            t = extractText(plist, badlistjs, text, corpus)
            logEntry([str(i) + ".txt", " ", doc["file"]])
            col.update_one(
                {"_id": doc["_id"]}, {
                    "$set": {"text2": t}
                })
