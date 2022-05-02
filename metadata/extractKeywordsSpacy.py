import pickle
import re
import spacy
import numpy as np

model = None
idf = None
def init():
    global model
    model = spacy.load( 'de_dep_news_trf' )
    path_to_idf = "..\\..\\test\\kibartmp\\msg_modelle\\keywords\\idf.data"
    file = open( path_to_idf, "rb" )
    global idf
    idf = pickle.load( file )
    file.close()

def clean_text( text : str ) -> str:
    
    """
    this function cleans the argument text by
    - removing multiple white spaces
    - removing "\""
    - removing everything but '[^a-zA-ZÄÖÜäöüß ]+'
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
    
    ret = re.sub( '[^a-zA-ZÄÖÜäöüß+ ]+', ' ', text )
    
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
    global model

    """
    This function takes a given text and lemmatizes each word in the text.
    
    PARAMETERS
    ----------
        text : str
            the text to be lemmatized
            
    RETURNS
    -------
        lemmatized : str
            the lemmatized text
    """
    
    lemmatized = ""
    
    list_of_texts = split_text( text )
    
    for item in list_of_texts:
    
        doc = model( item )
    
        for token in doc:
            
            if token.pos_ == "NOUN":
            
                lemmatized += token.lemma_ + " "
            
    lemmatized = lemmatized[ 0 : len( lemmatized ) - 1 ]
    
    return lemmatized

def tf_idf_importance( text : str ) -> str:
    
    """
    This function takes a text and returns die most important words with respect to tf-idf.
    
    PARAMETERS
    ----------
        text : str
            the text to be processed
            
    RETURNS
    -------
        important_words : str
            a sequence of the most important words
    """
    
    text = lemmatize_text( clean_text( text ) )
    
    tokens = text.split( " " )
    
    counts = {}
    for token in tokens:
        
        global idf
        if token in idf:
            
            if token not in counts:
                
                counts[ token ] = 1
                
            else:
                
                counts[ token ] += 1
                
    fractions = [ ( word, count / idf[ word ] ) for ( word, count ) in counts.items() ]
    
    fractions = sorted( fractions, key = lambda x : x[ 1 ], reverse = True )[ \
                            0 : int( np.ceil( np.sqrt( len( fractions ) ) ) ) ]
    
    important_words = " ".join( [ word for ( word, number ) in fractions ] )
    
    return important_words

def demo( text : str ) -> None:
    
    """
    Show the most important words of a text and the text.
    
    PARAMETERS
    ----------
        text : str
            the text to be analyzed
    """
    
    words = tf_idf_importance( text )
    
    print( "Wichtige Worte:" )
    
    print( words )
    
    print( "" )
    
    print( "" )
    
    print( "" )
    
    print( "Text:" )
    
    print( text )
# text = '\r\n\n\r\n\nBezirksamt Köpenick von Berlin\t(\r\n\nAbteilung Bau- und Wohnungswesen\r\n\nUntere Denkmalschutzbehörde\r\n\n\r\n\n\r\n\n\r\n\n�Bezirksamt Köpenick von Berlin, Postfach 1137, 12532 Berlin (Postanschrift)\r\n\n\t\t\r\n\n�\t\t\r\n\n\r\n\n\r\n\n\r\n\n\r\n\n\r\n\n\r\n\n\r\n\n\r\n\n\r\n\n\r\n\n\r\n\n\r\n\nBearbeiter/in\tTelefon (030)\tTelefax (030)\t\tDatum \tGeschZ. (bitte stets angeben)\r\n\nHerr Breer\t6582-2335\t6582-2337\t\t\t07.08.1998\t\tUD-619\r\n\n\t\t\t\t\t\t\t\r\n\n\r\n\n\r\n\n\r\n\nBetr.: Broschüre über die Denkmallandschaft\r\n\nhier:   Ihr Schreiben vom 13.07.1998\r\n\n\r\n\n\r\n\nSehr geehrte Frau von der Haar,\r\n\n\r\n\nnach der Urlaubszeit fanden wir Ihren Brief vor.\r\n\n\r\n\nAnbei erhalten Sie einige Exemplare unserer kleinen Broschüre. Wir wünschen Ihnen bei der Lektüre viel Freude.\r\n\n\r\n\nIn diesem Zusammenhang interessieren wir uns natürlich für Ihre Arbeit. Daher würden wir uns freuen, wenn wir uns vielleicht inhaltlich austauschen würden.\r\n\n\r\n\nMit freundlichen Grüßen\r\n\nIm Auftrag\r\n\n\r\n\n\r\n\n\r\n\nBreer\r\n\n\r\n\n�\nV1\r\n\nBezirksamt Köpenick von Berlin\t(\r\n\nAbteilung Bau- und Wohnungswesen\r\n\nUntere Denkmalschutzbehörde\r\n\n\r\n\n\r\n\n\r\n\n�Bezirksamt Köpenick von Berlin, Postfach 1137, 12532 Berlin (Postanschrift)\r\n\n\t\t\r\n\n�\t\t\r\n\n\r\n\n\r\n\n\r\n\n\r\n\n\r\n\n\r\n\n\r\n\n\r\n\n\r\n\n\r\n\n\r\n\n\r\n\nBearbeiter/in\tTelefon (030)\tTelefax (030)\t\tDatum \tGeschZ. (bitte stets angeben)\r\n\nHerr Breer\t6582-2335\t6582-2337\t\t\t07.08.1998\t\tUD-619\r\n\n\t\t\t\t\t\t\t\r\n\n\r\n\n\r\n\n\r\n\nBetr.: Broschüre über die Denkmallandschaft\r\n\nhier:   Ihr Schreiben vom 13.07.1998\r\n\n\r\n\n\r\n\nSehr geehrte Frau von der Haar,\r\n\n\r\n\nnach der Urlaubszeit fanden wir Ihren Brief vor.\r\n\n\r\n\nAnbei erhalten Sie einige Exemplare unserer kleinen Broschüre. Wir wünschen Ihnen bei der Lektüre viel Freude.\r\n\n\r\n\nIn diesem Zusammenhang interessieren wir uns natürlich für Ihre Arbeit. Daher würden wir uns freuen, wenn wir uns vielleicht inhaltlich austauschen würden.\r\n\n\r\n\nMit freundlichen Grüßen\r\n\nIm Auftrag\r\n\n\r\n\n\r\n\n\r\n\nBreer\r\n\n\r\n\n\r\n\n� DATEINAME \\* Kleinbuchstaben\\p \\* FORMATVERBINDEN �d:\\aktenplan\\6193\\6193_1\\broschüre.doc�\r\n\n\r\n\n\r\n\nSprechzeiten:\tBankverbindung:\tFahrverbindung:\r\n\nMo, Di\t  9.00 - 12.00 Uhr\tSparkasse der Stadt Berlin\tPostbank Berlin\tBerliner Bank\tStraßenbahn  68\r\n\nDo   \t16.00 - 18.00 Uhr\tKto.-Nr.:1613013228\tKto.-Nr.: 651616-109\tKto.-Nr.: 7281759300\t4. Station nach Schloßplatz\r\n\n\t\tBLZ 100 500 00\tBLZ: 100 10010\tBLZ: 100 200 00\tRichtung Alt Schmöckwitz\r\n\n\r\n\n\r\n\n\r\n\n\r\n\nBezirksamt Köpenick von Berlin\r\n\nDienstgebäude \r\n\nGrünauer Str. 210-216\r\n\n12557 Berlin\r\n\n\r\n\nZimmer:  318\r\n\n\r\n\n\r\n\nForschungsprojekt Jugendberatung\r\n\nProf. Dr. Elke von der Haar\r\n\nFachhochschule für Sozialarbeit und Sozialpädagogik Berlin\r\n\nKarl-Schrader-Str. 6\r\n\n\r\n\n10781 Berlin\r\n\n\r\n\nBezirksamt Köpenick von Berlin\r\n\nDienstgebäude \r\n\nGrünauer Str. 210-216\r\n\n12557 Berlin\r\n\n\r\n\nZimmer:  318\r\n\n\r\n\n\r\n\nForschungsprojekt Jugendberatung\r\n\nProf. Dr. Elke von der Haar\r\n\nFachhochschule für Sozialarbeit und Sozialpädagogik Berlin\r\n\nKarl-Schrader-Str. 6\r\n\n\r\n\n10781 Berlin\r\n\n\r\n\n\r\n\n\r\n\n'
# demo( text )
