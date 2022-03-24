from numpy import number
from pymongo.collection import Collection

import requests
import os
from metadata.support import logEntry


def extract_text(file_path, tika_url):
    d = open(file_path, 'rb')
    r = requests.put(tika_url + "/tika", data=d)
    r.encoding = r.apparent_encoding
    result = r.text
    return result


def extract_meta(file_path, tika_url):
    file_name = str.split(file_path, '\\')[-1]
    response = requests.put(tika_url + "/meta", data=open(file_path,
                            'rb'),  headers={"Accept": "application/json"})
    try:
        result = response.json()
    except:
        result = {}
    result['file_name'] = file_name
    return result


def ignore(s: str):
    sl = s.lower()
    badlist = [".png", ".xml", ".js", ".css", ".htm", ".jfif",
               ".html", ".db", ".eml", ".mp3", ".mp4", ".jpeg",
               ".dwg", ".plt", ".gwi", ".gif", ".tif", ".c4d", ".ogv",
               ".wmf", ".jpg", ".svg", ".mov", ".dbf", ".prj", ".qpj"]
    return (sl in badlist)


def tikaText(district: str, path: str, col: Collection, 
             tika_url: str, startindex: number, deleteall: bool):
    i = 0
    i = startindex
    m = 0
    if deleteall:
        col.delete_many({})
    for root, d_names, f_names in os.walk(path):
        for f in f_names:
            if not f.endswith(".xml"):
                i = i+1
                if i > 0:
                    ff = os.path.join(root, f)
                    ext = os.path.splitext(ff)[1]
                    if not ignore(ext):
                        txt = extract_text(ff, tika_url)
                    else:
                        continue
                        # txt = ""
                    if not logEntry([i, " ", os.path.join(root, ff)]):
                        return
                    # met = extract_meta(ff, tika_url)
                    met = {}
                    try:
                        res = col.find_one_and_update({"file": f, "ext": ext, "path": root},
                                                      {"$set": {"meta": met, "text": txt, "district": district}})
                        if res == None:
                            # this is only needed if new documents are added:
                            # m = col.find().sort({"docid":-1}).limit(1)+1
                            m += 1
                            col.insert_one(
                                {"docid": m, "district": district, "file": f, "ext": ext, "path": root, "meta": met, "text": txt})
                    except:
                        logEntry(["TIKA Problem: ", ff])
                        pass
