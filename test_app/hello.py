from flask import Flask, json, Response, request
import pymongo
import os

myapp = Flask(__name__)
uri = os.getenv("MONGO_CONNECTION")
myclient = pymongo.MongoClient(uri)
mydb = myclient["kibardoc"]


@myapp.route("/")
def hello():
    return "Hello Flask, This is the KiBarDok Service. Try intents, words"


@myapp.route("/hida")
def allhida():
    # print(request.args)
    query = request.args
    collist = mydb.list_collection_names()
    vi = []
    if "hida" in collist:
        hida_col = mydb["hida"]
        hida = hida_col.find(query)
        for v in hida:
            if 'OBJ-Dok-Nr' in v:
                vi.append(v['OBJ-Dok-Nr'])
    # json_string = json.dumps(vi,ensure_ascii = False)
    response = Response(
        str(vi), content_type="application/json; charset=utf-8")
    return response


@myapp.route("/hida/<id>")
def hida(id=""):
    collist = mydb.list_collection_names()
    vi = {}
    if "hida" in collist:
        hida_col = mydb["hida"]
        hida = hida_col.find({'OBJ-Dok-Nr': id})
        for v in hida:
            response = Response(
                str(v), content_type="application/json; charset=utf-8")
            return response
    json_string = json.dumps(vi, ensure_ascii=False)
    response = Response(
        json_string, content_type="application/json; charset=utf-8")
    return response


@myapp.route("/intents")
def allintents():
    collist = mydb.list_collection_names()
    vi = {}
    if "vorhaben_inv" in collist:
        vorhabeninv_col = mydb["vorhaben_inv"]
        vorhabeninv = vorhabeninv_col.find()
        for v in vorhabeninv:
            for intent in v["intents"]:
                vi[intent] = v["intents"][intent]
    json_string = json.dumps(vi, ensure_ascii=False)
    response = Response(
        json_string, content_type="application/json; charset=utf-8")
    return response


@myapp.route("/intents/<intent>")
def intents(intent=""):
    uri = os.getenv("MONGO_CONNECTION")
    myclient = pymongo.MongoClient(uri)
    mydb = myclient["kibardoc"]
    collist = mydb.list_collection_names()
    vi = {}
    if "vorhaben_inv" in collist:
        vorhabeninv_col = mydb["vorhaben_inv"]
        vorhabeninv = vorhabeninv_col.find()
        for v in vorhabeninv:
            if intent:
                if intent in v["intents"]:
                    vi = v["intents"][intent]
    json_string = json.dumps(vi, ensure_ascii=False)
    response = Response(
        json_string, content_type="application/json; charset=utf-8")
    return response


@myapp.route("/words")
def allwords():
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
            for wor in v["words"]:
                vi[wor] = v["words"][wor]
    json_string = json.dumps(vi, ensure_ascii=False)
    response = Response(
        json_string, content_type="application/json; charset=utf-8")
    return response


@myapp.route("/words/<word>")
def words(word=""):
    collist = mydb.list_collection_names()
    vi = {}
    if "vorhaben_inv" in collist:
        vorhabeninv_col = mydb["vorhaben_inv"]
        vorhabeninv = vorhabeninv_col.find()
        for v in vorhabeninv:
            if word:
                if word in v["words"]:
                    vi = v["words"][word]
    json_string = json.dumps(vi, ensure_ascii=False)
    response = Response(
        json_string, content_type="application/json; charset=utf-8")
    return response
