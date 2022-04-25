# from tkinter import N
import spacy
import re
import numpy as np
import pickle
# import sklearn
from pymongo.collection import Collection
from metadata.support import logEntry

tagger=None
index_of_words=None
idf=None

def clean_text( text : str ) -> str:
    ret = re.sub( '[^a-zA-ZÄÖÜäöüß0-9@+ ]+', ' ', text )
    ret = re.sub( ' +', ' ', ret )
    ret = ret.replace( "\"", "" )
    tokens = re.split( " ", ret )
    list_of_tokens = []
    for token in tokens:
        if token.upper() == token:
            list_of_tokens.append( token )
        elif token.lower() == token:
            list_of_tokens.append( token )
        elif ( token[ 0 ].upper == token[ 0 ] ) and ( token[ 1 : len( token ) ].lower() == token[ 1 : len( token ) ] ):
            list_of_tokens.append( token )
        else:
            if token[ 0 ].upper() == token[ 0 ]:   
                new_tokens = re.findall( '[A-ZÄÖÜ][^A-ZÄÖÜ]*', token )
                for new_token in new_tokens:
                    list_of_tokens.append( new_token )
            else:
                first_token = re.split( "[A-ZÄÖÜ]", token )[ 0 ]
                list_of_tokens.append( first_token )
                additional_tokens = re.findall( '[A-ZÄÖÜ][^A-ZÄÖÜ]*', token )
                for additional_token in additional_tokens:
                    list_of_tokens.append( additional_token )
    ret = ""
    for token in list_of_tokens:
        ret += token + " "
    ret = ret[ 0 : len( ret ) - 1 ]
    return ret

def split_text( text : str ) -> list:
    tokens = text.split( " " )
    number_of_items = int( np.ceil( len( tokens ) / 512 ) )
    list_of_texts = []
    for i in range( number_of_items ):
        start = i * 512
        end = min( ( i + 1 ) * 512, len( tokens ) )
        sublist = tokens[ start : end ]
        text_in_sublist = ""
        for token in sublist:
            if len( token ) > 2:
                text_in_sublist += token + " "
        text_in_sublist = text_in_sublist[ 0 : len( text_in_sublist ) ]
        list_of_texts.append( text_in_sublist )
    return list_of_texts

def lemmatize_text( text : str ) -> str:  
    only_nouns = ""
    list_of_texts = split_text( text )
    for item in list_of_texts:
        global tagger
        doc = tagger( re.sub( "[^a-zA-ZÄÖÜäöüß ]", "", item ) )
        for token in doc:
            word = token.lemma_
            if token.pos_ == "NOUN":
                only_nouns +=  word + " "
    only_nouns = only_nouns[ 0 : len( only_nouns ) - 1 ]
    return only_nouns

def reduce_text( text : str ) -> str:
    return lemmatize_text( clean_text( text ) )

def tfidf( text : str ) -> np.array:
    words = text.split( " " )
    arr = np.zeros( shape = [ len( index_of_words.items() ) ] )
    for word in words:
        if word in idf:
            arr[ int( index_of_words[ word ] ) ] += 1 / idf[ word ]
    return arr

def init():
    tagger0 = spacy.load( 'de_dep_news_trf' )

    path_to_forest = "C:\\Data\\test\\kibartmp\\msg_modelle\\classifier\\forest.pickle"
    file0 = open( path_to_forest, "rb" )
    forest0 = pickle.load( file0 )
    file0.close()

    path_to_index = "C:\\Data\\test\\kibartmp\\msg_modelle\\classifier\\index.pickle"
    file1 = open( path_to_index, "rb" )
    index_of_words1 = pickle.load( file1 )
    file1.close()

    path_to_idf = "C:\\Data\\test\\kibartmp\\msg_modelle\\classifier\\idf.pickle"
    file2 = open( path_to_idf, "rb" )
    idf2 = pickle.load( file2 )
    file2.close()
    
    return tagger0, forest0, index_of_words1, idf2


        
doctypes = {"0": "Kein Dokumenttyp gefunden",
"1": "Genehmigung",
"2": "Stellungnahme",
"3": "Anfrage",
"4": "Nachforderung",
"5": "Eingang",
"6": "Versagung",
"7": "Antrag"}

def findDocTypeSpacy(col: Collection):
    global index_of_words
    global idf
    global tagger
    tagger, forest, index_of_words, idf = init()

    dlist = []
    for doc in col.find():
        dlist.append(doc)
    i = 0
    dlist = []
    for doc in col.find():
        dlist.append(doc)

    for doc in dlist:
        i = i+1
        text = doc["text"]
        text = reduce_text( text )
        lt = len(text)
        if  i > 0:
            if lt < 10:
                col.update_one({"_id": doc["_id"]}, {
                               "$set": {"doctype2": "< 10 Zeichen"}})
            else:
                if lt > 10000:
                    dtype = "zu groß: "
                    if not logEntry(["Dokumenttyp2: ",i, " ", doc["file"], dtype, lt]):
                        return
                    col.update_one({"_id": doc["_id"]}, {
                                   "$set": {"doctype2": "> 10000 Zeichen"}})
                    continue
                doctypecodes = forest.predict( [ tfidf( text ) ] )
                doctype=doctypes[str(doctypecodes[0])]
                print(i, doc["file"], str(doctype))
                if len(doctype)>0:
                    if not logEntry(["DocType2: ", i, " " , doctype]):
                        return
                    col.update_one({"_id": doc["_id"]}, { "$set": {"doctype2": doctype}})
                else:
                    col.update_one({"_id": doc["_id"]}, { "$set": {"doctype2": "Kein Dokumenttyp gefunden"}})