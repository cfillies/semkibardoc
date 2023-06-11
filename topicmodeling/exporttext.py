# import pymongo
import requests
import os
from pprint import pprint
import spacy

# def saveMongoText2Folder(path: str, name: str, dbname: str, uri: str):
#     myclient = pymongo.MongoClient(uri)
#     mydb = myclient[dbname]
#     col = mydb[name]
#     # texts = []
#     for doc in col.find():
#         if "text2" in doc:
#             # texts.append(doc["text2"])
#             cont = doc["text2"]
#             if len(cont) > 0:
#                 with open(path + "\\" + name + "-" + str(doc["docid"]) + '.txt', 'w', encoding='utf-8') as f:
#                     f.writelines(cont)

# saveMongoText2Folder("C:\\Data\\test\\kibartmp\\sense2vec\\informatik\\input", "Informatik","kibardoc", "mongodb://localhost:27017")


# ------------TIKA-------------------------------------------

def extract_text(file_path, tika_url):
    d = open(file_path, 'rb')
    r = requests.put(tika_url + "/tika", data=d)
    r.encoding = r.apparent_encoding
    result = r.text
    return result


def ignorefiletypes(s: str):
    sl = s.lower()
    badlist = [".png", ".xml", ".js", ".css", ".htm", ".jfif",
               ".html", ".db", ".eml", ".mp3", ".mp4", ".jpeg",
               ".dwg", ".plt", ".gwi", ".gif", ".tif", ".c4d", ".ogv",
               ".wmf", ".jpg", ".svg", ".mov", ".dbf", ".prj", ".qpj"]
    return (sl in badlist)


def tika2txt(inputpath: str, outputpath: str, tika_url: str):
    if not os.path.exists(outputpath):
        os.mkdir(outputpath)
    i = 0
    for root, d_names, f_names in os.walk(inputpath):
        for f in f_names:
            if not f.endswith(".xml"):
                i = i+1
                if i > 0:
                    ff = os.path.join(root, f)
                    ext = os.path.splitext(ff)[1]
                    if not ignorefiletypes(ext):
                        txt = extract_text(ff, tika_url)
                        with open(outputpath + "\\" + f + '.txt', 'w', encoding='utf-8') as f:
                            pprint(txt, f)
                    else:
                        continue
                    print([i, " ", os.path.join(root, ff)])

# tika2txt(r"C:\\Users\\cfill\\OneDrive - Semtation GmbH\\Informatik Spektrum", r"C:\Data\test\kibartmp\txt","http://localhost:9998")


# -------------------LEMMATIZE-------------------

nlp = None
nlpcache = {}


def spacy_nlp(x: str):
    global nlpcache
    if x in nlpcache:
        return nlpcache[x]
    global nlp
    if nlp == None:
        loadCorpus("de_core_news_md")

    if len(nlpcache) > 30000:
        nlpcache = {}
    if len(x) > 1000000:
        x = x[0:999998]
    y = nlp(x)
    nlpcache[x] = y
    return y


stop_words = {"- ", ".", " , ", ", ", "$", "(", ")", "/", "II", "\n", "BZUG"}


def remove_stopwords(word: str) -> str:
    for c in stop_words:
        word = word.replace(c, " ")

    # word = word.replace("Berliner ", " ")
    # word = word.replace("GmbH", "")
    wl = spacy_nlp(word)
    tokens = [word for word in wl if not word.is_stop]
    return " ".join(str(x) for x in tokens), tokens


currentcorpus = ""


def loadCorpus(corpus: str):
    global currentcorpus
    global nlp
    if nlp == None or corpus != currentcorpus:
        nlp = spacy.load(corpus)
        currentcorpus = corpus
        nlp.add_pipe('sentencizer')
        nlp.disable_pipe("ner")
        nlp.disable_pipe("attribute_ruler")
        nlp.Defaults.stop_words |= stop_words
        global nlpcache
        nlpcache = {}


def remove_blanks(w: str) -> str:
    w = w.replace("       ", " ")
    w = w.replace("      ", " ")
    w = w.replace("     ", " ")
    w = w.replace("    ", " ")
    w = w.replace("   ", " ")
    w = w.replace("  ", " ")
    return w


def split_in_sentences(text: str) -> list[str]:
    doc = spacy_nlp(text)
    return [str(sent).strip() for sent in doc.sents]


def lemmatizetxt(filename: str) -> str:
    ntext = []
    with open(filename, encoding='utf-8') as f:
        d = f.read()
    d2 = d.replace(r'\\n', ' ')
    d2 = d2.replace(r'\n', ' ')
    d2 = d2.replace('\n', ' ')
    d2 = d2.replace("'", "")
    d2 = d2.replace(r'\r', ' ')
    d2 = d2.replace(r'\t', ' ')

    paragraphs: list[str] = split_in_sentences(d2)
    for p in paragraphs:
        pt: str = p
        if len(pt) > 3:
            ptext = ""
            # if pt in badlist:
            #     logEntry(["Badlist:", pt])
            #     continue
            # pt2: str = matchPattern(pt, pattern)
            # if pt2 != pt:
            #     pt = pt2

            # skip = False
            # for bp in bad_paragraphs:
            #     if pt.find(bp) > -1:
            #         skip = True
            #         continue
            # if skip:
            #     continue

            docp: any = spacy_nlp(pt)
            for wl in docp.noun_chunks:
                w: str = wl.lemma_
                if len(w) < 3:
                    continue
                w, ignore = remove_stopwords(w)
                w = w.strip()
                if len(w) == 0:
                    continue
                # if w in bad_phrases:
                #     continue
                if w.find("\\n") > -1:
                    w = w.replace(r"\n", " ")
                w = remove_blanks(w)
                ptext = ptext + w + " "
            if len(ptext) > 0:
                ntext.append(ptext)
    return ntext


def txt2lemma(inputpath: str, outputpath: str,
              corpus: str):
    if not os.path.exists(outputpath):
        os.mkdir(outputpath)

    global nlp
    if nlp == None:
        loadCorpus(corpus)
    i = 0
    for root, d_names, f_names in os.walk(inputpath):
        for f in f_names:
            if f.endswith(".txt"):
                i = i+1
                if i > 0:
                    ff = os.path.join(root, f)
                    txt = lemmatizetxt(ff)
                    with open(outputpath + "\\" + f + '.txt', 'w', encoding='utf-8') as f:
                        pprint(txt, f)
                    print([i, " ", os.path.join(root, ff)])


txt2lemma(r"C:\Data\test\kibartmp\txt",
          r"C:\Data\test\kibartmp\lem", "de_core_news_md")
