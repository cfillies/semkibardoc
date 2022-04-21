import spacy
import re
import numpy as np
import pickle
# import sklearn
from pymongo.collection import Collection
from metadata.support import logEntry

tagger=None

def clean_text( text : str ) -> str:
    
    """
    this function cleans the argument text by
    - removing multiple white spaces
    - removing "\""
    - removing everything but '[^a-zA-ZÄÖÜäöüß0-9 ]+'
    - then, the text is split at " ", and for each token, it is checked whether it only consists of uppercase letter.
    If it does contain lowercase letters, it is broken at every uppercase letter
    - tokens of length 1 and 2 are removed
    
    PARAMETERS
    ----------
        text : str
            a str object that is to be cleaned
            
    RETURNS
    -------
        ret : str
            a str object of cleaned text
    """
    
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
    
    """
    The tagger can only work with texts that have at most 512 tokens. Therefore, this function
    splits a text into sequences of at most 512 tokens.
    
    Also, we ignore any token with length 2 or smaller.
    
    PARAMETERS
    ----------
        text : str
            the text to be split
            
    RETURNS
    -------
        list_of_texts : list
            a list of texts
    """
    
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
    
    """
    This functions reduces a given text to a set of lemmatized nouns.
    
    PARAMETERS
    ----------
        text : str
            the text to be reduced
            
    RETURNS
    -------
        lemmatized : str
            the lemmatized text
    """

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
    
    """
    This functions reduces a dirty text to a set of lemmatized nouns
    
    PARAMETERS
    ----------
        text : str
            the dirty text
            
    RETURNS
    -------
        clean : str
            the cleaned text
    """
    
    return lemmatize_text( clean_text( text ) )

def init():
    global tagger
    tagger = spacy.load( 'de_dep_news_trf' )
    path_to_tfidf = "C:\\Data\\test\\kibartmp\\msg_modelle\\classifier\\tfidf.pickle"
    path_to_forest = "C:\\Data\\test\\kibartmp\\msg_modelle\\classifier\\forest.pickle"
    file = open( path_to_tfidf, "rb" )
    vectorizer = pickle.load( file )
    file.close()
    file = open( path_to_forest, "rb" )
    forest = pickle.load( file )
    file.close()
    return tagger, vectorizer, forest

# text = 'BA Treptow-Köpenick von Berlin\t\nAbt. Bauen, Stadtentwicklung und Umwelt\nStadtentwicklungsamt\t\nFachbereich Denkmalschutz\t\t\n\nFrau Töpfer\nGrün II 3\n\n\n\n\nGeschZ.\t\tBearbeiter/in\t\t\tZimmer\tTelefon\tTelefax\t\t\tDatum  \n[bookmark: _GoBack]FB UD552-14\t\tFrau Marion Zeidler\t\t321\t\t90297-2191\t90297-2195\t\t13.10.2014\n\n\nBetr.: Grundstück: Treptower Park\n\nStellungnahmeersuchen vom: 13.10.12015\nEingang: 14.10.2014 \n\nVorhaben: Baumfällung Ulmus BaumNr.20444 Parkteil B\nIhr Zeichen: Grün II 3\n\n\n\n\nDas Einvernehmen gemäß § 12 Abs. 3 DSchG Bln  wird in Verbindung mit § 11 Abs. 1 Denkmalschutzgesetz Berlin (DSchG Bln) vom 24.04.1995 (GVBl. 22 S. 274), zuletzt geändert durch Artikel II des Gesetzes vom 8. Juli 2010 (GVBl. S. 396) zu Baumfällung Ulmus BaumNr.204444 Parkteil B  erteilt.\nA\nGemäß § 11 Abs. 4 DSchG Bln kann die Genehmigung unter nachfolgend aufgeführten Bedingungen bzw. Auflagen sowie unter dem Vorbehalt des Widerrufs oder befristet erteilt werden.\n\n\nAuflagen:\n\n- Nachpfllanzung \n\nBegründung\n\nI.  Sachverhalt\n\n\n1. Genehmigungsbedürftigkeit\n\nDas beantragte Vorhaben  ist nach DSchG Bln genehmigungsbedürftig.\n\nNach § 11 Abs. 1 DSchG Bln darf ein Denkmal nur mit Genehmigung der zuständigen Denkmalbehörde in seinem Erscheinungsbild verändert, ganz oder teilweise beseitigt, von seinem Standort oder Aufbewahrungsort entfernt oder instandgesetzt und wiederhergestellt werden\n\nDie vom Antragsteller  beabsichtigte Baumfällungen\nist eine Veränderung des Denkmals im Sinne von § 11 Abs. 1 Nr.  1  DSchG Bln und somit nach dem Denkmalschutzgesetz genehmigungspflichtig.\n\n\n\n2. Denkmaleigenschaft\n\n3. Genehmigungsfähigkeit\n\nDie Genehmigung kann gemäß § 11 Abs. 4 DSchG Bln unter Bedingungen und Auflagen sowie \nunter dem Vorbehalt des Widerrufs oder befristet erteilt werden.\n\nDie denkmalrechtliche Genehmigung  zum o. g. Vorhaben wird unter Auflagen erteilt:\n\nAuflagen : Nachpflanzung in Abstimmung mit UD\n\nGemäß § 12 Abs. 2 DSchG Bln erlischt die Genehmigung, wenn nicht innerhalb von zwei Jahren nach Erteilung mit der Ausführung begonnen oder wenn die Ausführung ein Jahr unterbrochen worden ist. Die Fristen nach Satz 1 können auf schriftlichen Antrag jeweils bis zu einem Jahr verlängert werden.\n\nGemäß § 12 Abs. 3 DSchG Bln werden Genehmigungen, die auf Grund anderer Rechtsvorschriften erforderlich sind, durch die Erteilung auf Grund dieses Gesetzes nicht ersetzt.\n\n\n\n\n\nZeidler\n\n\n\n\nSeite 1 - 2\n\n'
# print( text )

# x = forest.predict( vectorizer.transform( [ lemmatize_text( clean_text( text ) ) ] ) )
# print(x)
        
doctypes = {"0": "Kein Dokumenttyp gefunden",
"1": "Genehmigung",
"2": "Stellungnahme",
"3": "Anfrage",
"4": "Nachforderung",
"5": "Eingang",
"6": "Versagung",
"7": "Antrag"}

def findDocTypeSpacy(col: Collection):
    tagger, vectorizer, forest = init()
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
        lt = len(text)
        if  i > 0:
            doctypecodes = forest.predict(vectorizer.transform([lemmatize_text( clean_text( text))]))
            doctype=doctypes[str(doctypecodes[0])]
            print(i, doc["file"], str(doctype))
            if len(doctype)>0:
                if not logEntry(["DocType2: ", i, " " , doctype]):
                    return
                col.update_one({"_id": doc["_id"]}, { "$set": {"doctype2": doctype}})
            else:
                col.update_one({"_id": doc["_id"]}, { "$set": {"doctype2": "Kein Dokumenttyp gefunden"}})