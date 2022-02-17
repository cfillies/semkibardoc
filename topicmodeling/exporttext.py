import pymongo
from pymongo.collection import Collection
import requests
import os
# from metadata.support import logEntry
from pprint import pprint


def extract_text(file_path, tika_url):
    d = open(file_path, 'rb')
    r = requests.put(tika_url + "/tika", data=d)
    r.encoding = r.apparent_encoding
    result = r.text
    return result

import os
from dotenv import load_dotenv
load_dotenv()
uri = os.getenv("MONGO_CONNECTION")
# uri = "mongodb://localhost:27017"
# uri = "mongodb+srv://semtation:SemTalk3!@cluster2.kkbs7.mongodb.net/kibardoc"

myclient = pymongo.MongoClient(uri)
mydb = myclient["kibardoc"]

def tm_test6(docs: any, word: str):
    all_sentences = []
    i = 0
    for p in docs:
        all_sentences1 = []
        for p0 in p:
            # p2 = preprocess_string(p0)
            if len(p0)>0:
                # s = p0.split()
                # s0 = []
                # for w in s:
                #     if len(w) > 3:
                #         s0.append(w)
                # if len(s0)>0:
                #     all_sentences.append(s0)
                all_sentences1.append(p0)
            i += 1
    with open(word + "-" + i +'.txt', 'w', encoding='utf-8') as f:
        f.writelines(all_sentences1)
        
def extractDocs5(path: str, name: str):
    col = mydb[name]
    # texts = []
    for doc in col.find():
        if "text2" in doc:
            # texts.append(doc["text2"])
            cont = doc["text2"]
            if len(cont)>0:
                with open(path + "\\" + name + "-" + str(doc["docid"]) + '.txt', 'w', encoding='utf-8') as f:
                    f.writelines(cont)
    # tm_test6(texts, name)

# extractDocs5("C:\\Data\\test\\kibartmp\\sense2vec\\input", "koepenick")
# extractDocs5("C:\\Data\\test\\kibartmp\\sense2vec\\input", "pankow")
# extractDocs5("C:\\Data\\test\\kibartmp\\sense2vec\\input", "metadata")
# extractDocs5("C:\\Data\\test\\kibartmp\\sense2vec\\input", "lichtenberg")


def ignore(s: str):
    sl = s.lower()
    badlist = [".png", ".xml", ".js", ".css", ".htm", ".jfif",
               ".html", ".db", ".eml", ".mp3", ".mp4", ".jpeg",
               ".dwg", ".plt", ".gwi", ".gif", ".tif", ".c4d", ".ogv",
               ".wmf", ".jpg", ".svg", ".mov", ".dbf", ".prj", ".qpj"]
    return (sl in badlist)

def tikaTextOnly(path: str, opath: str,tika_url: str):
    i = 0
    m = 0
    for root, d_names, f_names in os.walk(path):
        for f in f_names:
            if not f.endswith(".xml"):
                i = i+1
                if i > 0:
                    ff = os.path.join(root, f)
                    ext = os.path.splitext(ff)[1]
                    if not ignore(ext):
                        txt = extract_text(ff, tika_url)
                        with open(opath + "\\" + f + '.txt', 'w', encoding='utf-8') as f:
                            pprint(txt, f)
                    else:
                        continue
                        # txt = ""s
                    print([i, " ", os.path.join(root, ff)])
                    # if not logEntry([i, " ", os.path.join(root, ff)]):
                    #     return
                    
# tikaTextOnly(r"C:\Data\test\kibartmp\docs",r"C:\Data\test\kibartmp\txt","http://localhost:9998")