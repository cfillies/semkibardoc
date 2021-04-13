from flask import Flask, json, Response, request, render_template, url_for, flash, redirect
from flask_cors import CORS
import pymongo

import datetime
from werkzeug.exceptions import abort
from bson.objectid import ObjectId


from intent import extractTopicsAndPlaces, prepareWords, preparePattern, spacytest

#  https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3
myapp = Flask(__name__)
myapp.config['SECRET_KEY'] = 'your secret key'
CORS(myapp)

#  uri = os.getenv("MONGO_CONNECTION")
uri = "mongodb+srv://semtation:SemTalk3!@cluster0.pumvg.mongodb.net/kibardoc?retryWrites=true&w=majority" 

myclient = pymongo.MongoClient(uri)

mydb = myclient["kibardoc"]
collist = mydb.list_collection_names()

@myapp.route("/")
def index():
    return render_template('index.html')
    # return "Hello Flask, This is the KiBarDok Service. Try hida, intents, words, badlist, paragraph"

@myapp.route("/documents")
def documents():
    # print(request.args)
    query = request.args
    vi = []
    if "resolved" in collist:
        col = mydb["resolved"]
        resolved = col.find(query)
        for v in resolved:
            vi.append(v)
            file=v['file']
            path=v['dir']
            obj= v['obj']
            vi.append({ 'file': file, 'path': path, 'obj': obj})
    # json_string = json.dumps(vi,ensure_ascii = False)
    response = Response(
        str(vi), content_type="application/json; charset=utf-8")
    return response

@myapp.route("/showdocuments")
def showdocuments():
    vi = []
    if "resolved" in collist:
        col = mydb["resolved"]
        query = request.args
        resolved = col.find(query)
        for v in resolved:
            vi.append(v)
    return render_template('show_documents.html', documents=vi)

@myapp.route("/showdocument")
def showdocument():
    vi = []
    if "resolved" in collist:
        col = mydb["resolved"]
        query = request.args
        resolved = col.find(query)
        for v in resolved:
            return render_template('show_document.html', res=v)

@myapp.route("/hida")
def allhida():
    # print(request.args)
    query = request.args
    vi = []
    if "hida" in collist:
        hida_col = mydb["hida"]
        hida = hida_col.find(query)
        for v in hida:
            mname=""
            if 'Listentext' in v:
                mname= v['Listentext']
            elif 'Denkmalname' in v:
                mname= v['Denkmalname']
            sb = []
            if 'Sachbegriff' in v:
                sb= v['Sachbegriff']
            if 'OBJ-Dok-Nr' in v:
                vi.append({ 'OBJ-Dok-Nr': v['OBJ-Dok-Nr'], 'Listentext': mname, 'Sachbegriff':sb})
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

@myapp.route("/showhida/<id>")
def showhida(id=""):
    collist = mydb.list_collection_names()
    if "hida" in collist:
        hida_col = mydb["hida"]
        hida = hida_col.find({'OBJ-Dok-Nr': id})
        res = {}
        for v in hida:
            for at in v:
                if at != "_id" and at !="Objekt-Type":
                    va = v[at]
                    if isinstance(va, list): 
                        va = ', '.join(va)
                    res[at]=va    
            return render_template('show_monument.html', res=res, title="Hida")

@myapp.route("/monuments")
def monuments():
    vi = []
    if "hida" in collist:
        hida_col = mydb["hida"]
        query = request.args
        hida = hida_col.find(query)
        for v in hida:
            mname=""
            if 'Listentext' in v:
                mname= v['Listentext']
            elif 'Denkmalname' in v:
                mname= v['Denkmalname']
            sb = []
            if 'Sachbegriff' in v:
                sb= v['Sachbegriff']
            if 'OBJ-Dok-Nr' in v:
                vi.append({ 'OBJ-Dok-Nr': v['OBJ-Dok-Nr'], 'Listentext': mname, 'Sachbegriff':sb})
    return render_template('show_monuments.html', monuments=vi)

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

@myapp.route("/showtaxo")
def showtaxo():
    query = request.args
    vi = []
    if "taxo" in collist:
        taxo_col = mydb["taxo"]
        taxo = taxo_col.find(query)
        for v in taxo:
            vi.append(v)
    return render_template('show_taxo.html', taxo=vi, title="Taxonomy")

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

@myapp.route("/showintents")
def showintents():
    vi = {}
    if "vorhaben_inv" in collist:
        vorhabeninv_col = mydb["vorhaben_inv"]
        vorhabeninv = vorhabeninv_col.find()
        for v in vorhabeninv:
            for intent in sorted(v["intents"]):
                vi[intent] = v["intents"][intent]
    return render_template('show_listdict.html', listdict=vi, title="Subclasses")

@myapp.route("/words")
def allwords():
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


@myapp.route("/words/<word>")
def words(word=""):
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

@myapp.route("/showwords")
def showwords():
    vi = {}
    if "vorhaben_inv" in collist:
        vorhabeninv_col = mydb["vorhaben_inv"]
        vorhabeninv = vorhabeninv_col.find()
        for v in vorhabeninv:
            for wor in sorted(v["words"]):
                vi[wor] = v["words"][wor]
    return render_template('show_listdict.html', listdict=vi, title="Superclasses")

def get_item(table, id):
    col = mydb[table]
    item = col.find_one({'_id': ObjectId(id)})
    if item is None:
        abort(404)
    return item

@myapp.route("/pattern")
def allpattern():
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

@myapp.route('/pattern/<id>')
def pattern(id):
    item = get_item("pattern", id)
    return render_template('show_item.html', item=item)

@myapp.route("/showpattern")
def showpattern():
    vi = []
    if "pattern" in collist:
        list_col = mydb["pattern"]
        list = list_col.find()
        for v in list:
            vi.append(v)
    return render_template('show_list.html', list=sorted(vi, key=lambda p: p['paragraph']), title="Boilerplates", table="pattern")

@myapp.route('/pattern/<id>/edit', methods=('GET', 'POST'))
def editpatternlist(id):
    item = get_item("pattern", id)
    if request.method == 'POST':
        paragraph = request.form['paragraph']
        col = mydb["pattern"]
        col.update_one(
            {'_id': ObjectId(id)}, {'$set': {'paragraph': paragraph}})
        return redirect(url_for('showpattern'))
    return render_template('edit_item.html', item=item, delete_item="deletepattern")

@myapp.route('/pattern/<id>/delete', methods=('POST',))
def deletepattern(id):
    # item = get_item("pattern", id)
    col = mydb["pattern"]
    col.remove({'_id': ObjectId(id)})
    flash('"{}" was successfully deleted!'.format('Item'))
    return redirect(url_for('showpattern'))


@myapp.route("/badlist")
def allbadlist():
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

@myapp.route("/showbadlist")
def showbadlist():
    vi = []
    if "badlist" in collist:
        list_col = mydb["badlist"]
        list = list_col.find()
        for v in list:
            vi.append(v)
    return render_template('show_list.html', list=sorted(vi, key=lambda p: p['paragraph']), title="Badlist", table="editbadlist")

@myapp.route('/badlist/<id>')
def badlist(id):
    item = get_item("badlist", id)
    return render_template('show_item.html', item=item)

@myapp.route('/badlist/<id>/edit', methods=('GET', 'POST'))
def editbadlist(id):
    item = get_item("badlist", id)
    if request.method == 'POST':
        paragraph = request.form['paragraph']
        col = mydb["badlist"]
        col.update_one(
            {'_id': ObjectId(id)}, {'$set': {'paragraph': paragraph}})
        return redirect(url_for('showbadlist'))
    return render_template('edit_item.html', item=item, delete_item="deletebadlist")

@myapp.route('/badlist/<id>/delete', methods=('POST',))
def deletebadlist(id):
    # item = get_item("badlist", id)
    col = mydb["badlist"]
    col.remove({'_id': ObjectId(id)})
    flash('"{}" was successfully deleted!'.format('Item'))
    return redirect(url_for('showbadlist'))

@myapp.route("/keywords")
def keywords():
    query = request.args
    collist = mydb.list_collection_names()
    vi = []
    if "topics" in collist:
        list_col = mydb["topics"]
        list = list_col.find(query)
        for v in list:
            vi.append({ "file": v["file"], "keywords": v["keywords"], "intents": v["intents"] })
    json_string = json.dumps(vi, ensure_ascii=False)   
    response = Response(
        json_string, content_type="application/json; charset=utf-8")
    return response

@myapp.route("/allshowkeywords")
def allshowkeywords():
    query = request.args
    collist = mydb.list_collection_names()
    vi = []
    if "topics" in collist:
        list_col = mydb["topics"]
        list = list_col.find(query)
        for v in list:
            vi.append(v)
        return render_template('show_documents_keywords.html', documents=vi, title="Keywords", table="show_keywords")

@myapp.route("/showkeywords/<id>")
def showkeywords(id=""):
    collist = mydb.list_collection_names()
    if "topics" in collist:
        item = get_item("topics", id)
        return render_template('show_extraction.html', res=item, title="Keyword")

@myapp.route("/showfilekeywords")
def showfilekeywords(file=""):
    collist = mydb.list_collection_names()
    if "topics" in collist:
        list_col = mydb["topics"]
        query = request.args
        list = list_col.find(query)
        for v in list:
            item=v
        return render_template('show_extraction.html', res=item, title="Keyword")

@myapp.route("/extractintents", methods=('GET', 'POST'))
def extractintents():
    
    wvi = {}
    query = request.args
   
    if "vorhaben_inv" in collist:
        vorhabeninv_col = mydb["vorhaben_inv"]
        vorhabeninv = vorhabeninv_col.find()
        for v in vorhabeninv:
            for wor in v["words"]:
                wvi[wor] = v["words"][wor]
    words, wordlist = prepareWords(wvi)        
            

    patternjs = []
    if "pattern" in collist:
        pattern_col = mydb["pattern"]
        pattern = pattern_col.find()
        for v in pattern:
            patternjs.append({"paragraph": v["paragraph"]})
    plist = preparePattern(patternjs)        

    badlistjs = []
    if "badlist" in collist:
        badlist_col = mydb["badlist"]
        badlist = badlist_col.find()
        for v in badlist:
            badlistjs.append({"paragraph": v["paragraph"]})
    
    bparagraph = False
    if "bparagraph" in query:
        bparagraph = query["bparagraph"]
    
    res= extractTopicsAndPlaces(words, wordlist, plist, badlistjs, bparagraph, "")
    # return res

    print(res)
    json_string = json.dumps(res, ensure_ascii=False)
    response = Response(
        json_string, content_type="application/json; charset=utf-8")
    return response

@myapp.route('/create_extraction', methods=('GET', 'POST'))
def create_extraction():
    if request.method == 'POST':
        text = request.form['content']
        # print(text)
      #  return redirect(url_for('extractintents'))
        wvi = {}
        query = request.args
        if "vorhaben_inv" in collist:
            vorhabeninv_col = mydb["vorhaben_inv"]
            vorhabeninv = vorhabeninv_col.find()
            for v in vorhabeninv:
                for wor in v["words"]:
                    wvi[wor] = v["words"][wor]
        words, wordlist = prepareWords(wvi)        
                

        patternjs = []
        if "pattern" in collist:
            pattern_col = mydb["pattern"]
            pattern = pattern_col.find()
            for v in pattern:
                patternjs.append({"paragraph": v["paragraph"]})
        plist = preparePattern(patternjs)        

        badlistjs = []
        if "badlist" in collist:
            badlist_col = mydb["badlist"]
            badlist = badlist_col.find()
            for v in badlist:
                badlistjs.append({"paragraph": v["paragraph"]})
        
        bparagraph = False
        if "bparagraph" in query:
            bparagraph = query["bparagraph"]
        
        res = extractTopicsAndPlaces(words, wordlist, plist, badlistjs, bparagraph, text)
        if len(res)>0:
            return render_template('show_extraction.html', res=res[0])
        else:
            return render_template('index.html')

        # print(res)
        # json_string = json.dumps(res, ensure_ascii=False)
        # response = Response(
        #     json_string, content_type="application/json; charset=utf-8")
        # return response

    return render_template('create_extraction.html')

@myapp.route("/testprepare1")
def testprepare1():
    s=spacytest("Wollen wir die Fenster am Haus streichen?")
    json_string = json.dumps(s, ensure_ascii=False)
    response = Response(
        json_string, content_type="application/json; charset=utf-8")
    return response

@myapp.route("/testprepare2")
def testprepare2():
    collist = mydb.list_collection_names()
    wvi = {}
    if "vorhaben_inv" in collist:
        vorhabeninv_col = mydb["vorhaben_inv"]
        vorhabeninv = vorhabeninv_col.find()
        for v in vorhabeninv:
            for wor in v["words"]:
                wvi[wor] = v["words"][wor]
    words, wordlist = prepareWords(wvi)        
    s=spacytest("Wollen wir die Fenster am Haus streichen?")
    json_string = json.dumps(s, ensure_ascii=False)
    response = Response(
        json_string, content_type="application/json; charset=utf-8")
    return response

# CRUD UI Demo ########################################################

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


@myapp.route("/posts")
def posts():
    posts_col = mydb["posts"]
    posts = posts_col.find()
    # return "Hello Flask, This is the KiBarDok Service. Try hida, intents, words, badlist, paragraph"
    return render_template('posts.html', posts=posts)

###
@myapp.route('/posts/<int:id>')
def show_post(id):
    post = get_post(id)
    return render_template('show_post.html', post=post)


@myapp.route('/posts/create', methods=('GET', 'POST'))
def create_post():
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
            return redirect(url_for('posts'))
    return render_template('create_post.html')


@myapp.route('/posts/<int:id>/edit', methods=('GET', 'POST'))
def edit_post(id):
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
            return redirect(url_for('posts'))
    return render_template('edit_post.html', post=post)


@myapp.route('/posts/<int:id>/delete', methods=('POST',))
def delete_post(id):
    post = get_post(id)
    posts_col = mydb["posts"]
    posts_col.remove({'ID': id})
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('posts'))




