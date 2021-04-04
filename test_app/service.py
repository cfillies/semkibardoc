from flask import Flask, json, Response, request, render_template, url_for, flash, redirect
import pymongo
import os
import datetime
from werkzeug.exceptions import abort

myapp = Flask(__name__)
myapp.config['SECRET_KEY'] = 'your secret key'

uri = os.getenv("MONGO_CONNECTION")
myclient = pymongo.MongoClient(uri)

mydb = myclient["kibardoc"]
collist = mydb.list_collection_names()

if not "posts" in collist:
    posts_col = mydb["posts"]
    posts_col.insert_many([{'ID': 1, 'title': "TIT1", 'created': datetime.datetime.now(), 'content': 'cont1'},
                           {'ID': 2, 'title': "TIT2", 'created': datetime.datetime.now(), 'content': 'cont2'}])


def get_post(post_id):
    posts_col = mydb["posts"]
    post = posts_col.find_one({'ID': post_id})
    if post is None:
        abort(404)
    return post


@myapp.route("/")
def index():
    posts_col = mydb["posts"]
    posts = posts_col.find()
    # return "Hello Flask, This is the KiBarDok Service. Try hida, intents, words, badlist, paragraph"
    return render_template('index.html', posts=posts)


@myapp.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@myapp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash('Title is required!')
        else:
            posts_col = mydb["posts"]
            posts = posts_col.find()
            maxid = 0
            for p in posts:
                if p['ID'] > maxid:
                    maxid = p['ID']
            newid = maxid+1
            posts_col.insert({'ID': newid, 'title': title,
                             'created': datetime.datetime.now(), 'content': content})
            return redirect(url_for('index'))
    return render_template('create.html')


@myapp.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash('Title is required!')
        else:
            posts_col = mydb["posts"]
            posts_col.update_one(
                {'ID': id}, {'$set': {'title': title, 'content': content}})
            return redirect(url_for('index'))
    return render_template('edit.html', post=post)

@myapp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    posts_col = mydb["posts"]
    posts_col.remove( {'ID': id})
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))

@myapp.route("/hida")
def allhida():
    # print(request.args)
    query = request.args
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


@myapp.route("/taxo")
def alltaxo():
    query = request.args
    collist = mydb.list_collection_names()
    vi = []
    if "taxo" in collist:
        taxo_col = mydb["taxo"]
        taxo = taxo_col.find(query)
        for v in taxo:
            vi.append(v)
    response = Response(
        str(vi), content_type="application/json; charset=utf-8")
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


@myapp.route("/pattern")
def allpattern():
    collist = mydb.list_collection_names()
    vi = []
    if "pattern" in collist:
        pattern_col = mydb["pattern"]
        pattern = pattern_col.find()
        for v in pattern:
            vi.append(v["paragraph"])
    json_string = json.dumps(vi, ensure_ascii=False)
    response = Response(
        json_string, content_type="application/json; charset=utf-8")
    return response


@myapp.route("/badlist")
def allbadlist():
    collist = mydb.list_collection_names()
    vi = []
    if "badlist" in collist:
        badlist_col = mydb["badlist"]
        badlist = badlist_col.find()
        for v in badlist:
            vi.append(v["paragraph"])
    json_string = json.dumps(vi, ensure_ascii=False)
    response = Response(
        json_string, content_type="application/json; charset=utf-8")
    return response
