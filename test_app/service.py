import os
# from numpy import number
# from typing import Dict
from flask import Flask, Response, request, render_template, url_for, flash, redirect, jsonify
from flask.globals import session
from flask_cors import CORS
import pymongo
import json

# import numpy as np
import pandas as pd
from io import BytesIO
from flask import send_file
import re

import datetime
from werkzeug.exceptions import abort
from bson.objectid import ObjectId

from export2mongodb import cloneCollection, cloneDatabase
from export2mongodb import extractMetaData, projectMetaData, initMongoFromStaticFiles
from export2mongodb import insert_many, insert_one
from markupsafe import Markup
from typing import List, Dict, Any
from dotenv import load_dotenv
import hashlib

from intent import extractIntents, prepareWords, preparePattern, displacyText, displacyTextHTML
from intent import matchingConcepts, getSimilarity, hasVector, loadCorpus, extractLemmata
from intent import getSpacyVectors, mostSimilar, getSimilarityMatrix
from metadata.support import getLog, resetLog, cancel_execution

# from metadata import extractDocType
import threading
#  https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3
myapp = Flask(__name__, static_folder='client')
myapp.config['SECRET_KEY'] = 'your secret key'
CORS(myapp)

load_dotenv()
uri = os.getenv("MONGO_CONNECTION")
lib = os.getenv("DOCUMENT_URL")
tab = os.getenv("DOCUMENT_TABLE")

spacy_default_corpus = os.getenv("SPACY_CORPUS")
if spacy_default_corpus == None:
    spacy_default_corpus = "de_core_news_md"


# uri = "mongodb://localhost:27017"
# uri =  os.getenv("MONGO_CONNECTION_ATLAS")
# uri =  os.getenv("MONGO_CONNECTION_KLS")
# uri =  os.getenv("MONGO_CONNECTION_AZURE")


# metadatatable = "resolved"
metadatatable = "metadata"
# metadatatable = "lichtenberg"
# metadatatable = "koepenick"
# metadatatable = "treptow"
# metadatatable = "pankow"

uri = "mongodb+srv://semtation:SemTalk3!@cluster2.kkbs7.mongodb.net/kibardoc"
if True and (metadatatable == "pankow" or metadatatable == "lichtenberg"):
    uri = os.getenv("MONGO_CONNECTION_PANKOW")

if uri == None:
    uri = "mongodb://localhost:27017"
# uri = "mongodb://localhost:27017"

myclient = pymongo.MongoClient(uri,
                               maxPoolSize=50,
                               unicode_decode_error_handler='ignore')

mydb = myclient["kibardoc"]
collist = mydb.list_collection_names()

if tab:
    metadatatable = tab


sha256 = hashlib.sha256()
sha256.update(str('123').encode("utf-8"))
hashPass = sha256.hexdigest()
usertable = "user"
usercol = mydb[usertable]
user = usercol.find_one({'username': "knowlogy"})
if user == None:
    usercol.insert_one({'username': "knowlogy", "password": hashPass})


@myapp.route("/createuser", methods=['GET', 'POST'])
def createuser(username: str, password: str):
    if 'username' in session:
        if request.method == 'POST':
            sha256 = hashlib.sha256()
            sha256.update(str(password).encode("utf-8"))
            hashPass = sha256.hexdigest()
            usertable = "user"
            usercol = mydb[usertable]
            user = usercol.find_one({'username': username})
            if user == None:
                usercol.insert_one(
                    {'username': "knowlogy", "password": hashPass})


@myapp.route("/services", methods=['GET'])
def index():
    return render_template('services.html')

# Statics


@myapp.route('/', methods=['GET'])
def root():
    if 'username' in session:
        # s = ""
        # for arg in request.args:
        #     s = s + arg + "=" + request.args[arg] + "&"
        # if len(s) > 0:
        #     return myapp.send_static_file('index.html' + "?" + s[:len(s)])
        # else:
        return myapp.send_static_file('index.html')
    else:
        return redirect(url_for('login'))


@myapp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form["username"]
        password = request.form["password"]
        sha256 = hashlib.sha256()
        sha256.update(str(password).encode("utf-8"))
        hashPass = sha256.hexdigest()
        user = usercol.find_one({'username': uname, "password": hashPass})
        if user != None:
            session['username'] = uname
        return redirect(url_for('root'))

    return render_template('login.html')
    # return myapp.send_static_file('login.html')


@myapp.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
    # return myapp.send_static_file('login.html')


@myapp.route('/hidafacet', methods=['GET'])
def hidafacet():
    if user == None:
        return redirect(url_for('login'))
    return myapp.send_static_file('hida.html')


@myapp.route('/<path:path>', methods=['GET'])
def static_proxy(path):
    # send_static_file will guess the correct MIME type
    return myapp.send_static_file(path)


@myapp.route("/selectmetadata", methods=(['GET']))
def selectmetadata():
    if user == None:
        return redirect(url_for('login'))
    query = request.args
    if "collection" in query:
        global metadatatable
        metadatatable = query["collection"]
        global myclient
        global mydb
        global collist
        if True and (metadatatable == "pankow" or metadatatable == "lichtenberg"):
            uri = os.getenv("MONGO_CONNECTION_PANKOW")
            myclient = pymongo.MongoClient(uri,
                                           maxPoolSize=50,
                                           unicode_decode_error_handler='ignore')
            mydb = myclient["kibardoc"]
            collist = mydb.list_collection_names()
        else:
            # uri = "mongodb://localhost:27017"
            uri = os.getenv("MONGO_CONNECTION")
            uri = "mongodb+srv://semtation:SemTalk3!@cluster2.kkbs7.mongodb.net/kibardoc"
            myclient = pymongo.MongoClient(uri,
                                           maxPoolSize=50,
                                           unicode_decode_error_handler='ignore')
            mydb = myclient["kibardoc"]
            collist = mydb.list_collection_names()

        return myapp.send_static_file('index.html')
    return "OK"


_allcategories: List[str] = []
_colors: Dict[str, str] = {}


def allcategories_and_colors():
    global _allcategories
    if _allcategories != []:
        return _allcategories, _colors
    vi: List[str] = []
    cat_col = mydb["categories"]
    catobj: Dict[str, Dict[str, str]] = cat_col.find_one()
    for cat in catobj:
        if cat != '_id':
            vi.append(cat)
            caobj = catobj[cat]
            _colors[caobj["label"]] = caobj["color"]

    # if "vorhaben_inv" in collist:
    #     vorhabeninv_col = mydb["vorhaben_inv"]
    #     vorhabeninv = vorhabeninv_col.find()
    #     for v in vorhabeninv:
    #         for wor in v["words"]:
    #             if len(v["words"][wor]) == 0:
    #                 vi.append(wor)

    _allcategories = vi
    return vi, _colors


@ myapp.route("/categories", methods=['GET'])
def categories():
    vi, col = allcategories_and_colors()
    json_string = json.dumps(vi, ensure_ascii=False)
    response = Response(
        json_string, content_type="application/json; charset=utf-8")
    return response


@myapp.route("/documents", methods=['GET'])
def documents():
    if user == None:
        return redirect(url_for('login'))
    # print(request.args)
    query = request.args
    vi = []
    if metadatatable in collist:
        col = mydb[metadatatable]
        resolved = col.find(query)
        for v in resolved:
            v1 = {}
            # for a in v:
            #     if a != "_id" and a != "obj":
            #         v1[a] = v[a]
            # vi.append(v1)
            if "topic" in v:
                item: dict = v["topic"]
                if item != None:
                    vi.append(item)
    json_string = json.dumps(vi, ensure_ascii=False)
    response = Response(
        json_string, content_type="application/json; charset=utf-8")
    return response


@ myapp.route('/document/<docid>/edit', methods=['GET', 'POST'])
def editdocument(docid):
    if user == None:
        return redirect(url_for('login'))
    item = get_document(metadatatable, docid)
    if request.method == 'POST':
        qs = {}
        qs["qscomment"] = request.form['qscomment']
        qs["qsrelation"] = request.form["qsrelation"]
        qs["qsdoctype"] = request.form["qsdoctype"]
        if "qsobjnrInvalid" in request.form:
            qs["qsobjnrInvalid"] = True
        else:
            qs["qsobjnrInvalid"] = False
        qs["qsobjnummer"] = request.form["qsobjnummer"]
        qs["qsvorhaben"] = request.form["qsvorhaben"]
        qs["qscomment"] = request.form["qscomment"]
        col = mydb[metadatatable]
        col.update_one(
            {'docid': int(docid)}, {'$set': {'qs': qs}})
        return redirect(url_for('showdocument', docid=docid))
    else:
        comment = ""
        if "comment" in item:
            comment = item["comment"]
        vorhaben = ""
        if "vorhaben" in item:
            vorhaben = item["vorhaben"]
        p = item["path"].replace("C:\\Data\\test\\KIbarDok\\Treptow\\", "")
        p = p.replace("\\", "/")
        pdfurl = lib + p + "/" + item["file"]

        qs = {"docid": item["docid"],
              "qsdoctype": item["doctype"],
              "qsobjnrInvalid": False,
              "qsobjnummer": "",
              "qsvorhaben": vorhaben,
              "qscomment": comment
              }
        if "qs" in item:
            qs = item["qs"]
        qs["file"] = item["file"]
        qs["pdfurl"] = pdfurl
        do_monument = True
        if "qs" in item:
            if "qsrelation" in item["qs"] and not item["qs"]["qsrelation"] == "Denkmalschutz":
                do_monument = False

        qs["qsmonumentchecked"] = 'checked' if do_monument else ''
        qs["qsdistancechecked"] = '' if do_monument else 'checked'
        # , debug=myapp.debug
        return render_template('edit_document.html', **qs)


@myapp.route("/showdocuments", methods=['GET'])
def showdocuments():
    if user == None:
        return redirect(url_for('login'))
    vi = []
    if metadatatable in collist:
        col = mydb[metadatatable]
        query = request.args
        metadata = col.find(query)
        for v in metadata:
            v1 = {}
            v1["docid"] = v["docid"]
            v1["file"] = v["file"]
            v1["path"] = v["path"]
            if not "comment" in v:
                v1["comment"] = ""
            else:
                v1["comment"] = v["comment"]
            if "doctype" in v:
                v1["doctype"] = v["doctype"]
            else:
                v1["doctype"] = ""

            if "hida" in v:
                v1["hida"] = v["hida"]
            else:
                v1["hida"] = []

            if "vorhaben" in v:
                v1["vorhaben"] = v["vorhaben"]
            else:
                v1["vorhaben"] = []
            vi.append(v1)
    return render_template('show_documents.html', documents=vi)


@myapp.route("/showdocument", methods=['GET'])
def showdocument():
    if user == None:
        return redirect(url_for('login'))
    if metadatatable in collist:

        catlist, colors = allcategories_and_colors()
        options = {"ents": catlist, "colors": colors}
        res_col = mydb[metadatatable]
        # list_col = mydb["topics"]
        query = request.args
        query1 = query.copy()
        query1["docid"] = int(query1["docid"])
        metadata = res_col.find(query1)
        for v in metadata:
            # item: Dict = list_col.find_one({"file": v["file"]})
            if not "comment" in v:
                v["comment"] = ""
            paragraphs: List[dict] = []
            kw = {}
            if "topic" in v:
                item: dict = v["topic"]
                if item != None:
                    for i in item["intents"]:
                        pt: str = i["paragraph"]
                        ents: List[Any] = i["entities"]
                        html: Markup = displacyText(pt, ents, options)
                        paragraphs.append({"html": html})
                for c in catlist:
                    if c in v:
                        kw[c] = v[c]
            v["keywords"] = kw
            return render_template('show_document.html', res=v, paragraphs=paragraphs)


@myapp.route("/hida", methods=['GET'])
def allhida():
    # print(request.args)
    query = request.args
    vi = []
    if "hida" in collist:
        hida_col = mydb["hida"]
        hida = hida_col.find(query)
        for v in hida:
            v1 = {}
            if 'OBJ-Dok-Nr' in v:
                v1['OBJ-Dok-Nr'] = v['OBJ-Dok-Nr']
            if 'Teil-Obj-Dok-Nr' in v:
                v1['Teil-Obj-Dok-Nr'] = v['Teil-Obj-Dok-Nr']
            # for a in v:
            #     if a != "_id":
            #         v1[a]=v[a]
            # vi.append(v1)

            # mname=""
            if 'Listentext' in v:
                v1['Listentext'] = v['Listentext']
            if 'Denkmalname' in v:
                v1['Denkmalname'] = v['Denkmalname']
            if 'Sachbegriff' in v:
                v1['Sachbegriff'] = v['Sachbegriff']
            if 'Denkmalart' in v:
                v1['Denkmalart'] = v['Denkmalart']

            # elif 'Denkmalname' in v:
            #     mname= v['Denkmalname']
            # sb = []
            # if 'Sachbegriff' in v:
            #     sb= v['Sachbegriff']
            # if 'OBJ-Dok-Nr' in v:
            #     vi.append({ 'OBJ-Dok-Nr': v['OBJ-Dok-Nr'], 'Listentext': mname, 'Sachbegriff':sb})
            if 'OBJ-Dok-Nr' in v1:
                vi.append(v1)
            else:
                print(v)

    json_string = json.dumps(vi, ensure_ascii=False)
    response = Response(
        json_string, content_type="application/json; charset=utf-8")
    return response


@ myapp.route("/hida/<id>", methods=['GET'])
def hida(id=""):
    collist = mydb.list_collection_names()
    vi = {}
    if "hida" in collist:
        hida_col = mydb["hida"]
        hida = hida_col.find({'OBJ-Dok-Nr': id})
        # if hida.retrieved == 0:
        #     hida = hida_col.find({'Teil-Obj-Dok-Nr': id})
        for v in hida:
            response = Response(
                str(v), content_type="application/json; charset=utf-8")
            return response
        hida = hida_col.find({'Teil-Obj-Dok-Nr': id})
        for v in hida:
            response = Response(
                str(v), content_type="application/json; charset=utf-8")
            return response
    json_string = json.dumps(vi, ensure_ascii=False)
    response = Response(
        json_string, content_type="application/json; charset=utf-8")
    return response


@ myapp.route("/showhida/<id>", methods=['GET'])
def showhida(id=""):
    collist = mydb.list_collection_names()
    if "hida" in collist:
        hida_col = mydb["hida"]
        hida = hida_col.find({'OBJ-Dok-Nr': id})
        # if hida.retrieved == 0:
        #     hida = hida_col.find({'Teil-Obj-Dok-Nr': id})
        res = {}
        for v in hida:
            for at in v:
                if at != "_id" and at != "Objekt-Type":
                    va = v[at]
                    if isinstance(va, list):
                        va = ', '.join(va)
                    res[at] = va
            return render_template('show_monument.html', res=res, title="Denkmal")
        hida = hida_col.find({'Teil-Obj-Dok-Nr': id})
        for v in hida:
            for at in v:
                if at != "_id" and at != "Objekt-Type":
                    va = v[at]
                    if isinstance(va, list):
                        va = ', '.join(va)
                    res[at] = va
            return render_template('show_monument.html', res=res, title="Denkmal")


@ myapp.route("/monuments", methods=['GET'])
def monuments():
    vi = []
    if "hida" in collist:
        hida_col = mydb["hida"]
        query = request.args
        hida = hida_col.find(query)
        for v in hida:
            mname = ""
            if 'Listentext' in v:
                mname = v['Listentext']
            elif 'Denkmalname' in v:
                mname = v['Denkmalname']
            sb = []
            if 'Sachbegriff' in v:
                sb = v['Sachbegriff']
            if 'OBJ-Dok-Nr' in v:
                vi.append(
                    {'OBJ-Dok-Nr': v['OBJ-Dok-Nr'], 'Listentext': mname, 'Sachbegriff': sb})
    return render_template('show_monuments.html', monuments=vi)


@ myapp.route("/taxo", methods=['GET'])
def alltaxo():
    query = request.args
    collist = mydb.list_collection_names()
    vi = []
    if "taxo" in collist:
        taxo_col = mydb["taxo"]
        taxo = taxo_col.find(query)
        for v in taxo:
            v1 = {}
            for a in v:
                if a != "_id":
                    v1[a] = v[a]
            vi.append(v1)

    json_string = json.dumps(vi, ensure_ascii=False)
    response = Response(
        json_string, content_type="application/json; charset=utf-8")
    return response


@ myapp.route("/showtaxo", methods=['GET'])
def showtaxo():
    query = request.args
    vi = []
    if "taxo" in collist:
        taxo_col = mydb["taxo"]
        taxo = taxo_col.find(query)
        for v in taxo:
            vi.append(v)
    return render_template('show_taxo.html', taxo=vi, title="Sachbegriffe")


@ myapp.route("/taxoexcel", methods=['GET'])
def taxoexcel():
    query = request.args
    vi = []
    if "taxo" in collist:
        taxo_col = mydb["taxo"]
        taxo = taxo_col.find(query)
        for v in taxo:
            vi.append(v)
    return excel(vi, "taxo.xlsx", "Sheet1")


@ myapp.route("/intents", methods=['GET'])
def allintents():
    if user == None:
        return redirect(url_for('login'))
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


@ myapp.route("/intents/<intent>", methods=['GET'])
def intents(intent=""):
    if user == None:
        return redirect(url_for('login'))
    # uri = os.getenv("MONGO_CONNECTION")
    # myclient = pymongo.MongoClient(uri)
    # mydb = myclient["kibardoc"]
    # collist = mydb.list_collection_names()
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


@ myapp.route("/showintents", methods=['GET'])
def showintents():
    if user == None:
        return redirect(url_for('login'))
    vi = {}
    if "vorhaben_inv" in collist:
        vorhabeninv_col = mydb["vorhaben_inv"]
        vorhabeninv = vorhabeninv_col.find()
        for v in vorhabeninv:
            for intent in sorted(v["intents"]):
                vi[intent] = v["intents"][intent]
    return render_template('show_listdict.html', listdict=vi, title="Unterklassen", excel="intentssexcel")


@ myapp.route("/intentssexcel", methods=['GET'])
def intentssexcel():
    vi = []
    if "vorhaben_inv" in collist:
        vorhabeninv_col = mydb["vorhaben_inv"]
        vorhabeninv = vorhabeninv_col.find()
        for v in vorhabeninv:
            for intent in sorted(v["intents"]):
                v2 = [intent]
                v2.append(v["intents"][intent])
                vi.append(v2)
    return excel(vi, "intents.xlsx", "Sheet1")


@ myapp.route("/words", methods=['GET'])
def allwords():
    if user == None:
        return redirect(url_for('login'))
    query = request.args
    vi = {}
    if "vorhaben_inv" in collist:
        vorhabeninv_col = mydb["vorhaben_inv"]
        vorhabeninv = vorhabeninv_col.find(query)
        for v in vorhabeninv:
            for wor in v["words"]:
                vi[wor] = v["words"][wor]
    json_string = json.dumps(vi, ensure_ascii=False)
    response = Response(
        json_string, content_type="application/json; charset=utf-8")
    return response


@ myapp.route("/words/<word>", methods=['GET'])
def words(word=""):
    if user == None:
        return redirect(url_for('login'))
    collist = mydb.list_collection_names()
    vi = {}
    query = request.args
    if "vorhaben_inv" in collist:
        vorhabeninv_col = mydb["vorhaben_inv"]
        vorhabeninv = vorhabeninv_col.find(query)
        for v in vorhabeninv:
            if word:
                if word in v["words"]:
                    vi = v["words"][word]
    json_string = json.dumps(vi, ensure_ascii=False)
    response = Response(
        json_string, content_type="application/json; charset=utf-8")
    return response


@ myapp.route("/showwords", methods=['GET'])
def showwords():
    if user == None:
        return redirect(url_for('login'))
    vi = {}
    if "vorhaben_inv" in collist:
        vorhabeninv_col = mydb["vorhaben_inv"]
        vorhabeninv = vorhabeninv_col.find()
        for v in vorhabeninv:
            for wor in sorted(v["words"]):
                vi[wor] = v["words"][wor]
    return render_template('show_listdict.html', listdict=vi, title="Oberbegriffe", excel="wordsexcel")


@ myapp.route("/wordsexcel", methods=['GET'])
def wordsexcel():
    vi = []
    if "vorhaben_inv" in collist:
        vorhabeninv_col = mydb["vorhaben_inv"]
        vorhabeninv = vorhabeninv_col.find()
        for v in vorhabeninv:
            vl = v["words"]
            for wor in sorted(vl):
                # vi[wor] = v["words"][wor]
                v2 = [wor]
                v2.append(vl[wor])
                vi.append(v2)
    return excel(vi, "words.xlsx", "Sheet1")


def get_item(table: str, id: str):
    col = mydb[table]
    item = col.find_one({'_id': ObjectId(id)})
    if item is None:
        abort(404)
    return item


def get_document(table: str, docid: str):
    col = mydb[table]
    item = col.find_one({'docid': int(docid)})
    if item is None:
        abort(404)
    return item


@ myapp.route("/pattern", methods=['GET'])
def allpattern():
    if user == None:
        return redirect(url_for('login'))
    collist = mydb.list_collection_names()
    vi = []
    if "pattern" in collist:
        list_col = mydb["pattern"]
        list = list_col.find()
        for v in list:
            vi.append(v["paragraph"])
    json_string = json.dumps(vi, ensure_ascii=False)
    response = Response(
        json_string, content_type="application/json; charset=utf-8")
    return response


@ myapp.route('/pattern/<id>', methods=['GET'])
def pattern(id):
    if user == None:
        return redirect(url_for('login'))
    item = get_item("pattern", id)
    return render_template('show_item.html', item=item)


@ myapp.route("/showpattern", methods=['GET'])
def showpattern():
    if user == None:
        return redirect(url_for('login'))
    vi = []
    if "pattern" in collist:
        list_col = mydb["pattern"]
        list = list_col.find()
        for v in list:
            vi.append(v)
    return render_template('show_list.html', list=sorted(vi, key=lambda p: p['paragraph']), title="Textbausteine", table="editpatternlist")


@ myapp.route('/pattern/<id>/edit', methods=['GET', 'POST'])
def editpatternlist(id):
    if user == None:
        return redirect(url_for('login'))
    item = get_item("pattern", id)
    if request.method == 'POST':
        paragraph = request.form['paragraph']
        typ = request.form['type']
        col = mydb["pattern"]
        col.update_one(
            {'_id': ObjectId(id)}, {'$set': {'paragraph': paragraph, 'type': typ}})
        return redirect(url_for('showpattern'))
    collist = mydb.list_collection_names()
    vi = [{"name": ""}]
    if "doctypes" in collist:
        list_col = mydb["doctypes"]
    list = list_col.find()
    for v in list:
        v1 = {}
        for a in v:
            if a != "_id":
                v1[a] = v[a]
        vi.append(v1)
    return render_template('edit_item.html', item=item, types=vi, delete_item="deletepattern")


@ myapp.route('/pattern/<id>/delete', methods=['POST'])
def deletepattern(id):
    if user == None:
        return redirect(url_for('login'))
    # item = get_item("pattern", id)
    col = mydb["pattern"]
    col.remove({'_id': ObjectId(id)})
    flash('"{}" was successfully deleted!'.format('Item'))
    return redirect(url_for('showpattern'))


@ myapp.route("/doctypes", methods=['GET'])
def alldoctypes():
    if user == None:
        return redirect(url_for('login'))
    collist = mydb.list_collection_names()
    vi = []
    if "doctypes" in collist:
        list_col = mydb["doctypes"]
        list = list_col.find()
        for v in list:
            v1 = {}
            for a in v:
                if a != "_id":
                    v1[a] = v[a]
            vi.append(v1)
    json_string = json.dumps(vi, ensure_ascii=False)
    response = Response(
        json_string, content_type="application/json; charset=utf-8")
    return response


@ myapp.route("/showdoctypes", methods=['GET'])
def showdoctypes():
    if user == None:
        return redirect(url_for('login'))
    vi = []
    if "doctypes" in collist:
        list_col = mydb["doctypes"]
        list = list_col.find()
        for v in list:
            vi.append(v)
    return render_template('show_document_types.html', documents=vi, title="Dokumenttypen")


@ myapp.route("/badlist", methods=['GET'])
def allbadlist():
    if user == None:
        return redirect(url_for('login'))
    collist = mydb.list_collection_names()
    vi = []
    if "badlist" in collist:
        list_col = mydb["badlist"]
        list = list_col.find()
        for v in list:
            vi.append(v["paragraph"])
    json_string = json.dumps(vi, ensure_ascii=False)
    response = Response(
        json_string, content_type="application/json; charset=utf-8")
    return response


@ myapp.route("/showbadlist", methods=['GET'])
def showbadlist():
    if user == None:
        return redirect(url_for('login'))
    vi = []
    if "badlist" in collist:
        list_col = mydb["badlist"]
        list = list_col.find()
        for v in list:
            vi.append(v)
    return render_template('show_list.html', list=sorted(vi, key=lambda p: p['paragraph']), title="Badlist", table="editbadlist")


@ myapp.route('/badlist/<id>', methods=['GET'])
def badlist(id):
    if user == None:
        return redirect(url_for('login'))
    item = get_item("badlist", id)
    return render_template('show_item.html', item=item)


@ myapp.route('/badlist/<id>/edit', methods=['GET', 'POST'])
def editbadlist(id):
    if user == None:
        return redirect(url_for('login'))
    item = get_item("badlist", id)
    if request.method == 'POST':
        paragraph = request.form['paragraph']
        col = mydb["badlist"]
        col.update_one(
            {'_id': ObjectId(id)}, {'$set': {'paragraph': paragraph}})
        return redirect(url_for('showbadlist'))
    return render_template('edit_item.html', item=item, types=[], delete_item="deletebadlist")


@ myapp.route('/badlist/<id>/delete', methods=('POST',))
def deletebadlist(id):
    if user == None:
        return redirect(url_for('login'))
    # item = get_item("badlist", id)
    col = mydb["badlist"]
    col.remove({'_id': ObjectId(id)})
    flash('"{}" was successfully deleted!'.format('Item'))
    return redirect(url_for('showbadlist'))


@ myapp.route("/showemblist", methods=['GET'])
def showemblist():
    if user == None:
        return redirect(url_for('login'))
    vi = []
    if "emblist" in collist:
        list_col = mydb["emblist"]
        list = list_col.find_one()
        for v in list:
            if v != "_id":
                vi.append({"word": v, "match": list[v]})
    return render_template('show_emblist.html', list=vi, title="de_core_news_md", table="editemblist")


@ myapp.route('/emblist/<id>/edit', methods=['GET', 'POST'])
def editemblist(id):
    if user == None:
        return redirect(url_for('login'))
    # item = get_item("emblist", id)
    if request.method == 'POST':
        # paragraph = request.form['paragraph']
        # col = mydb["pattern"]
        # col.update_one(
        #     {'_id': ObjectId(id)}, {'$set': {'paragraph': paragraph}})
        return redirect(url_for('showemblist'))
    # return render_template('edit_embitem.html', item=item, delete_item="deleteemblist")
    return redirect(url_for('showemblist'))


@ myapp.route("/shownoemblist", methods=['GET'])
def shownoemblist():
    if user == None:
        return redirect(url_for('login'))
    vi = []
    if "noemblist" in collist:
        list_col = mydb["noemblist"]
        list1 = list_col.find_one()
        for v in list1:
            if v != "_id":
                vi.append({"word": v, "count": list1[v]})
    return render_template('show_noemblist.html', list=vi, title="Unmatched", table="editnoemblist")


@ myapp.route('/noemblist/<id>/edit', methods=['GET', 'POST'])
def editnoemblist(id):
    if user == None:
        return redirect(url_for('login'))

    # item = get_item("noemblist", id)
    if request.method == 'POST':
        # paragraph = request.form['paragraph']
        # col = mydb["pattern"]
        # col.update_one(
        #     {'_id': ObjectId(id)}, {'$set': {'paragraph': paragraph}})
        return redirect(url_for('shownoemblist'))
    # return render_template('edit_embitem.html', item=item, delete_item="deleteemblist")
    return redirect(url_for('shownoemblist'))


@ myapp.route("/keywords", methods=['GET'])
def keywords():
    if user == None:
        return redirect(url_for('login'))
    query = request.args
    collist: List = mydb.list_collection_names()
    vi: List[Dict[str, Any]] = []
    # if "topics" in collist:
    #     list_col = mydb["topics"]
    #     list = list_col.find(query)
    #     for v in list:
    #         vi.append({"file": v["file"], "path": v["path"],
    #                   "keywords": v["keywords"], "intents": v["intents"]})
    if metadatatable in collist:
        list_col = mydb[metadatatable]
        list = list_col.find(query)
        for v in list:
            kwor = []
            inte = []
            if "topic" in v:
                kwor = v["topic"]["keywords"]
                inte = v["topic"]["intents"]
            vi.append({"file": v["file"], "path": v["path"],
                      "keywords": kwor, "intents": inte})
    json_string = json.dumps(vi, ensure_ascii=False)
    response = Response(
        json_string, content_type="application/json; charset=utf-8")
    return response


@ myapp.route("/allshowkeywords", methods=['GET'])
def allshowkeywords():
    if user == None:
        return redirect(url_for('login'))
    query = request.args
    collist = mydb.list_collection_names()
    vi: List[Dict[str, Any]] = []
    # if "topics" in collist:
    #     list_col = mydb["topics"]
    #     list: List[Dict[str, Any]] = list_col.find(query)
    #     for v in list:
    #         vi.append(v)
    if metadatatable in collist:
        list_col = mydb[metadatatable]
        list = list_col.find(query)
        for v in list:
            kwor = []
            inte = []
            if "topic" in v:
                kwor = v["topic"]["keywords"]
                inte = v["topic"]["intents"]
            vi.append({"docid": v["docid"], "file": v["file"], "path": v["path"],
                      "keywords": kwor, "intents": inte})
    return render_template('show_documents_keywords.html', documents=vi, title="Schlagworte", table="show_keywords")


@ myapp.route("/showkeywords/<docid>", methods=['GET'])
def showkeywords(docid=""):
    if user == None:
        return redirect(url_for('login'))
    collist = mydb.list_collection_names()
    # if "topics" in collist:
    if metadatatable in collist:
        catlist, colors = allcategories_and_colors()
        options: dict[str, Any] = {"ents": catlist, "colors": colors}
        # item: dict = get_item("topics", id)
        # doc: dict = get_item(metadatatable, id)
        doc: dict = get_document(metadatatable, docid)
        paragraphs: List[Dict[str, Any]] = []
        res = {}
        res["file"] = doc["file"]
        if "place" in doc:
            res["place"] = doc["place"]
        else:
            res["place"] = []
        res["keywords"] = []

        if "topic" in doc:
            item = doc["topic"]
            res["keywords"] = item["keywords"]
            for i in item["intents"]:
                pt: str = i["paragraph"]
                ents: List[Any] = i["entities"]
                html: Markup = displacyText(pt, ents, options)
                paragraphs.append({"words:": i["words"], "html": html})
        return render_template('show_extraction.html', res=res, title="Schlagworte", paragraphs=paragraphs)


@ myapp.route('/create_extraction', methods=['GET', 'POST'])
def create_extraction():
    dist = 0.5
    corpus = spacy_default_corpus
    if request.method == 'POST':
        text = request.form['content']
        query = request.args
        bparagraph = True
        if "bparagraph" in query:
            bparagraph = query["bparagraph"]

        word_dimension, word_supers, categories, plist, badlistjs = prepareList({}, [
        ], [])

        res, all_matches, no_matches = extractIntents(
            word_dimension, word_supers, categories, plist, badlistjs, bparagraph,
            text, dist, corpus)
        if len(res) > 0:
            catlist, colors = allcategories_and_colors()
            options = {"ents": catlist, "colors": colors}
            item: dict = res
            paragraphs: list[dict[str, any]] = []
            for i in item["intents"]:
                pt: str = i["paragraph"]
                ents: list[any] = i["entities"]
                html: Markup = displacyText(pt, ents, options)
                paragraphs.append({"words:": i["words"], "html": html})
            return render_template('show_extraction.html', res=item,
                                   title="Keyword", paragraphs=paragraphs)
        else:
            return render_template('index.html')

    return render_template('create_extraction.html')

# #########################################
# Search


def _get_array_param(param: str) -> List[str]:
    if param == '':
        return []
    else:
        return param.split(",")


def _get_group_pipeline(group_by: str):
    return [
        {
            '$group': {
                '_id': '$' + group_by,
                'count': {'$sum': 1},
            }
        },
        {
            '$project': {
                '_id': 0,
                'value': '$_id',
                'count': 1,
            }
        },
        {
            '$sort': {'count': -1}
        },
        {
            '$limit': 6,
        }
    ]


def getmatch(args, catlist: List[str]) -> Dict[str, str]:
    match: Dict[str, Any] = {}
    for cat in catlist:
        catvals = _get_array_param(args.get(cat, ''))
        if catvals:
            match[cat] = {'$in': catvals}
    return match


def _get_facet_pipeline(facet, match):
    pipeline = []
    if match:
        if facet in match:
            matchc = match.copy()
            del matchc[facet]
        else:
            matchc = match
        pipeline = [
            {'$match': matchc}
        ] if match else []
    return pipeline + _get_group_pipeline(facet)


def _get_group_pipeline(group_by):
    return [
        {'$unwind': '$' + group_by},
        {
            '$group': {
                '_id': '$' + group_by,
                'count': {'$sum': 1},
            }
        },
        {
            '$project': {
                '_id': 0,
                'value': '$_id',
                'count': 1,
            }
        },
        {
            '$sort': {'count': -1}
        },
        {
            '$limit': 100,
        }
    ]


def _get_single_value_facet_pipeline(facet, match):
    pipeline = []
    if match:
        if facet in match:
            matchc = match.copy()
            del matchc[facet]
        else:
            matchc = match
        pipeline = [
            {'$match': matchc}
        ] if match else []
    return pipeline + _get_single_value_group_pipeline(facet)


def _get_single_value_group_pipeline(group_by):
    return [
        {
            '$group': {
                '_id': '$' + group_by,
                'count': {'$sum': 1},
            }
        },
        {
            '$project': {
                '_id': 0,
                'value': '$_id',
                'count': 1,
            }
        },
        {
            '$sort': {'count': -1}
        },
        {
            '$limit': 100,
        }
    ]


@ myapp.route("/search/resolved2_facets", methods=['GET'])
def resolved2_facets():
    # --------------------------------
    # to be replaced by "metadata_facets"
    # --------------------------------

    if user == None:
        return redirect(url_for('login'))

    catlist, colors = allcategories_and_colors()
    match = getmatch(request.args, catlist)

    search = request.args.get('search', '')

    hidas = _get_array_param(request.args.get('hidas', ''))
    path = _get_array_param(request.args.get('path', ''))
    doctype = _get_array_param(request.args.get('doctype', ''))
    ext = _get_array_param(request.args.get('ext', ''))
    district = _get_array_param(request.args.get('district', ''))
    vorhaben = _get_array_param(request.args.get('vorhaben', ''))
    Sachbegriff = _get_array_param(request.args.get('Sachbegriff', ''))
    Denkmalart = _get_array_param(request.args.get('Denkmalart', ''))
    Denkmalname = _get_array_param(request.args.get('Denkmalname', ''))

    if path:
        match['path'] = {'$in': path}
    if hidas:
        match['hidas'] = {'$in': hidas}
    if doctype:
        match['doctype'] = {'$in': doctype}
    if ext:
        match['ext'] = {'$in': ext}
    if district:
        match['district'] = {'$in': district}
    if vorhaben:
        match['vorhaben'] = {'$in': vorhaben}
    if Sachbegriff:
        match['Sachbegriff'] = {'$in': Sachbegriff}
    if Denkmalart:
        match['Denkmalart'] = {'$in': Denkmalart}
    if Denkmalname:
        match['Denkmalname'] = {'$in': Denkmalname}
    pipeline = [{
        '$match': {'$text': {'$search': search}}
    }] if search else []

    facets = {
        'path':  _get_single_value_facet_pipeline('path', match),
        'path':  _get_single_value_facet_pipeline('path', match),
        'hidas':  _get_facet_pipeline('hidas', match),
        'doctype': _get_single_value_facet_pipeline('doctype', match),
        'ext': _get_single_value_facet_pipeline('ext', match),
        'district': _get_single_value_facet_pipeline('district', match),
        'vorhaben':  _get_single_value_facet_pipeline('vorhaben', match),
        'Sachbegriff':  _get_facet_pipeline('Sachbegriff', match),
        'Denkmalart':  _get_facet_pipeline('Denkmalart', match),
        'Denkmalname':  _get_facet_pipeline('Denkmalname', match),
    }
    for cat in catlist:
        facets[cat] = _get_facet_pipeline(cat, match)

    pipeline += [{'$facet': facets}]

    col = mydb[metadatatable]
    json_string ="{}"
    try:
        res = list(col.aggregate(pipeline))[0]
        json_string = json.dumps(res, ensure_ascii=False)
    except:
       pass
    
    response = Response(
        json_string, content_type="application/json; charset=utf-8")
    return response


@ myapp.route("/search/metadata_facets", methods=['POST'])
def metadata_facets():
    if user == None:
        return redirect(url_for('login'))

    catlist = []
    singlevaluefacets = []
    multivaluefacets = []
    search = []
    match = {}

    if request.method == 'POST':
        if request.json:
            if 'search' in request.json:
                search = request.json['search']
            if 'match' in request.json:
                match = request.json['match']
            if 'categories' in request.json:
                catlist = request.json['categories']
            if 'singlevaluefacets' in request.json:
                singlevaluefacets = request.json['singlevaluefacets']
            if 'multivaluefacets' in request.json:
                multivaluefacets = request.json['multivaluefacets']
            if 'corpus' in request.json:
                corpus = request.json['corpus']
    if len(catlist) == 0:
        catlist, colors = allcategories_and_colors()

    facets = {}
    for f in singlevaluefacets:
        facets[f] = _get_single_value_facet_pipeline(f, match)
    for f in multivaluefacets:
        facets[f] = _get_facet_pipeline(f, match)
    for cat in catlist:
        facets[cat] = _get_facet_pipeline(cat, match)

    pipeline = [{
        '$match': {'$text': {'$search': search}}
    }] if search else []

    pipeline += [{'$facet': facets}]

    col = mydb[metadatatable]
    res = list(col.aggregate(pipeline))[0]
    json_string = json.dumps(res, ensure_ascii=False)
    response = Response(
        json_string, content_type="application/json; charset=utf-8")
    return response

# def getFilterFromArgs(args, catlist, singlevaluefacets, multivaluefacets):
#     match = getmatch(args, catlist)
#     search = args.get('search', '')
#     facetnames = singlevaluefacets + multivaluefacets
#     for facet in facetnames:
#         filter = _get_array_param(args.get(facet, ''))
#         if filter:
#             match[facet] = {'$in': filter}
#     pipeline = [{
#         '$match': {'$text': {'$search': search}}
#     }] if search else []
#     return pipeline, match


@ myapp.route("/search/resolved2", methods=['GET'])
def resolved2():
    if user == None:
        return redirect(url_for('login'))
    # pagination
    page = int(request.args.get('page', '0'))
    page_size = int(request.args.get('page_size', '50'))
    skip = page * page_size
    limit = min(page_size, 50)

    catlist, col = allcategories_and_colors()
    match = getmatch(request.args, catlist)

    search = request.args.get('search', '')
    # regex = request.args.get('regex', '')

    # if search and str(search).startswith("/") and str(search).endswith("/"):
    #     try:
    #         re.compile(search)
    #         pattern=search[1:len(search)-1]
    #         regex = pattern
    #         search=''
    #     except:
    #         print("Non valid regex pattern")
 
    hidas = _get_array_param(request.args.get('hidas', ''))
    path = _get_array_param(request.args.get('path', ''))
    doctype = _get_array_param(request.args.get('doctype', ''))
    ext = _get_array_param(request.args.get('ext', ''))
    district = _get_array_param(request.args.get('district', ''))
    vorhaben = _get_array_param(request.args.get('vorhaben', ''))
    Sachbegriff = _get_array_param(request.args.get('Sachbegriff', ''))
    Denkmalart = _get_array_param(request.args.get('Denkmalart', ''))
    Denkmalname = _get_array_param(request.args.get('Denkmalname', ''))

    if search and search != '':
        # match['$text'] = {'$search': search, '$language': 'de'}
       match['$text'] = {'$search': search}
    # if regex and regex != '':
    #     match['text'] = {'$regex': "/" + regex + "/" }

    if path:
        match['path'] = {'$in': path}
    if hidas:
        match['hidas'] = {'$in': hidas}
    if doctype:
        match['doctype'] = {'$in': doctype}
    if ext:
        match['ext'] = {'$in': ext}
    if district:
        match['district'] = {'$in': district}
    if vorhaben:
        match['vorhaben'] = {'$in': vorhaben}
    if Sachbegriff:
        match['Sachbegriff'] = {'$in': Sachbegriff}
    if Denkmalart:
        match['Denkmalart'] = {'$in': Denkmalart}
    if Denkmalname:
        match['Denkmalname'] = {'$in': Denkmalname}

    pipeline = [{
        '$match': match
    }] if match else []

    pipeline += [{
        '$facet': {
            metadatatable: [
                {'$skip': skip},
                {'$limit': limit}
            ],
            'count': [
                {'$count': 'total'}
            ],
        }
    }]

    col = mydb[metadatatable]
    res={}
    try:
        res = list(col.aggregate(pipeline))[0]
    except:
        return

    
    print(res["count"])

    # remove _id, is an ObjectId and is not serializable
    # for resolved in res[metadatatable]:
    #     del resolved['_id']

    vi: Dict[str, Any] = []
    for v in res[metadatatable]:  # remove _id, is an ObjectId and is not serializable
        v1: Dict[str, Any] = {}
        for a in v:
            if a != "_id" and a != "obj" and a != "hida" and a != "meta" and a != "topic" and a != "adrDict" and a != "text2":
                v1[a] = v[a]
        vi.append(v1)

    del res[metadatatable]
    res["metadata"] = vi
    res['count'] = res['count'][0]['total'] if res['count'] else 0

    # return jsonify(res)
    json_string = json.dumps(res, ensure_ascii=False)
    response = Response(
        json_string, content_type="application/json; charset=utf-8")
    return response


@ myapp.route("/search/metadata", methods=['POST'])
def metadata():
    if user == None:
        return redirect(url_for('login'))
    search = []
    regex = ''
    match = {}

    # pagination
    page = 0
    page_size = 50

    if request.method == 'POST':
        if request.json:
            if 'page' in request.json:
                page = request.json['page']
            if 'page_size' in request.json:
                page_size = request.json['page_size']
            if 'search' in request.json:
                search = request.json['search']
            if 'regex'  in request.json:
                regex = request.json['regex']
            if 'match' in request.json:
                match = request.json['match']

    skip = page * page_size
    limit = min(page_size, 50)

    if search and str(search).startswith("/") and str(search).endswith("/"):
        regex=search[1:len(search)-1]
        search=''
    if search and search != '':
        match['$text'] = {'$search': search}
    # if regex and regex != '':
    #     match['text'] = {'$regex': "/" + regex + "/" }

    pipeline = [{
        '$match': match
    }] if match else []

    pipeline += [{
        '$facet': {
            metadatatable: [
                {'$skip': skip},
                {'$limit': limit}
            ],
            'count': [
                {'$count': 'total'}
            ],
        }
    }]

    col = mydb[metadatatable]
    res = list(col.aggregate(pipeline))[0]
    print(res["count"])

    # remove _id, is an ObjectId and is not serializable
    # for resolved in res[metadatatable]:
    #     del resolved['_id']

    vi: Dict[str, Any] = []
    for v in res[metadatatable]:  # remove _id, is an ObjectId and is not serializable
        v1: Dict[str, Any] = {}
        for a in v:
            if a != "_id" and a != "obj" and a != "hida" and a != "meta" and a != "topic" and a != "adrDict" and a != "text2":
                v1[a] = v[a]
        vi.append(v1)

    del res[metadatatable]
    res["metadata"] = vi
    res['count'] = res['count'][0]['total'] if res['count'] else 0

    # return jsonify(res)
    json_string = json.dumps(res, ensure_ascii=False)
    response = Response(
        json_string, content_type="application/json; charset=utf-8")
    return response


@ myapp.route("/search/doclib", methods=['GET'])
def doclib():
    res = {}
    global lib
    if lib == None:
        lib = ""
    otherlib = lib.replace(r"kibardokintern/Treptow/", "")
    otherres = otherlib + r"kibardokintern/Treptow/"
    
    if metadatatable == "koepenick":
        otherres = otherlib + r"kibardokintern/Treptow/2_Köpenick"
    if metadatatable == "treptow" or metadatatable == "metadata":
        otherres = otherlib + r"kibardokintern/Treptow/"
    if metadatatable == "pankow":
        otherres = otherlib + r"kibardokintern/Pankow/"
    if metadatatable == "lichtenberg":
        otherres = otherlib + r"kibardokintern/Lichtenberg/"
    res['doclib'] = otherres

    # return jsonify(res)
    json_string = json.dumps(res, ensure_ascii=False)
    response = Response(
        json_string, content_type="application/json; charset=utf-8")
    return response


@ myapp.route("/search/hida2_facets", methods=['GET'])
def hida2_facets():

    hcatlist = ["Sachbegriff",
                "Num-Dat",
                "Künstler-Rolle", "Künstler-Name", "Künstler-Funktion",
                "Sozietät-Art-Rolle", "Sozietät-Name", "Sozietät-ber-Funktion",
                "Ausw-Stelle"]

    match = getmatch(request.args, hcatlist)

    Bezirk = _get_array_param(request.args.get('Bezirk', ''))
    Ortsteil = _get_array_param(request.args.get('Ortsteil', ''))
    Denkmalart = _get_array_param(request.args.get('Denkmalart', ''))

    search = request.args.get('search', '')

    pipeline = [{
        '$match': {'$text': {'$search': search}}
    }] if search else []

    if Bezirk:
        match['Bezirk'] = {'$in': Bezirk}
    if Ortsteil:
        match['Ortsteil'] = {'$in': Ortsteil}
    if Denkmalart:
        match['Denkmalart'] = {'$in': Denkmalart}

    facets = {
        'Bezirk':  _get_single_value_facet_pipeline('Bezirk', match),
        'Ortsteil':  _get_single_value_facet_pipeline('Ortsteil', match),
        'Denkmalart':  _get_single_value_facet_pipeline('Denkmalart', match),
    }
    for cat in hcatlist:
        facets[cat] = _get_facet_pipeline(cat, match)

    pipeline += [{'$facet': facets}]

    col = mydb["hida"]
    res = list(col.aggregate(pipeline))[0]

    json_string = json.dumps(res, ensure_ascii=False)
    response = Response(
        json_string, content_type="application/json; charset=utf-8")
    return response


@ myapp.route("/search/hida2", methods=['GET'])
def hida2():
    # pagination
    page = int(request.args.get('page', '0'))
    page_size = int(request.args.get('page-size', '50'))
    skip = page * page_size
    limit = min(page_size, 50)

    # "Bezirk", "Ortsteil", "Denkmalart", "Sachbegriff",
    hcatlist = ["Sachbegriff", "Num-Dat", "Künstler-Rolle", "Künstler-Name",
                "Künstler-Funktion",
                "Sozietät-Art-Rolle",
                "Sozietät-Name",
                "Sozietät-ber-Funktion"
                "Ausw-Stelle"]

    match = getmatch(request.args, hcatlist)

    Bezirk = _get_array_param(request.args.get('Bezirk', ''))
    Ortsteil = _get_array_param(request.args.get('Ortsteil', ''))
    Denkmalart = _get_array_param(request.args.get('Denkmalart', ''))

    search = request.args.get('search', '')

    if search and search != '':
        match['$text'] = {'$search': search}

    if Bezirk:
        match['Bezirk'] = {'$in': Bezirk}
    if Ortsteil:
        match['Ortsteil'] = {'$in': Ortsteil}
    if Denkmalart:
        match['Denkmalart'] = {'$in': Denkmalart}

    pipeline = [{
        '$match': match
    }] if match else []

    pipeline += [{
        '$facet': {
            'hida': [
                {'$skip': skip},
                {'$limit': limit}
            ],
            'count': [
                {'$count': 'total'}
            ],
        }
    }]

    col = mydb["hida"]
    res = list(col.aggregate(pipeline))[0]
    print(res["count"])

    vi: Dict[str, Any] = []
    for v in res['hida']:  # remove _id, is an ObjectId and is not serializable
        v1: Dict[str, Any] = {}
        for a in v:
            if a != "_id":
                v1[a] = v[a]
        vi.append(v1)

    res['hida'] = vi
    res['count'] = res['count'][0]['total'] if res['count'] else 0

    # return jsonify(res)
    json_string = json.dumps(res, ensure_ascii=False)
    response = Response(
        json_string, content_type="application/json; charset=utf-8")
    return response

# #########################################


@myapp.route('/excel/qs', methods=['GET'])
def excelqs2():
    if user == None:
        return redirect(url_for('login'))
    col = mydb[metadatatable]
    vi: Dict[str, Any] = []
    for row in col.find({"qs": {"$exists": True}}):
        v1: Dict[str, Any] = {}
        v1["docid"] = row["docid"]
        for a in row["qs"]:
            v1[a] = row["qs"][a]
        vi.append(v1)

    df_1 = pd.DataFrame(vi)

    # df_1 = pd.DataFrame(vi)
    # df_1 = pd.DataFrame(np.random.randint(0,10,size=(10, 4)), columns=list('ABCD'))

    # create an output stream
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')

    # taken from the original question
    df_1.to_excel(writer, startrow=0, merge_cells=False, sheet_name="Sheet_1")
    workbook = writer.book
    worksheet = writer.sheets["Sheet_1"]
    writer.close()
    output.seek(0)
    return send_file(output, attachment_filename="qs.xlsx", as_attachment=True)


@myapp.route('/excel/resolved2', methods=['GET'])
def excelresolved2():
    if user == None:
        return redirect(url_for('login'))
    # pagination
    # page = int(request.args.get('page', '0'))
    page_size = int(request.args.get('page_size', '50'))
    # skip = page * page_size
    limit = min(page_size, 50)
    page = 0
    skip = 0
    # limit = 100

    catlist, col = allcategories_and_colors()
    match = getmatch(request.args, catlist)

    search = request.args.get('search', '')

    hidas = _get_array_param(request.args.get('hidas', ''))
    path = _get_array_param(request.args.get('path', ''))
    doctype = _get_array_param(request.args.get('doctype', ''))
    ext = _get_array_param(request.args.get('ext', ''))
    district = _get_array_param(request.args.get('district', ''))
    vorhaben = _get_array_param(request.args.get('vorhaben', ''))
    Sachbegriff = _get_array_param(request.args.get('Sachbegriff', ''))
    Denkmalart = _get_array_param(request.args.get('Denkmalart', ''))
    Denkmalname = _get_array_param(request.args.get('Denkmalname', ''))

    if search and search != '':
        match['$text'] = {'$search': search}

    if path:
        match['path'] = {'$in': path}
    if hidas:
        match['hidas'] = {'$in': hidas}
    if doctype:
        match['doctype'] = {'$in': doctype}
    if ext:
        match['ext'] = {'$in': ext}
    if district:
        match['district'] = {'$in': district}
    if vorhaben:
        match['vorhaben'] = {'$in': vorhaben}
    if Sachbegriff:
        match['Sachbegriff'] = {'$in': Sachbegriff}
    if Denkmalart:
        match['Denkmalart'] = {'$in': Denkmalart}
    if Denkmalname:
        match['Denkmalname'] = {'$in': Denkmalname}

    pipeline = [{
        '$match': match
    }] if match else []

    metaspec = [{'$skip': skip}, {'$limit': limit}]

    pipeline += [{
        '$facet': {
            metadatatable: metaspec,
            'count': [
                {'$count': 'total'}
            ],
        }
    }]

    col = mydb[metadatatable]
    res = list(col.aggregate(pipeline))[0]
    print(res["count"])

    # remove _id, is an ObjectId and is not serializable
    # for resolved in res[metadatatable]:
    #     del resolved['_id']

    vi: Dict[str, Any] = []
    for v in res[metadatatable]:  # remove _id, is an ObjectId and is not serializable
        v1: Dict[str, Any] = {}
        for a in v:
            if a != "_id" and a != "obj" and a != "hida" and a != "meta" and a != "topic" and a != "adrDict" and a != "text":
                v1[a] = v[a]
        vi.append(v1)

    # res[metadatatable] = vi
    res['count'] = res['count'][0]['total'] if res['count'] else 0

    cnt = res['count']
    while cnt > len(vi):
        page += 1
        skip = page * page_size
        metaspec[0] = {'$skip': skip}
        res = list(col.aggregate(pipeline))[0]
        for v in res[metadatatable]:  # remove _id, is an ObjectId and is not serializable
            v1: Dict[str, Any] = {}
            for a in v:
                if a != "_id" and a != "obj" and a != "hida" and a != "meta" and a != "topic" and a != "adrDict" and a != "text":
                    v1[a] = v[a]
            vi.append(v1)
        return excel(vi, "testing.xlsx", "Sheet_1")


def excel(vi: dict, attachment_filename: str, sheet_name: str):
    df_1 = pd.DataFrame(vi)

    # df_1 = pd.DataFrame(vi)
    # df_1 = pd.DataFrame(np.random.randint(0,10,size=(10, 4)), columns=list('ABCD'))

    # create an output stream
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')

    # taken from the original question
    df_1.to_excel(writer, startrow=0, merge_cells=False, sheet_name=sheet_name)
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]
    # format = workbook.add_format()
    # format.set_bg_color('#eeeeee')
    # worksheet.set_column(0,9,28)

    # the writer has done its job
    writer.close()

    # go back to the beginning of the stream
    output.seek(0)

    # finally return the file
    return send_file(output, attachment_filename=attachment_filename, as_attachment=True)


# #########################################
# spacy API

@ myapp.route("/spacy/hasvector", methods=['GET', 'POST'])
def hasvector():
    text = ""
    corpus = spacy_default_corpus
    query = request.args
    if query:
        if "text" in query:
            text = query["text"]
        if "corpus" in query:
            corpus = query["corpus"]

    if request.method == 'POST':
        if request.json:
            if 'text' in request.json:
                text = request.json['text']
            if 'corpus' in request.json:
                corpus = request.json['corpus']

    res = hasVector(text, corpus)
    print(res)
    json_string = json.dumps(res, ensure_ascii=False)
    response = Response(
        json_string, content_type="application/json; charset=utf-8")
    return response


@ myapp.route("/spacy/wordswithvector", methods=['GET', 'POST'])
def wordswithvector():
    corpus = spacy_default_corpus
    query = request.args
    ontology: dict[str, list[str]] = {}
    if query:
        if "corpus" in query:
            corpus = query["corpus"]

    if request.method == 'POST':
        if request.json:
            if 'corpus' in request.json:
                corpus = request.json['corpus']
            if 'ontology' in request.json:
                ontology = request.json['ontology']

    word_dimension, word_supers, categories, plist, badlistjs = prepareList(
        ontology, [], [])
    loadCorpus(corpus, word_dimension)
    words = getSpacyVectors(word_dimension, corpus)

    res = list(words.keys())
    # print(res)
    json_string = json.dumps(res, ensure_ascii=False)
    response = Response(
        json_string, content_type="application/json; charset=utf-8")
    return response


@ myapp.route("/spacy/similarity", methods=['GET', 'POST'])
def similarity():
    word = ""
    word2 = ""
    corpus = spacy_default_corpus

    query = request.args
    if query:
        if "word" in query:
            word = query["word"]
        if "word2" in query:
            word2 = query["word2"]
        if "corpus" in query:
            corpus = query["corpus"]

    if request.method == 'POST':
        if request.json:
            if 'word' in request.json:
                word = request.json['word']
            if 'word2' in request.json:
                word2 = request.json['word2']
            if 'corpus' in request.json:
                corpus = request.json['corpus']

    res = getSimilarity(word, word2, corpus)
    # print(res)
    # json_string = json.dumps(res, ensure_ascii=False)
    # response = Response(
    #     json_string, content_type="application/json; charset=utf-8")
    # return response
    return res


@ myapp.route("/spacy/similaritymatrix", methods=['POST'])
def similaritymatrix():
    words = []
    words2 = []
    dist = 0.0
    corpus = spacy_default_corpus

    if request.method == 'POST':
        if request.json:
            if 'words' in request.json:
                words = request.json['words']
            if 'words2' in request.json:
                words2 = request.json['words2']
            if 'corpus' in request.json:
                corpus = request.json['corpus']
            if 'dist' in request.json:
                dist = request.json['dist']

    res = getSimilarityMatrix(words, words2, dist, corpus)
    print(res)
    json_string = json.dumps(res, ensure_ascii=False)
    response = Response(
        json_string, content_type="application/json; charset=utf-8")
    return response


@ myapp.route("/spacy/mostsimilar", methods=['GET', 'POST'])
def mostsimilar():
    word = ""
    topn = 10
    corpus = spacy_default_corpus

    query = request.args
    if query:
        if "word" in query:
            word = query["word"]
        if "topn" in query:
            topn = query["topn"]
        if "corpus" in query:
            corpus = query["corpus"]

    if request.method == 'POST':
        if request.json:
            if 'word' in request.json:
                word = request.json['word']
            if 'topn' in request.json:
                topn = request.json['topn']
            if 'corpus' in request.json:
                corpus = request.json['corpus']

    words, distances = mostSimilar(word,  corpus, topn)
    dis = list(distances[0])
    res = [(words[i], float(dis[i])) for i in range(0, len(words))]
    print(res)
    json_string = json.dumps(res, ensure_ascii=False)
    response = Response(
        json_string, content_type="application/json; charset=utf-8")
    return response


def prepareList(ontology: dict[str, list[str]], pattern: list[str], badlist: list[str]):
    wvi: dict[str, list[str]] = {}
    if len(ontology) > 0:
        wvi = ontology
    else:
        if "vorhaben_inv" in collist:
            vorhabeninv_col = mydb["vorhaben_inv"]
            vorhabeninv: dict = vorhabeninv_col.find_one()
            wvi = vorhabeninv["words"]
    word_dimension, word_supers = prepareWords(wvi)

    categories: list[str] = []

    # if "categories" in collist:
    #     cat_col = mydb["categories"]
    #     catobj = cat_col.find_one()
    #     for cat in catobj:
    #         if cat != '_id':
    #             categories.append(cat)

    patternjs: list[str] = []
    if len(pattern) == 0 and "pattern" in collist:
        pattern_col = mydb["pattern"]
        pattern = pattern_col.find()
    for v in pattern:
        patternjs.append(v["paragraph"])
    plist: List[Dict[str, str]] = preparePattern(patternjs)

    badlistjs: list[str] = []

    if len(badlist) == 0 and "badlist" in collist:
        badlist_col = mydb["badlist"]
        badlist = badlist_col.find()
    for v in badlist:
        badlistjs.append(v["paragraph"])

    return word_dimension, word_supers, categories, plist, badlistjs


@ myapp.route("/spacy/matchingconcepts", methods=['GET', 'POST'])
def matchingconcepts():
    text = ""
    ontology: dict[str, list[str]] = {}
    pattern: list[str] = []
    badlist: list[str] = []
    dist = 0.8
    corpus = spacy_default_corpus

    query = request.args
    if query:
        if "text" in query:
            text = query["text"]
        if "corpus" in query:
            corpus = query["corpus"]
        if "distance" in query:
            dist = query["distance"]

    if request.method == 'POST':
        if request.json:
            if 'text' in request.json:
                text = request.json['text']
            if 'ontology' in request.json:
                ontology = request.json['ontology']
            if 'corpus' in request.json:
                corpus = request.json['corpus']
            if 'badlist' in request.json:
                ontology = request.json['badlist']
            if 'distance' in request.json:
                dist = request.json['distance']

    word_dimension, word_supers, categories, plist, badlistjs = prepareList(
        ontology, pattern, badlist)
    res = matchingConcepts(word_dimension, word_supers,
                           plist, badlistjs, text, dist, corpus)

    print(res)
    json_string = json.dumps(res, ensure_ascii=False)
    response = Response(
        json_string, content_type="application/json; charset=utf-8")
    return response


@ myapp.route("/spacy/extractintents", methods=['GET', 'POST'])
def extractintents():
    text = ""
    ontology: dict[str, list[str]] = {}
    pattern: list[str] = []
    badlist: list[str] = []
    dist = 0.98
    s2v = False
    corpus = spacy_default_corpus

    query = request.args
    if query:
        if "text" in query:
            text = query["text"]
        if "corpus" in query:
            corpus = query["corpus"]
        if "distance" in query:
            dist = query["distance"]

    if request.method == 'POST':
        if request.json:
            if 'text' in request.json:
                text = request.json['text']
            if 'ontology' in request.json:
                ontology = request.json['ontology']
            if 'corpus' in request.json:
                corpus = request.json['corpus']
            if 'badlist' in request.json:
                badlist = request.json['badlist']
            if 'distance' in request.json:
                dist = request.json['distance']
            if 's2v' in request.json:
                s2v = request.json['distance'] == True

    word_dimension, word_supers, categories, match_pattern, badlist = prepareList(
        ontology, pattern, badlist)

    bparagraph = True

    res = extractIntents(
        word_dimension, word_supers, categories, match_pattern, badlist, bparagraph,
        text, dist, corpus, s2v)

    # print(res)
    json_string = json.dumps(res, ensure_ascii=False)
    response = Response(
        json_string, content_type="application/json; charset=utf-8")
    return response


@ myapp.route("/spacy/extractlemmata", methods=['GET', 'POST'])
def extractlemmata():
    text = ""
    corpus = spacy_default_corpus

    query = request.args
    if query:
        if "text" in query:
            text = query["text"]
        if "corpus" in query:
            corpus = query["corpus"]

    if request.method == 'POST':
        if request.json:
            if 'text' in request.json:
                text = request.json['text']
            if 'corpus' in request.json:
                corpus = request.json['corpus']
    res = extractLemmata(text, corpus)

    # print(res)
    json_string = json.dumps(res, ensure_ascii=False)
    response = Response(
        json_string, content_type="application/json; charset=utf-8")
    return response


@ myapp.route("/spacy/displacy", methods=['POST'])
def displacy():
    text: str = ""
    ents: list[any] = []
    catlist, colors = allcategories_and_colors()

    if request.method == 'POST':
        if request.json:
            if 'text' in request.json:
                text = request.json['text']
            if 'entities' in request.json:
                ents = request.json['entities']
            if 'colors' in request.json:
                colors = request.json['colors']

    options = {"ents": catlist, "colors": colors}
    res = displacyTextHTML(text, ents, options)
    # print(res)
    response = Response(
        res, content_type="plain/text; charset=utf-8")
    return response

# #########################################


@ myapp.route("/metadata/clonecollection", methods=['POST'])
def clone_Collection():
    colname = ""
    desturi = ""
    destdbname = ""
    destcolname = ""

    query = request.args
    if query:
        if "colname" in query:
            colname = query["colname"]
        if "desturi" in query:
            desturi = query["desturi"]
        if "destdbname" in query:
            destdbname = query["destdbname"]
        if "destcolname" in query:
            destcolname = query["destcolname"]

    if request.method == 'POST':
        if request.json:
            if 'colname' in request.json:
                colname = request.json['colname']
            if 'desturi' in request.json:
                desturi = request.json['desturi']
            if 'destdbname' in request.json:
                destdbname = request.json['destdbname']
            if 'destcolname' in request.json:
                destcolname = request.json['destcolname']

    res = cloneCollection(colname, desturi, destdbname, destcolname)
    # print(res)
    response = Response(
        res, content_type="plain/text; charset=utf-8")
    return response


@ myapp.route("/showcopydatabase", methods=['GET', 'POST'])
def show_copydatabase():
    nargs = {"desturi": "",
             "destdbname": "KIBarDok",
             "badlist": []}
    if request.method == 'POST':
        if 'desturi' in request.form and request.form['desturi']:
            nargs["desturi"] = request.form['desturi']
        if 'destdbname' in request.form and request.form['destdbname']:
            nargs["destdbname"] = request.form['destdbname']

        thread = threading.Thread(target=cloneDatabase, kwargs=nargs)
        thread.daemon = True         # Daemonize
        thread.start()
        return render_template('services.html')
    return render_template('copy_database.html', res=nargs)


@ myapp.route("/metadata/clonedatabase", methods=['GET', 'POST'])
def clone_Database(desturi: str, destdbname: str):
    desturi = ""
    destdbname = ""
    badlist = []

    query = request.args
    if query:
        if "desturi" in query:
            desturi = query["desturi"]
        if "destdbname" in query:
            destdbname = query["destdbname"]

    if request.method == 'POST':
        if request.json:
            if 'desturi' in request.json:
                desturi = request.json['desturi']
            if 'destdbname' in request.json:
                destdbname = request.json['destdbname']
            if 'badlist' in request.json:
                badlist = request.json['badlist']

    res = cloneDatabase(desturi, destdbname, badlist)
    # print(res)
    response = Response(
        res, content_type="plain/text; charset=utf-8")
    return response

# insert_many("files.json", "folders")
# insert_many(r".\static\badlist.json", "badlist")
# { "colname": "badlist", "items": {}}


@ myapp.route("/metadata/insert_many", methods=['POST'])
def insert_many_srv():
    colname = ""
    dict = {}
    if request.method == 'POST':
        if request.json:
            if 'colname' in request.json:
                colname = request.json['colname']
            if 'items' in request.json:
                dict = request.json['items']

    res = insert_many(dict, colname)
    response = Response(res, content_type="plain/text; charset=utf-8")
    return response


@ myapp.route("/metadata/insert_one", methods=['POST'])
def insert_one_srv():
    colname = ""
    dict = {}
    if request.method == 'POST':
        if request.json:
            if 'colname' in request.json:
                colname = request.json['colname']
            if 'item' in request.json:
                dict = request.json['item']

    res = insert_one(dict, colname)
    response = Response(res, content_type="plain/text; charset=utf-8")
    return response

# { "hidaname": "hida",
# "ispattern": false,
# "ishida": false,
# "iscategories": false,
# "isfolders": false,
# "isbadlist": false,
# "isvorhaben": false,
# "isvorhabeninv": false,
# "istaxo": false,
# "isinvtaxo": false}


@ myapp.route("/metadata/init", methods=['POST'])
def init_database():
    if request.method == 'POST':
        if request.json:
            res = initMongoFromStaticFiles(**request.json)
            response = Response(
                res, content_type="plain/text; charset=utf-8")
            return response


@ myapp.route("/showprojectmetadata", methods=['GET', 'POST'])
def show_project_metadata():
    # corpus = spacy_default_corpus
    supcol = mydb["support"]
    sup: dict = supcol.find_one()
    if sup != None and "project" in sup:
        nargs = sup["project"]
    else:
        nargs = {"metadataname": "treptow",
                 "hidaname": "hida",
                 "ismetadatahida": False,
                 "ismetadatakeywords": False,
                 "ismetadatanokeywords": True,
                 "isupdatehida": False,
                 "isupdatetaxo": False,
                 "isupdatehidataxo": False,
                 }
    if request.method == 'POST':
        if 'hidaname' in request.form and request.form['hidaname']:
            nargs["hidaname"] = request.form['hidaname']
        if 'metadataname' in request.form and request.form['metadataname']:
            nargs["metadataname"] = request.form['metadataname']
        nargs["ismetadatahida"] = 'ismetadatahida' in request.form
        nargs["ismetadatakeywords"] = 'ismetadatakeywords' in request.form
        nargs["ismetadatanokeywords"] = 'ismetadatanokeywords' in request.form
        nargs["isupdatehida"] = 'isupdatehida' in request.form
        nargs["isupdatetaxo"] = 'isupdatetaxo' in request.form
        nargs["isupdatehidataxo"] = 'isupdatehidataxo' in request.form
        supcol.update_one({"_id": sup["_id"]}, {"$set": {"project": nargs}})

        log: any = getLog(1)
        if log != {}:
            return "We are busy. Please try later: " + nargs["name"].dumps(log)
        thread = threading.Thread(target=projectMetaData, kwargs=nargs)
        thread.daemon = True         # Daemonize
        thread.start()
        # return "Extraction started in background thread."
        return render_template('services.html')

    return render_template('project_metadata.html', res=nargs)

# { "metadataname": "metadata",
# "hidaname": "hida",
# "ismetadatahida": false,
# "ismetadatakeywords": false,
# "ismetadatanokeywords": false,
# "isupdatehida": false,
# "isupdatetaxo": false,
# "isupdatehidataxo": false
# }


@ myapp.route("/metadata/project", methods=['POST'])
def project_metadata():
    res = projectMetaData(**request.json)
    response = Response(
        res, content_type="plain/text; charset=utf-8")
    return response


@ myapp.route("/showextractmetadata", methods=['GET', 'POST'])
def show_extract_metadata():
    # corpus = spacy_default_corpus
    supcol = mydb["support"]
    sup: dict = supcol.find_one()
    if sup != None and "extract" in sup:
        nargs = sup["extract"]
    else:
        nargs = {"name": "Treptow",
                 "metadataname": "treptow",
                 "district": "Treptow-Köpenick",
                 "path": r"C:\\Data\\test\\KIbarDok\\Treptow\\1_Treptow",
                 "foldersname": "folders",
                 "tika": r"http://localhost:9998",
                 "startindex": 0,
                 "dist": 0.8,
                 "s2v": True,
                 "corpus": spacy_default_corpus,
                 "istika": False,
                 "isfolders": False,
                 "issupport": False,
                 "isaddress": True,
                 "isdoctypes": False,
                 "isdates": False,
                 "istopic": False,
                 "isintents": False
                 }
    if request.method == 'POST':
        if 'name' in request.form and request.form['name']:
            nargs["name"] = request.form['name']
        if 'metadataname' in request.form and request.form['metadataname']:
            nargs["metadataname"] = request.form['metadataname']
        if 'district' in request.form and request.form['district']:
            nargs["district"] = request.form['district']
        if 'path' in request.form and request.form['path']:
            nargs["path"] = request.form['path']
        if 'foldersname' in request.form and request.form['foldersname']:
            nargs["foldersname"] = request.form['foldersname']
        if 'tika' in request.form and request.form['tika']:
            nargs["tika"] = request.form['tika']
        if 'startindex' in request.form and request.form['startindex']:
            nargs["startindex"] = request.form['startindex']
        if 'dist' in request.form and request.form['dist']:
            nargs["dist"] = request.form['dist']
        if 's2v' in request.form and request.form['s2v']:
            nargs["s2v"] = 's2v' in request.form['s2v']
        if 'corpus' in request.form and request.form['corpus']:
            nargs["corpus"] = request.form['corpus']
        nargs["istika"] = 'istika' in request.form
        nargs["isfolders"] = 'isfolders' in request.form
        nargs["issupport"] = 'issupport' in request.form
        nargs["isaddress"] = 'isaddress' in request.form
        nargs["isdoctypes"] = 'isdoctypes' in request.form
        nargs["isdates"] = 'isdates' in request.form
        nargs["istopic"] = 'istopic' in request.form
        nargs["isintents"] = 'isintents' in request.form
        supcol.update_one({"_id": sup["_id"]}, {"$set": {"extract": nargs}})

        log: any = getLog(1)
        if log != {}:
            return "We are busy. Please try later: " + nargs["name"]
        thread = threading.Thread(target=extractMetaData, kwargs=nargs)
        thread.daemon = True         # Daemonize
        thread.start()
        # return "Extraction started in background thread."
        return render_template('services.html')

    return render_template('extract_metadata.html', res=nargs)


#  body = { "name": "Treptow",
#         "metadataname": "treptow",
#         "district": "Treptow-Köpenick",
#         "path": "C:\\Data\\test\\KIbarDok\\Treptow\\1_Treptow",
#         "foldersname": "folders",
#         "tika": "http://localhost:9998",
#         "startindex": 0,
#         "dist": 0.8,
#         "s2v": True,
#         "corpus": spacy_default_corpus,
#         "istika": False,
#         "issupport": False,
#         "isaddress": True,
#         "isdoctypes": False,
#         "isdates": False,
#         "istopic": False,
#         "isintents": False
# }
@ myapp.route("/metadata/extract", methods=['POST'])
def extract_metadata():
    log: any = getLog(1)
    if log != {}:
        return "We are busy. Please try later: " + json.dumps(log)
    thread = threading.Thread(target=extractMetaData, kwargs=request.json)
    thread.daemon = True         # Daemonize
    thread.start()
    return "Extraction started in background thread."


@ myapp.route("/metadata/getlog", methods=['POST'])
def getlog_metadata():
    topn = 10

    if request.method == 'POST':
        if request.json:
            if 'topn' in request.json:
                topn = request.json['topn']

    res = getLog(topn)
    json_string = json.dumps(res, ensure_ascii=False)
    response = Response(
        json_string, content_type="application/json; charset=utf-8")
    return response


@ myapp.route("/metadata/resetlog", methods=['POST'])
def resetlog_metadata():
    res = resetLog()
    json_string = json.dumps(res, ensure_ascii=False)
    response = Response(
        json_string, content_type="application/json; charset=utf-8")
    return response


@ myapp.route("/showlogdata", methods=['GET', 'POST'])
def show_logdata():
    # if request.method == 'POST':
    #     print(request)
    log = getLog(10)
    t = []
    for i in log:
        s = log[i]
        t.append(" ".join(str(e) for e in log[i]))
    return render_template('show_log.html', title="Log", list=t)


@ myapp.route("/cancelall", methods=['GET', 'POST'])
def cancelall():
    log: any = getLog(1)
    if log != {}:
        cancel_execution()
    return show_logdata()
