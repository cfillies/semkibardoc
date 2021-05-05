from docx import Document
from numpy import double
import schluesselregex as rex
import spacy
from spacy import displacy
from spacy.tokens import Span
from markupsafe import Markup
# from spacy.matcher import PhraseMatcher


import pathlib
import os
import json
import asyncio
import warnings
# from win32com import client
import random
from typing import Dict, Any, List, Tuple


warnings.filterwarnings("ignore", category=SyntaxWarning)
nlp = None

# all_stopwords = nlp.Defaults.stop_words

def spacy_nlp(x: str):
    global nlp
    return nlp(x)

def spacytest(s: str):
    s1 = remove_stopwords(s)
    print(s1)
    return {"nostop": s1}

def remove_stopwords(word: str) -> str:
    word = word.replace("(", " ")
    word = word.replace(")", " ")
    word = word.replace("/", " ")
    word = word.replace("II", " ")
    word = word.replace("I", " ")
    word = word.replace("Berliner ", " ")
    word = word.replace("GmbH", "")

    wl = spacy_nlp(word)
    tokens = [word for word in wl if not word.is_stop]
    return " ".join(str(x) for x in tokens)

def prepareWords(wordsjs: Dict[str,List[str]]) -> Tuple[Dict[str, Dict[str, Any]], Dict[str,List[str]]]:
    # for m in vorhabeninv['intents']:
    #     if (m == "Entwässerung"):
    #         continue
    #     if (m == "Massnahme"):
    #         continue
    #     if (m == "Brandschutz"):
    #         continue
    #     if (m == "Öffentliche Bauten"):
    #         continue
    #     if (m == "Diverse"):
    #         continue
    #     if (m == "Instandsetzung"):
    #         continue
    #     if (m == "Sicherung"):
    #         continue
    #     if (m == "Umbau"):
    #         continue
    #     if (m == "Wasserversorgungs- und Entwässerungsanlagen"):
    #         continue
    #     if (m == "hinterleuchtete , verglaste Großflächenvitrine"):
    #         continue
    #     if (m == "Umbau"):
    #         continue
    #     if (m == "wasserbauliche Anlage"):
    #         continue
    #     words0 = ''
    #     for w in vorhabeninv['intents'][m]:
    #         words0 = words0 + w + ' '
    #     words0 = remove_stopwords(words0)
    #     words0 = words0.replace("- ", " ")
    #     wdoc = spacy_nlp(words0)
    # topics[m] = wdoc

    words: Dict[str, Dict[str, Any]] = {}
    wordlist: Dict[str,List[str]] = {}
    for m in wordsjs:
        hierachy: List[str] = wordsjs[m]
        wordlist[m] = hierachy
        dim: str = ""
        if len(hierachy) == 0:
            # dimensions[m] = []
            dim = m
        else:
            dim = hierachy[len(hierachy)-1]
        if (m == "Zimmer"):
            continue
        if (m == "wasserbauliche Anlage"):
            continue
        if (m == "Ort der Leistung"):
            continue
        if (m == "solarthermische Anlage"):
            continue
        if (m == "Maßnahme"):
            continue

           # if (m == "Standsicherheit des Schornsteinkopfes"):
        #     continue
        # if (m == "Stätte der Leistung"):
        #     continue
        # if (m == "Erinnerungs- und Informationsstele"):
        #     continue

        # wdoc = spacy_nlp(m1)
        words[m] = { "dimension": dim}
    return words, wordlist

def similarity(words: Dict[str, Dict[str, Any]], wd: str, wl: str) -> float:
    wdoc: Any = None
    if wd in words:
        w: Dict[str, str] = words[wd]
        if "wdoc" in w:
            wdoc = w["wdoc"]
        else:
            m1 = remove_stopwords(wd)
            m1 = m1.replace("- ", " ")
            m1 = m1.replace(" , ", " ")
            if m1 == " " or len(m1)==0:
                return 0
            wdoc = spacy_nlp(m1)
            w["wdoc"] = wdoc
    if wdoc != None:
        if not wdoc.has_vector:
            print("No vector:", wdoc)
        return wdoc.similarity(wl)
    else:
        return 0

def preparePattern(patternjs: List[str]) -> List[Dict[str,str]]:
    plist: List[Dict[str,str]] = []
    for p in patternjs:
        patstr: str = p
        head: str = ""
        tail: str = ""
        pos: int = patstr.find("XXX")
        if pos == 0:
            tail = patstr[4:]
            pos = tail.find("YYY")
            if pos > -1:
                tail = tail[pos+4:]
            plist.append({"head": head, "tail": tail})
        elif pos > -1:
            head = patstr[:pos-1]
            tail = patstr[pos+4:]
            pos = tail.find("YYY")
            if pos > -1:
                tail = tail[pos+4:]
            plist.append({"head": head, "tail": tail})
    return plist

def matchPattern(s: str, pattern: List[Dict[str,str]]) -> str:
    s0: str = s
    sl: int = len(s)
    for p in pattern:
        h = p["head"]
        t = p["tail"]
        dt: int = s.find(t)
        if dt > 0 and dt == sl-len(t):
            if len(h) > 0:
                if s.find(h) == 0:
                    print("Pattern: ", s[len(h):sl-len(t)])
                    return s[len(h):sl-len(t)]
            else:
                print("Pattern: ", s[:sl-len(t)])
                return s[:sl-len(t)]
    return s0

def extractTopicsAndPlaces(word_cache: Dict[str, Dict[str, Any]], 
                           ontology: Dict[str,List[str]], 
                           categories: List[str], 
                           pattern: List[Dict[str,str]], badlist: List[str], 
                           bparagraphs: bool, 
                           text: str):
    # wordlistjs = wljs
    # pattern = pljs
    # badlist = bljs
    global nlp
    if nlp == None:
        nlp = spacy.load("de_core_news_md")
        # nlp = spacy.load("de")
        nlp.add_pipe('sentencizer')
    if len(text) == 0:
        try:
            source_dir = r"C:\Data\test\KIbarDok\\txt"
            os.chdir(source_dir)
            files: List[str] = sorted(os.listdir(source_dir))
            res, all_matches = asyncio.run(extractTopicsFromFiles(files, "Vorhaben:", "Grundstück:", "Grundstücke:", word_cache, 
                                                    ontology,categories, pattern,  badlist, bparagraphs))
            print(all_matches)
            return res
        except:
            pass
    else:
        no_matches = {}
        all_matches = {}
        res = extractTopicsFromText(
            "", "Vorhaben:", "Grundstück:", "Grundstücke:", word_cache, 
            ontology, categories,  pattern, badlist,bparagraphs, text,all_matches,no_matches)
        print(all_matches)
        print(no_matches)
        return res


         
        # if not nlp.has_pipe("entity_ruler"):
        #     ruler = nlp.add_pipe("entity_ruler")
        # else:
        #     ruler = nlp.get_pipe("entity_ruler")
        # patterns = [
        #             {"label": "ROLLE", "pattern": "Bundeskanzlerin"},
        #             {"label": "ROLLE", "pattern": "Gesundheitsminister"},
        #             # {"label": "GELD", "pattern": "Corona-Bonus"},
        #             # {"label": "GELD", "pattern": [{"LOWER": "Corona"}, {"LOWER": "Bonus"}]},
        #             {"label": "GELD", "pattern": "1000-Euro-Corona-Bonus"}
        #             ]
        # ruler.add_patterns(patterns)
        # ruler.overwrite_ents = False

        # doc = nlp(text)

        # new_ents = [x for x in doc.ents]
        # new_ent = Span(doc, 55, 56, label="ACHTUNG")
        # new_ents.append(new_ent)
        
        

        # matcher = PhraseMatcher(nlp.vocab)
        # patterns = [nlp.make_doc(name) for name in ["Pflegenotstand", "Pressekonferenz"]]
        # matcher.add("Names", patterns)
        # for match_id, start, end in matcher(doc):
        #      print("Matched based on lowercase token text:", doc[start:end])
        #      new_ents.append(Span(doc, start, end, label="ISSUE"))

        # doc.ents = new_ents

        # for ent in doc.ents:
        #     print(ent.text, ent.label_)          

        # colors = {"ROLLE": "red", "GELD": "yellow"}
        # options = {"ents": ["ROLLE", "GELD", "ACHTUNG", "LOC", "ISSUE"], "colors": colors}

        # html = displacy.render(doc,style="ent", options=options)
        # html = Markup(html.replace("\n\n","\n"))
        # return res , html
    
# entities: ( person: #a6e22d, norp: #e00084, facility: #43c6fc, org: #43c6fc, gpe: #fd9720, loc: #fd9720, product: #8e7dff, event: #ffcc00, work_of_art: #ffcc00, language: #ffcc00, date: #2fbbab, time: #2fbbab, percent: #999, money: #999, quantity: #999, ordinal: #999, cardinal: #999 )

def color_generator(number_of_colors: int) -> str:
        color: str = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
                 for i in range(number_of_colors)]
        return color

def displacyText(pt: str, ents: List[Any], options: Dict[ str, Any]) -> Markup:
    inp: Dict[str, any] = { "text": pt, "ents": ents, "title": None}
    html1: str = displacy.render(inp,style="ent", manual=True, options=options)
    html: Markup = Markup(html1.replace("\n\n","\n"))
    return html

def extractTopicsFromText(tfile: str,
                        pattern_topic: str, pattern_place: str, pattern_place_alt: str,
                        wordcache: Dict[str, Dict[str, Any]], 
                        ontology: Dict[str,List[str]], 
                        categories: List[str], 
                        pattern: List[str], badlist: List[str],
                        bparagraphs: bool, document: str, 
                        all_matches: Dict[str,Dict], no_matches: Dict[str, int]) -> Dict:
        topic: str = ""
        # t0: str = ""
        wordlist_list_document: List[str] = []
        intents: List[Dict] = []
        # docs_paragraph= []
        wordlist_list_category: Dict[str, List[str]] = {}
        doc: Any = spacy_nlp(document)
        paragraphs: List[str] = split_in_sentences(document)
        for p in paragraphs:
            pt: str = p
            if len(pt) > 0:
                if pt in badlist:
                    print("Badlist:", pt)
                    continue
                wnfd: bool = False
                pt2: str = matchPattern(pt, pattern)
                if pt2 != pt:
                    wnfd = True
                    pt = pt2
                # if pt.find("Bearbeiter") > -1:
                #     continue
                # # if pt.find("Bearbeiter/in") > -1:
                #     continue
                # if pt.find("Bearbeiter/in\t\tZimmer") > -1:
                #     continue
                # if pt.find("Bearbeiter/in\tZimmer") > -1:
                #     continue
                if pt.find("Dienstgebäude:") > -1:
                    continue
                # if pt.find("Dienstgebäude:\nZimmer") > -1:
                #     continue
                if pt.find("Grundstück:") > -1:
                    continue
                if pt.find("Grundstücke:") > -1:
                    continue
                if pt.find("Anlage:") > -1:
                    continue
                # if pt.find("Maßnahme") > -1:
                #         continue
                if pt.find("Anlagen:") > -1:
                    continue
                pt = pt.replace(" Anlage ", "")

                docp: Any = spacy_nlp(pt)
                # new_ents = [x for x in docp.ents]
                new_ents: List[Dict[str, Any]] = []
                # for ent in docp.ents:
                #   for h2 in hida:
                #         h2doc = hida[h2]["nlp"]
                #         h2si = h2doc.similarity(ent)
                #         if h2si > 0.95:
                # print("Hida: ", h2, " in ", ent.lemma_, str(h2si))
                wordlist_list_paragraph: List[str] = []
                for wl in docp.noun_chunks:
                    w: str = wl.lemma_
                    w = w.replace("- ", " ")
                    w = w.replace(" , ", " ")
                    w = remove_stopwords(w)
                    w = w.strip()
                    if len(w)==0:
                        continue
                    if w.find("Bezirksamt Treptow-Köpenick") > -1:
                        continue
                    if w.find("Am Treptower Park") > -1:
                        continue
                    if w.find("Grundstück") > -1:
                        continue
                    # if w.find("Maßnahme") > -1:
                    #     continue
                    if w.find("Bearbeiter") > -1:
                        continue
                    if w.find("Ort") > -1:
                        continue
                    if w.find("Seite") > -1:
                        continue
                    if w.find("\n\n\n  Gebäude") > -1:
                        continue
                    if w.find("Bezirksverordnetenversammlung") > -1:
                        continue
                    if w in no_matches:
                        no_matches[w]+=1 
                        continue
                    fnd: bool = w in ontology
                    if not fnd and w in all_matches:
                        w = all_matches[w]["w2"]
                        fnd = True
                    if not fnd and wl.has_vector:
                        matches: Dict[float, str] = {}
                        for w2 in wordcache:
                            # w2doc = words[w2]["wdoc"]
                            # w2si = w2doc.similarity(wl)
                            w2si: float = similarity(wordcache, w2, wl)
                            # print(w, " ", w2, " ", str(w2si))
                            if w2si > 0.8:
                                matches[w2si] = w2
                        if len(matches) > 0:
                            w2stlist = sorted(matches, reverse=True)
                            w2si: float = w2stlist[0]
                            w2: str = matches[w2si]
                            all_matches[w] = {"w2": w2, "s": w2si}
                            print(w, " -> ", w2, " (", str(w2si), ")")
                            w = w2
                            fnd = True
                        else:
                            no_matches[w] = 1    
                            continue
                    if fnd:
                        wnfd = True
                        dim: str = ""
                        if w in wordcache:
                            dim = wordcache[w]["dimension"]
                        if len(dim) > 0:
                            if dim in wordlist_list_category:
                                dwl = wordlist_list_category[dim]
                                if not w in dwl:
                                    dwl.append(w)
                                    wordlist_list_category[dim] = dwl
                            else:
                                wordlist_list_category[dim] = [w]
                            if not w in wordlist_list_paragraph:
                                wordlist_list_paragraph.append(w)
                            if not w in wordlist_list_document:
                                wordlist_list_document.append(w)
                            
                            # new_ents.append(Span(doc, wl.start, wl.end, label=dim.upper()))
                            new_ents.append({ "start": wl.start_char,"end": wl.end_char, "label": dim})
    
                        if w in ontology:
                            superclasses: str = ontology[w]
                            for superclass in superclasses:
                                if not superclass in wordlist_list_paragraph:
                                    dim2: str = ""
                                    if superclass in wordcache:
                                        dim2 = wordcache[superclass]["dimension"]
                                    if len(dim2) > 0:
                                        if dim2 in wordlist_list_category:
                                            dwl = wordlist_list_category[dim2]
                                            if not superclass in dwl:
                                                dwl.append(superclass)
                                                wordlist_list_category[dim2] = dwl
                                        else:
                                            wordlist_list_category[dim2] = [superclass]
                                        if not superclass in wordlist_list_paragraph:
                                            wordlist_list_paragraph.append(superclass)
                                        if not superclass in wordlist_list_document:
                                            wordlist_list_document.append(superclass)
                                        # new_ents.append(Span(doc, wl.start, wl.end, label=w.upper()))
                if wnfd == True:
                    # t0 = t0 + "\n" + p
                    # docp.ents = new_ents
                    if bparagraphs:
                        # html = displacy.render(doc,style="ent", options=options)
                        # html = displacy.render(docp,style="ent")
                        # html = Markup(html.replace("\n\n","\n"))
                        intents.append(
                            {'paragraph': p, 'words': wordlist_list_paragraph, "entities": new_ents})
                # docs_paragraph.append(docp)
        ents: List[Dict] = []
        nouns = []

        # doc = spacy_nlp(tfile.replace("_", " ").replace(
        #     ".docx", "").replace(".", " "))
       # print(tfile + ": " + str(intents))
        print(tfile)
        for e in doc.ents:
            ents.append({'lemma': e.lemma_, 'label': e.label_})
        # for e in doc.noun_chunks:
        #     nouns.append({'lemma': e.lemma_, 'label': e.label_})
        place: str = ""
        fnd: bool = False
        for p in paragraphs:
            txt: str = p
            start_topic: int = txt.find(pattern_topic)
            if start_topic != -1:
                fnd = True
                topic: str = txt[start_topic+10:].split('\n')[0]
                topic = topic.replace("\t", "")
                doc2: Any = spacy_nlp(topic)
                for e in doc2.ents:
                    ents.append({'lemma': e.lemma_, 'label': e.label_})
                for e in doc2.noun_chunks:
                    nouns.append({'lemma': e.lemma_, 'label': e.label_})
            start_place: int = txt.find(pattern_place)
            if start_place != -1:
                place = txt[start_place+12:].split('\n')[0]
                place = rex.getRegex(place).adresseUnvollständig
            else:
                start_place = txt.find(pattern_place_alt)
                if start_place != -1:
                    place = txt[start_place+13:].split('\n')[0]
                    place = rex.getRegex(place).adresseUnvollständig
        fnd = True
        if fnd:
            t = {'topic': topic, 'file': tfile.replace(".txt",".docx"),  'place': place, 
                 'keywords': wordlist_list_category, 
                 'intents': intents,
                 'nouns': nouns }
 # 'entities': ents,
            try:
                json.dumps(t)
                return t
            except:
                pass
                return {}


async def extractTopicsFromFiles(files: List[str], 
                                pattern_topic: str, pattern_place: str, pattern_place_alt: str,
                                wordcache: Dict[str, Dict[str, Any]], 
                                ontology: Dict[str,List[str]], 
                                categories: List[str], 
                                pattern: List[str], badlist: List[str],
                                bparagraphs: bool):
    tlist: List[Dict] = []
    all_matches: Dict[str,Dict] = {}
    no_matches: Dict[str, int]={}

    for i in range(0, len(files)):
        ext: str = files[i][-4:].lower()
        if ext != ".txt":
            continue
        document: str = ""
        with open(files[i]) as f:
            document = f.read()
            tfile: str = files[i]
            t: Dict = extractTopicsFromText(tfile,pattern_topic,pattern_place,pattern_place_alt,
                        wordcache,ontology, categories,pattern,badlist,bparagraphs,document, all_matches,no_matches)
            if t != {}:            
                tlist.append(t)
    
    with open('C:\\Data\\test\\topics3a.json', 'w', encoding='utf-8') as json_file:
                json.dump(tlist, json_file, indent=4, ensure_ascii=False)
    return tlist, all_matches, no_matches

def split_in_sentences(text: str) -> List[str]:
    doc = spacy_nlp(text)
    return [str(sent).strip() for sent in doc.sents]


def extractText():
        # try:
            target_dir = r"C:\Data\test\KIbarDok\\docx"
            os.chdir(target_dir)
            files = sorted(os.listdir(target_dir))
            res = asyncio.run(extractText1(files))
            return res
        # except:
        #     pass

async def extractText1(files):
    tlist = []
    for i in range(0, len(files)):
        ext = files[i][-5:].lower()
        if ext != ".docx":
            continue
        try:
            document = Document(files[i])
        except:
            continue
        doctext = ""
        for p in document.paragraphs:
            txt = p.text
            if len(txt) > 0:
                doctext = doctext + "\n" + txt
        if len(doctext)>0:
            doctext= doctext[1:]
        tfile = files[i]
        print(tfile)
        t = {'file': tfile, 'text': doctext}
        try:
            json.dumps(t)
            tlist.append(t)
        except:
            pass
    with open('C:\\Data\\test\\text3.json', 'w', encoding='utf-8') as json_file:
                json.dump(tlist, json_file, indent=4, ensure_ascii=False)
    return tlist
 
#  extractText();

def doc2docx(word, doc_path, docx_path):
    try:
        doc = word.Documents.Open(doc_path)
        doc.SaveAs(docx_path, 16)  # 16 doc2docx
        doc.Close()
    except:
        pass

#  https://docs.microsoft.com/en-us/previous-versions/office/developer/office-2003/aa220734(v=office.11)
#  https://docs.microsoft.com/en-us/office/vba/api/word.wdsaveformat
def doc2txt(word, doc_path, docx_path):
    try:
        doc = word.Documents.Open(doc_path)
        doc.SaveAs(docx_path, 2)  # wdFormatText
        doc.Close()
    except:
        pass
 
def doc2pdf(word, doc_path, docx_path):
    try:
        doc = word.Documents.Open(doc_path)
        doc.SaveAs(docx_path, 17)  # pdf
        doc.Close()
    except:
        pass

# def convert():
#     word = client.Dispatch('word.Application')

#     # path = "C:\\Data\\test\\KIbarDok\\docx"
#     # docx_path = 'C:\\Data\\test\\KIbarDok\\pdf'

#     # i = 0
#     # for root, d_names, f_names in os.walk(path):
#     #     for f in f_names:
#     #         if f.endswith(".docx"):
#     #             i = i+1
#     #             if i > 770:
#     #                 print(i, " ", f)
#     #                 doc2pdf(word, os.path.join(root, f), os.path.join(
#     #                     docx_path, f.replace(".docx", ".pdf")))  

#     path = "C:\\Data\\test\\KIbarDok\\docx"
#     docx_path = 'C:\\Data\\test\\KIbarDok\\txt'

#     i = 0
#     for root, d_names, f_names in os.walk(path):
#         for f in f_names:
#             if f.endswith(".docx"):
#                 i = i+1
#                 if i > 730:
#                     print(i, " ", f)
#                     doc2txt(word, os.path.join(root, f), os.path.join(
#                         docx_path, f.replace(".docx", ".txt")))  

#     word.Quit()
