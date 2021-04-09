from flask import Flask, json, Response, request, render_template, url_for, flash, redirect
import pymongo

import datetime
from werkzeug.exceptions import abort
from intent import extractTopicsAndPlaces, prepareWords, preparePattern, spacytest

#  https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3
myapp = Flask(__name__)
myapp.config['SECRET_KEY'] = 'your secret key'

#  uri = os.getenv("MONGO_CONNECTION")
uri = "mongodb+srv://semtation:SemTalk3!@cluster0.pumvg.mongodb.net/kibardoc?retryWrites=true&w=majority" 

myclient = pymongo.MongoClient(uri)

mydb = myclient["kibardoc"]
collist = mydb.list_collection_names()

@myapp.route("/")
def index():
    return render_template('index.html')
    # return "Hello Flask, This is the KiBarDok Service. Try hida, intents, words, badlist, paragraph"


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
    # uri = os.getenv("MONGO_CONNECTION")
    # myclient = pymongo.MongoClient(uri)
    # myclient._topology_settings
    # mydb = myclient["kibardoc"]
    # collist = mydb.list_collection_names()
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

@myapp.route("/showpattern")
def showpattern():
    vi = []
    if "pattern" in collist:
        list_col = mydb["pattern"]
        list = list_col.find()
        for v in list:
            vi.append(v["paragraph"])
    return render_template('show_list.html', list=sorted(vi), title="Boilerplates")

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
            vi.append(v["paragraph"])
    return render_template('show_list.html', list=sorted(vi), title="Badlist")

@myapp.route("/testprepare")
def testprepare():
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
    
    res = extractTopicsAndPlaces(words, wordlist, plist, badlistjs, bparagraph, "")
    # print(res)
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




