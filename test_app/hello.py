from flask import Flask, json,Response
import pymongo
import os

myapp = Flask(__name__)

@myapp.route("/")
def hello():
    return "Hello Flask, on Azure App Service for Linux"

@myapp.route("/foo")
def foo():
    uri = os.getenv("MONGO_CONNECTION")
    myclient = pymongo.MongoClient(uri)
    myclient._topology_settings
    mydb = myclient["kibardoc"]
    collist = mydb.list_collection_names()
    vi = {}
    if "vorhaben_inv" in collist:
        vorhabeninv_col = mydb["vorhaben_inv"]
        vorhabeninv = vorhabeninv_col.find()
        for v in vorhabeninv:
            print(v["intents"])
            print(v["words"])
            for int in v["intents"]:
                vi[int] = v["intents"][int]

    # f = { "foo": "Hello Flask, on Azure App Service for Linux" }
    json_string = json.dumps(vi,ensure_ascii = False)
    #creating a Response object to set the content type and the encoding
    response = Response(json_string,content_type="application/json; charset=utf-8" )
    return response
