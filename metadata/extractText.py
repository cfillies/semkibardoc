import requests
from requests.api import request
import os
from pymongo.collection import Collection

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


def extractText(path: str, col: Collection, tika_url: str):
    i = 0
    col.delete_many({})
    for root, d_names, f_names in os.walk(path):
        for f in f_names:
            if not f.endswith(".xml"):
                i = i+1
                if i > 0:
                    ff = os.path.join(root, f)
                    print(i, " ", os.path.join(root, ff))
                    ext = os.path.splitext(ff)[1]
                    txt = extract_text(ff, tika_url)
                    met = extract_meta(ff, tika_url)
                    try:
                        col.insert_one(
                            {"file": f, "ext": ext, "path": root, "meta": met, "text": txt})
                    except:
                        pass
