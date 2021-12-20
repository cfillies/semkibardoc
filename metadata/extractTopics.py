# from docx import Document
# from numpy import double
import schluesselregex as rex
import spacy
from spacy import displacy
# from spacy.tokens import Span
from markupsafe import Markup
# from spacy.matcher import PhraseMatcher


# import pathlib
# import os
import json
# import asyncio
import warnings
# from win32com import client
import random
# from typing import Dict, Any, List, Tuple


warnings.filterwarnings("ignore", category=SyntaxWarning)
nlp = None
nlp1 = None

# all_stopwords = nlp.Defaults.stop_words

nlpcache = {}
nlp1cache = {}


def spacy_nlp(x: str):
    global nlpcache
    if x in nlpcache:
        return nlpcache[x]
    global nlp
    global nlp1
    if nlp == None:
        # nlp1 = spacy.load(r"C:\Data\test\kibartmp\treptowmodel2")
        # nlp1 = spacy.load("topicmodeling\hidamodel")
        nlp1 = spacy.load("de_core_news_md")
        # nlp1 = spacy.load("de_core_news_lg")
        nlp = spacy.load("de_core_news_md")
        # nlp = spacy.load("de_core_news_lg")
        # nlp = spacy.load("de")
        print(nlp.pipe_names)
        # 'tagger', 'morphologizer', 'parser', 'ner', 'attribute_ruler', 'lemmatizer'
        # nlp.disable_pipe("tagger")
        # nlp.disable_pipe("morphologizer")
        # nlp.disable_pipe("parser")

        nlp.disable_pipe("ner")
        nlp.disable_pipe("attribute_ruler")

        nlp.add_pipe('sentencizer')

        # nlp.Defaults.stop_words |= {"(",")","/","II","I","Berliner","GmbH"}
    if len(nlpcache) > 30000:
        nlpcache = {}
    if len(x) > 1000000:
        x = x[0:999998]
    y = nlp(x)
    nlpcache[x] = y
    return y


def spacy_nlp1(x: str):
    global nlp1cache
    if x in nlp1cache:
        return nlp1cache[x]
    global nlp
    global nlp1
    if nlp == None:
        # nlp1 = spacy.load("C:\Data\test\kibartmp\treptowmodel2")
        # nlp1 = spacy.load("topicmodeling\hidamodel")
        nlp1 = spacy.load("de_core_news_md")
        nlp = spacy.load("de_core_news_md")
        # nlp = spacy.load("de_core_news_lg")
        # nlp = spacy.load("de")
        print(nlp.pipe_names)
        # 'tagger', 'morphologizer', 'parser', 'ner', 'attribute_ruler', 'lemmatizer'
        # nlp.disable_pipe("tagger")
        # nlp.disable_pipe("morphologizer")
        # nlp.disable_pipe("parser")

        nlp.disable_pipe("ner")
        nlp.disable_pipe("attribute_ruler")

        nlp.add_pipe('sentencizer')

        # nlp.Defaults.stop_words |= {"(",")","/","II","I","Berliner","GmbH"}
    if len(nlp1cache) > 30000:
        nlp1cache = {}
    if len(x) > 1000000:
        x = x[0:999998]
    y = nlp1(x)
    nlp1cache[x] = y
    return y


def spacytest(s: str):
    s1 = remove_stopwords(s)
    print(s1)
    return {"nostop": s1}


def remove_stopwords(word: str) -> str:
    word = word.replace("(", " ")
    word = word.replace(")", " ")
    word = word.replace("/", " ")
    word = word.replace("II", " ")
    # word = word.replace("I", " ")
    word = word.replace("Berliner ", " ")
    word = word.replace("GmbH", "")
    wl = spacy_nlp(word)
    tokens = [word for word in wl if not word.is_stop]
    return " ".join(str(x) for x in tokens), tokens


def prepareWords(wordsjs: dict[str, dict[str]]) -> tuple[dict[str, dict[str, any]],
                                                         dict[str, list[str]]]:
    words: dict[str, dict[str, any]] = {}
    wordlist: dict[str, list[str]] = {}
    for m in wordsjs:
        hierachy: list[str] = wordsjs[m]
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
        words[m] = {"dimension": dim}
    return words, wordlist


def getVectors(words: dict[str, dict[str, any]]) -> dict[str, dict[str, any]]:
    words2 = {}
    for wd in words:
        w: dict[str, str] = words[wd]
        if "wdoc" in w:
            wdoc = w["wdoc"]
        else:
            m1 = wd.replace("- ", " ")
            m1 = m1.replace(" , ", " ")
            m1, ignore = remove_stopwords(m1)
            if m1 == " " or len(m1) == 0:
                return 0
            wdoc = spacy_nlp1(m1)
            # wdoc = spacy_nlp(m1)
            w["wdoc"] = wdoc
        if wdoc != None:
            if not wdoc.has_vector or wdoc.vector_norm == 0:
                print("No vector:", wdoc)
            else:
                words2[wd] = w
    return words2


def similarity(words: dict[str, dict[str, any]], wd: str, wl: any) -> float:
    if not wl.has_vector or wl.vector_norm == 0:
        print("No vector:", wl)
        # return 0
    wdoc: any = None
    if wd in words:
        w: dict[str, str] = words[wd]
        if "wdoc" in w:
            wdoc = w["wdoc"]
        # else:
        #     m1 = remove_stopwords(wd)
        #     m1 = m1.replace("- ", " ")
        #     m1 = m1.replace(" , ", " ")
        #     if m1 == " " or len(m1) == 0:
        #         return 0
        #     wdoc = spacy_nlp1(m1)
        #     w["wdoc"] = wdoc
    if wdoc != None:
        # if not wdoc.has_vector or wdoc.vector_norm == 0:
        #     print("No vector:", wdoc, wdoc.similarity(wl))
        #     return 0
        # else:
        sim = wdoc.similarity(wl)
        # print("Is vector:", wdoc, sim)
        return sim
    else:
        return 0


def preparePattern(patternjs: list[str]) -> list[dict[str, str]]:
    plist: list[dict[str, str]] = []
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


def matchPattern(s: str, pattern: list[dict[str, str]]) -> str:
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


# entities: ( person: #a6e22d, norp: #e00084, facility: #43c6fc, org: #43c6fc, gpe: #fd9720, loc: #fd9720, product: #8e7dff, event: #ffcc00, work_of_art: #ffcc00, language: #ffcc00, date: #2fbbab, time: #2fbbab, percent: #999, money: #999, quantity: #999, ordinal: #999, cardinal: #999 )

def color_generator(number_of_colors: int) -> str:
    color: str = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
                  for i in range(number_of_colors)]
    return color


def displacyText(pt: str, ents: list[any], options: dict[str, any]) -> Markup:
    inp: dict[str, any] = {"text": pt, "ents": ents, "title": None}
    html1: str = displacy.render(
        inp, style="ent", manual=True, options=options)
    html: Markup = Markup(html1.replace("\n\n", "\n"))
    return html


bad_phrases = [
    "Bezirksamt Treptow-Köpenick",
    "Am Treptower Park",
    "Grundstück",
    "anlage",
    "Maßnahme",
    "maßnahme",
    "Bearbeiter",
    "Bearbeiter/in",
    "Dienstgebäude:",
    "Dienstgebäude",
    "Ort",
    "Seite",
    "\n\n\n  Gebäude",
    "Bezirksverordnetenversammlung",
    "Bauen und Stadtentwicklung",
    "Bau- und Wohnungsaufsichtsamt",
    "Umgebung"
]

bad_paragraphs = [
    "Bauen, Stadtentwicklung und Umwelt",
    "Stadtentwicklung Bau- und Wohnungsaufsichtsamt",
    "Berliner Wasserbetriebe",
    "Deutsche Wohnen",
    "Berliner Bau- und Wohnungsgenossenschaft",
    "Bearbeiter",
    "Dienstgebäude",
    "Grundstück:",
    "Grundstücke:",
    "Anlage:",
    "Anlagen:",
    "Bearbeiter",
    "Bauen",
]


def extractTopicsFromText(tfile: str,
                          pattern_topic: str, pattern_place: str, pattern_place_alt: str,
                          spacywords: dict[str, dict[str, any]],
                          wordcache: dict[str, dict[str, any]],
                          ontology: dict[str, list[str]],
                          categories: list[str],
                          pattern: list[str], badlist: list[str],
                          bparagraphs: bool, document: str,
                          all_matches: dict[str, dict], no_matches: dict[str, int]) -> dict:
    global nlp
    if nlp == None:
        nlp = spacy.load("de_core_news_md")
        # nlp = spacy.load("de_core_news_lg")
        # nlp = spacy.load("de")
        nlp.add_pipe('sentencizer')

    topic: str = ""
    # t0: str = ""
    wordlist_list_document: list[str] = []
    intents: list[dict] = []
    # docs_paragraph= []
    wordlist_list_category: dict[str, list[str]] = {}
    d2 = document.replace('\n', ' ')
    paragraphs: list[str] = split_in_sentences(d2)
    for p in paragraphs:
        pt: str = p
        if len(pt) > 3:
            if pt in badlist:
                print("Badlist:", pt)
                continue
            wnfd: bool = False
            pt2: str = matchPattern(pt, pattern)
            if pt2 != pt:
                wnfd = True
                pt = pt2

            skip = False
            for bp in bad_paragraphs:
                if pt.find(bp) > -1:
                    skip = True
                    continue
            if skip:
                continue

            pt = pt.replace(" Anlage", "")

            # pt2, docp = remove_stopwords(pt)
            docp: any = spacy_nlp(pt)
            # new_ents = [x for x in docp.ents]
            new_ents: list[dict[str, any]] = []
            # for ent in docp.ents:
            #   for h2 in hida:
            #         h2doc = hida[h2]["nlp"]
            #         h2si = h2doc.similarity(ent)
            #         if h2si > 0.85:
            # print("Hida: ", h2, " in ", ent.lemma_, str(h2si))
            wordlist_list_paragraph: list[str] = []
            for wl in docp.noun_chunks:
                w: str = wl.lemma_
                if len(w) < 3:
                    continue
                w = w.replace("- ", " ")
                w = w.replace(".", " ")
                w = w.replace(" , ", " ")
                w = w.replace(", ", " ")
                w = w.replace("$", "")
                w, wl0 = remove_stopwords(w)
                w = w.strip()
                if len(w) == 0:
                    continue
                if w in bad_phrases:
                    continue
                if w.find("\n") > -1:
                    w = w.replace("\n", " ")
                w = w.replace("       ", " ")
                w = w.replace("      ", " ")
                w = w.replace("     ", " ")
                w = w.replace("    ", " ")
                w = w.replace("   ", " ")
                w = w.replace("  ", " ")
                if w in no_matches:
                    no_matches[w] += 1
                    continue
                fnd: bool = w in ontology
                m = {}
                if not fnd and w in all_matches:
                    m = all_matches[w]
                    w = m["w2"]
                    fnd = True
                if not fnd:
                    wl1 = spacy_nlp1(w)
                    # wl1 = spacy_nlp(w)
                    if wl1.vector_norm:
                        matches: dict[float, str] = {}
                        for w20 in spacywords:
                            w2si: float = similarity(wordcache, w20, wl1)
                            if w2si > 0.98:
                                # print(w, " ", w20, " ", str(w2si))
                                if not w2si in matches:
                                    matches[w2si] = set([w20])
                                else:
                                    matches[w2si].add(w20)
                        if len(matches) > 0:
                            w2stlist = sorted(matches, reverse=True)
                            w2si: float = w2stlist[0]
                            w21: str = list(matches[w2si])[0]
                            m = {"w2": w21, "s": w2si}
                            all_matches[w] = m
                            if w21.lower().find(w.lower()) == -1:
                                print(w, " -> ", w21, " (", str(w2si), ")")
                                w = w21
                                fnd = True
                        else:
                            if not w in wordcache:
                                no_matches[w] = 1
                                continue
                            else:
                                fnd = True
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
                        new_ents.append(
                            {"start": wl.start_char, "end": wl.end_char, "label": dim, "match": m})

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
                                        wordlist_list_category[dim2] = [
                                            superclass]
                                    if not superclass in wordlist_list_paragraph:
                                        wordlist_list_paragraph.append(
                                            superclass)
                                    if not superclass in wordlist_list_document:
                                        wordlist_list_document.append(
                                            superclass)
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
            # else:
            #     intents.append(
            #         {'paragraph': p, 'words': wordlist_list_paragraph, "entities": new_ents})
            # docs_paragraph.append(docp)
    ents: list[dict] = []
    nouns = []

    # doc = spacy_nlp(tfile.replace("_", " ").replace(
    #     ".docx", "").replace(".", " "))
   # print(tfile + ": " + str(intents))
    # print(tfile)
    doc: any = spacy_nlp(document)
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
            doc2: any = spacy_nlp(topic)
            for e in doc2.ents:
                ents.append({'lemma': e.lemma_, 'label': e.label_})
            for e in doc2.noun_chunks:
                nouns.append({'lemma': e.lemma_, 'label': e.label_})
        start_place: int = txt.find(pattern_place)
        if start_place != -1:
            place = txt[start_place+12:].split('\n')[0]
            place = rex.getRegex(place).adresseUnvollstaendig
        else:
            start_place = txt.find(pattern_place_alt)
            if start_place != -1:
                place = txt[start_place+13:].split('\n')[0]
                place = rex.getRegex(place).adresseUnvollstaendig
    fnd = True
    if fnd:
        t = {'topic': topic, 'file': tfile,  'place': place,
             'keywords': wordlist_list_category,
             'intents': intents,
             'nouns': nouns}
 # 'entities': ents,
        try:
            json.dumps(t)
            return t
        except:
            # pass
            return {}


def split_in_sentences(text: str) -> list[str]:
    doc = spacy_nlp(text)
    return [str(sent).strip() for sent in doc.sents]


def extractText(pattern: list[str], badlist: list[str],
                document: str,
                ) -> str:
    global nlp
    if nlp == None:
        nlp = spacy.load("de_core_news_md")
        # nlp = spacy.load("de_core_news_lg")
        # nlp = spacy.load("de")
        nlp.add_pipe('sentencizer')

    ntext = []
    d2 = document.replace('\n', ' ')
    paragraphs: list[str] = split_in_sentences(d2)
    for p in paragraphs:
        pt: str = p
        if len(pt) > 3:
            ptext = ""
            if pt in badlist:
                print("Badlist:", pt)
                continue
            pt2: str = matchPattern(pt, pattern)
            if pt2 != pt:
                pt = pt2

            skip = False
            for bp in bad_paragraphs:
                if pt.find(bp) > -1:
                    skip = True
                    continue
            if skip:
                continue

            pt = pt.replace(" Anlage ", "")

            docp: any = spacy_nlp(pt)
            for wl in docp.noun_chunks:
                w: str = wl.lemma_
                if len(w) < 3:
                    continue
                w = w.replace("- ", " ")
                w = w.replace(".", " ")
                w = w.replace(" , ", " ")
                w = w.replace("$", "")
                w, wl0 = remove_stopwords(w)
                w = w.strip()
                if len(w) == 0:
                    continue
                if w in bad_phrases:
                    continue
                if w.find("\n") > -1:
                    w = w.replace("\n", " ")
                w = w.replace("       ", " ")
                w = w.replace("      ", " ")
                w = w.replace("     ", " ")
                w = w.replace("    ", " ")
                w = w.replace("   ", " ")
                w = w.replace("  ", " ")
                ptext = ptext + w + " "
            if len(ptext) > 0:
                ntext.append(ptext)
    return ntext
