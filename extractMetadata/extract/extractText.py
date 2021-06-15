#!/usr/bin/env python
# coding: utf-8

import spacy
from HanTa import HanoverTagger as ht
tagger = ht.HanoverTagger('morphmodel_ger.pgz')
import docx
import re
import string
import os, zipfile, xml.dom.minidom, sys, getopt
from win32com import client as wc
import asyncio
import aiohttp
import json
import extract.extractAdresse as extractAdresse



def docxPfad(pfad, datei):
    docxPfad=pfad+'\docx\\'+datei+'x'
    currentPfad=pfad+'\\'+datei
    if datei.endswith('.doc'):
        if not os.path.exists(pfad+'\docx'):
            os.makedirs(pfad+'\docx')
        elif not os.path.exists(docxPfad):
            try:
                w = wc.Dispatch('Word.Application')
                doc=w.Documents.Open(currentPfad)
                doc.SaveAs(docxPfad,16)# Must have parameter 16, otherwise an error will occur.
                doc.Close()
                return docxPfad
            except:
                return ''
        elif os.path.exists(docxPfad):
            return docxPfad
        else:
            return ''
    elif datei.endswith('.docx'):
        return currentPfad
    else:
        return ''

    
def getInhalt(metadata, methode = 'tika', docxVorhanden = True):
    
    if type(metadata) is dict:
        pfadOriginal = next(iter(metadata))
        datei = next(iter(metadata[pfadOriginal]))
        pfad = metadata[pfadOriginal][datei]['pfadAktuell']
    if type(metadata) is list:
        # List mit Datei und Ordner, in dem es sich befindet
        pfad = metadata[1]
        datei = metadata[0]  
    
    
    content = ''
    if methode == 'tika':
        try:
            file = pfad + '\\' + datei
            content = process_data(file, "http://localhost:9998/tika", 'text')
        except:
            content = ''
            
    # elif methode == 'tika_local':        
        # from tika import parser
        # raw = parser.from_file(pfad + '\\' + datei)
        # content = raw['content']
    
    elif methode == 'docx':
        try:
            if not docxVorhanden:
                if docxPfad(pfad, datei)!='':
                    doc = docx.Document(docxPfad(pfad, datei))
                    fullText = []
                    for para in doc.paragraphs:
                        fullText.append(para.text)
                    content = '\n'.join(fullText)   
            else:
                    if datei[-4:] == 'docx':
                        # Documents have already been converted to docx
                        doc = docx.Document(pfad+'\\'+datei)
                        fullText = []
                        for para in doc.paragraphs:
                            fullText.append(para.text)
                        content = '\n'.join(fullText)
                    else:
                        content = ''
        except:
            content = ''
            
    if content == None or content =='':
        content = ''  
        
    return content


def getPageNumber(pfad,datei,methode, docxVorhanden = True):
    # if methode == 'tika':
        # from tika import parser
        # file = pfad+'\\'+datei
        # raw = parser.from_file(file)
        # try:
        #     pages=raw['metadata']['xmpTPg:NPages']
        #     if type(pages)==str:
        #         pages=int(pages)
        #     else:
        #         pages=int(max(pages))
        # except:
        #     pages='1'
    # elif methode == 'docx': 
    if methode == 'docx': 
        if not docxVorhanden:
            document = zipfile.ZipFile(docxPfad(pfad, datei))
        else:
            document = zipfile.ZipFile(pfad + '\\' + datei)
        dxml = document.read('docProps/app.xml')
        uglyXml = xml.dom.minidom.parseString(dxml)
        pages = uglyXml.getElementsByTagName('Pages')[0].childNodes[0].nodeValue
    else:
        pages='1'
    return int(pages)        
        
    
def getLemma(wordList, origWord):
    lemmaList = []
    for (word,lemma,pos) in tagger.tag_sent(wordList):
        possibleTags = [i[0] for i in tagger.tag_word(lemma,casesensitive=False,cutoff=5)]

        if possibleTags[0] in ['NE','ADJA','ADJD']:
            continue
            
        elif possibleTags[0] in ['ART']:
            if len(wordList) > 1:
                # charSplit was used but went wrong; get original word
                return [origWord]
            else:
                continue
                
        elif "denkmal" in lemma.lower():
            continue
            
        else:
            lemmaList.append(lemma)
            
    return lemmaList


def getLemmaRemvStopPunct(nlpdoc, stop_words):
    lemma_list = []
    for token in nlpdoc:
        tkLemma = token.lemma_
        try:
            splitWord = char_split.split_compound(tkLemma)
            if splitWord[0][0] > 0.9: # oder vielleicht höher? 0.9?

                wort1 = splitWord[0][1]
                wort2 = splitWord[0][2]

                wortList = [wort1,wort2]

                lemma = getLemma(wortList, tkLemma)                    
                lemma_list.extend(lemma)

            else:
                lemma = getLemma([tkLemma], tkLemma)                    
                lemma_list.extend(lemma)

        except:
                lemma = getLemma([tkLemma], tkLemma)                    
                lemma_list.extend(lemma)
    
    """
    lemma_list1 = []
    for token in doc:
        lemma_list1.append(token.lemma_)
    text_tokens = lemma_list1
    print(text_tokens)
    print(lemma_list)
    """

    # Stopwords entfernen
    #tokens_without_sw = [word for word in text_tokens if not word in all_stopwords]
    tokens_without_sw = [word for word in lemma_list if not word.lower() in stop_words]

    #Remove punctuation
    tokens_without_punct = [''.join(c for c in s if c not in string.punctuation) for s in tokens_without_sw]
    #print(tokens_without_sw)
    
    return tokens_without_punct



# Test pre-processing
def preprocessText(text, adresseMode= False, locSuche=False):
    
    nlpsp = spacy.load('de_core_news_lg')
    
    # Alternative nltk: https://towardsdatascience.com/text-normalization-with-spacy-and-nltk-1302ff430119
    
    # Überflüssige Leerzeichen im Text entfernen
    textCleanSpace = re.sub(' +', ' ', text.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ').rstrip())
    
    adressen = []
    if adresseMode:
        adressen = extractAdresse.getAdresse(text)          
    
    doc = nlpsp(textCleanSpace)
    
    all_stopwords = nlpsp.Defaults.stop_words
    
    lemmas_without_sw = getLemmaRemvStopPunct(doc, all_stopwords)

    # Remove empty strings
    tokensNotEmpty = []
    for word in lemmas_without_sw:
        if len(word) >= 3:
            tokensNotEmpty.append(word.lower())
    #tokens_without_sw = list(filter(None, tokens_without_sw))
    
    locations = []
    if locSuche:
        locations = list(set([ent.text for ent in doc.ents if ent.label_ in ['LOC']])) 
    
    return tokensNotEmpty, adressen, locations







async def extract_text(file_path, tika_url):
    async with aiohttp.ClientSession() as session:
        async with session.put(url=tika_url, data=open(file_path, 'rb')) as response:
            text_data = await response.text()
            return text_data
        
        
async def extract_meta(file_path, tika_url):
    async with aiohttp.ClientSession() as session:
        async with session.put(url=tika_url, data=open(file_path, 'rb'),headers={'Accept': 'application/json'}) as response:
            file_name = str.split(file_path, '\\')[-1]
            try:
                data = await response.text()
                if data:
                    meta_data = json.loads(data)
                    meta_data['file_name'] = file_name
                else:
                    meta_data = ''
            except Exception as ex:
                print("repsonse_failed")
            return meta_data
        
        
        
def process_data(file, tika_url, typeOfInfo):
    
    loop = asyncio.get_event_loop()
    if typeOfInfo == 'text':
        processed, unprocessed = loop.run_until_complete(asyncio.wait([extract_text(j, "http://localhost:9998/tika") for j in [file]],timeout=60))
    else:
        processed, unprocessed = loop.run_until_complete(asyncio.wait([extract_meta(j, "http://localhost:9998/tika") for j in [file]],timeout=60))
    json_data = [f.result() for f in processed]
    return json_data[0]
