# from docx import Document
from __future__ import annotations
import schluesselregex as rex
import spacy
from spacy import displacy
# from spacy.tokens import Span
from markupsafe import Markup
# from spacy.matcher import PhraseMatcher
import json
import random

nlp = None
nlpcache = {}

def spacy_nlp(x: str) -> any:
    global nlpcache
    if x in nlpcache:
        return nlpcache[x]
    global nlp
    if nlp == None:
        # nlp1 = spacy.load(r"C:\Data\test\kibartmp\treptowmodel2")
        # nlp1 = spacy.load("topicmodeling\hidamodel")
        # nlp1 = spacy.load("de_core_news_md")
        # nlp1 = spacy.load("de_core_news_lg")
        nlp = spacy.load("de_core_news_md")
        # nlp = spacy.load("de_core_news_lg")
        # nlp = spacy.load("de")
        # print(nlp.pipe_names)
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

stop_words = {"- ","."," , ",", ","$","(",")","/","II","\n"}

def remove_stopwords(word: str) -> str:
    for c in stop_words:
        word = word.replace(c, " ")

    # word = word.replace("Berliner ", " ")
    # word = word.replace("GmbH", "")
    wl = spacy_nlp(word)
    tokens = [word for word in wl if not word.is_stop]
    return " ".join(str(x) for x in tokens), tokens

def remove_blanks(w: str) -> str:
    w = w.replace("       ", " ")
    w = w.replace("      ", " ")
    w = w.replace("     ", " ")
    w = w.replace("    ", " ")
    w = w.replace("   ", " ")
    w = w.replace("  ", " ")
    return w
 

def prepareWords(wordsjs: dict[str, dict[str]]) -> tuple[dict[str, dict[str, any]],
                                                         dict[str, list[str]]]:
    word_dimension: dict[str, dict[str, any]] = {}
    word_supers: dict[str, list[str]] = {}
    for m in wordsjs:
        hierachy: list[str] = wordsjs[m]
        word_supers[m] = hierachy
        dim: str = ""
        if len(hierachy) == 0:
            # dimensions[m] = []
            dim = m
        else:
            dim = hierachy[len(hierachy)-1]
        # if (m == "Zimmer"):
        #     continue
        # if (m == "wasserbauliche Anlage"):
        #     continue
        # if (m == "Ort der Leistung"):
        #     continue
        # if (m == "solarthermische Anlage"):
        #     continue
        # if (m == "Maßnahme"):
        #     continue
        word_dimension[m] = {"dimension": dim}
    return word_dimension, word_supers

spacywords: dict[str, dict[str, any]] = []

def hasVector(w: str, corpus: str) -> bool:
    global nlp
    if nlp == None:
        loadCorpus(corpus, {})
    m1, ignore = remove_stopwords(w)
    if m1 == " " or len(m1) == 0:
        return False
    wdoc = spacy_nlp(m1)
    if not wdoc.has_vector or wdoc.vector_norm == 0:
        return False
    else:
        return True
    
def getSimilarity(w1: str, w2: str, corpus: str) -> float:
    global nlp
    if nlp == None:
        loadCorpus(corpus, {})
    m1, ignore = remove_stopwords(w1)
    if m1 == " " or len(m1) == 0:
        return 0
    wdoc1 = spacy_nlp(m1)
    if not wdoc1.has_vector or wdoc1.vector_norm == 0:
        return 0
    
    m2, ignore = remove_stopwords(w2)
    if m2 == " " or len(m2) == 0:
        return 0
    wdoc2 = spacy_nlp(m2)
    if not wdoc2.has_vector or wdoc2.vector_norm == 0:
        return 0
    return wdoc1.similarity(wdoc2)

def getSimilarityMatrix(wl1: list[str], wl2: list[str], dist: float, corpus: str) -> float:
    global nlp
    if nlp == None:
        loadCorpus(corpus, {})
    vl1: dict[str, any]= {}
    for w2 in wl1:
        m1, ignore = remove_stopwords(w2)
        if m1 == " " or len(m1) == 0:
            continue
        wdoc1 = spacy_nlp(m1)
        if not wdoc1.has_vector or wdoc1.vector_norm == 0:
            continue
        vl1[w2]=wdoc1
        
    vl2: dict[str, any] = {}
    for w2 in wl2:
        m2, ignore = remove_stopwords(w2)
        if m2 == " " or len(m2) == 0:
            continue
        wdoc2 = spacy_nlp(m2)
        if not wdoc2.has_vector or wdoc2.vector_norm == 0:
            continue
        vl2[w2]=wdoc2
    res1 = {}
    for v1 in vl1:
        w1=vl1[v1]
        res2 = {}
        for v2 in vl2:
            w2=vl2[v2]
            s = w1.similarity(w2)
            if s>dist:
                res2[v2]= s
        if res2 != {}:
            res1[v1]=res2
    return res1    

def mostSimilar(word: str, corpus: str, topn=10):
    global nlp
    if nlp == None:
        loadCorpus(corpus,{})
    ms = nlp.vocab.vectors.most_similar(
            nlp(word).vector.reshape(1,nlp(word).vector.shape[0]), n=topn)
    words = [nlp.vocab.strings[w] for w in ms[0][0]]
    distances = ms[2]
    return words, distances

def getSpacyVectors(words: dict[str, dict[str, any]], corpus: str) -> dict[str, dict[str, any]]:
    words2 = {}
    for wd in words:
        w: dict[str, str] = words[wd]
        if "wdoc" in w: 
            wdoc = w["wdoc"]
        else:
            m1, ignore = remove_stopwords(wd)
            if m1 == " " or len(m1) == 0:
                return 0
            wdoc = spacy_nlp(m1)
            w["wdoc"] = wdoc
        if wdoc != None:
            if not wdoc.has_vector or wdoc.vector_norm == 0:
                # print("No vector:", wdoc)
                pass
            else:
                words2[wd] = w
    return words2


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


spacywords: dict[str, dict[str, any]] = []


currentcorpus = ""
def loadCorpus(corpus: str, word_dimension: dict[str, dict[str, any]]):
    global currentcorpus
    global nlp
    if nlp == None or corpus != currentcorpus:
        nlp = spacy.load(corpus)
        currentcorpus = corpus
        nlp.add_pipe('sentencizer')
        nlp.disable_pipe("ner")
        nlp.disable_pipe("attribute_ruler")
        nlp.Defaults.stop_words |= stop_words
        global nlpcache
        nlpcache = {}
        if len(word_dimension) > 0:
            global spacywords
            if spacywords == []:
                spacywords = getSpacyVectors(word_dimension, corpus)

def extractIntents(word_dimension: dict[str, dict[str, any]],
                           word_supers: dict[str, list[str]],
                           categories: list[str],
                           pattern: list[dict[str, str]], badlist: list[str],
                           bparagraphs: bool,
                           text: str,
                           dist: float,
                           corpus: str):
    global nlp
    if nlp == None:
        loadCorpus(corpus, word_dimension)
        
    all_matches: dict[str, dict] = {}
    no_matches: dict[str, int] = {}
    res = _extractIntents(
        "", "Vorhaben:", "Grundstück:", "Grundstücke:", spacywords, word_dimension,
        word_supers, categories,  pattern, badlist, bparagraphs, 
        text, dist, all_matches, no_matches)
    return res, all_matches, no_matches

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


def displacyText(pt: str, ents: list[any], options: dict[str, any]) -> Markup:
    inp: dict[str, any] = {"text": pt, "ents": ents, "title": None}
    html1: str = displacy.render(
        inp, style="ent", manual=True, options=options)
    html: Markup = Markup(html1.replace("\n\n", "\n"))
    return html

def displacyTextHTML(pt: str, ents: list[any], options: dict[str, any]) -> str:
    inp: dict[str, any] = {"text": pt, "ents": ents, "title": None}
    html1: str = displacy.render(
        inp, style="ent", manual=True, options=options)
    return html1.replace("\n\n", "\n")


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

def _extractIntents(tfile: str,
                          pattern_topic: str, pattern_place: str, pattern_place_alt: str,
                          spacywords: dict[str, dict[str, any]],
                          word_dimension: dict[str, dict[str, any]],
                          ontology: dict[str, list[str]],
                          categories: list[str],
                          pattern: list[str], 
                          badlist: list[str],
                          bparagraphs: bool, 
                          document: str,
                          dist: float,
                          all_matches: dict[str, dict], 
                          no_matches: dict[str, int]) -> dict:

    topic: str = ""
    # t0: str = ""
    intents: list[dict] = []
    wordlist_list_document: list[str] = []
    wordlist_list_category: dict[str, list[str]] = {}

    d2 = document.replace('\n', ' ')
    d2 = d2.replace('\r', ' ')
    d2 = d2.replace('\t', ' ')

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
                w, wl0 = remove_stopwords(w)
                w = w.strip()
                if len(w) == 0:
                    continue
                if w in bad_phrases:
                    continue
                w = remove_blanks(w)
                if w in no_matches:
                    no_matches[w] += 1
                    continue
                fnd: bool = w in ontology
                m = {}
                foundwords = set()
                if not fnd and w in all_matches:
                    m = all_matches[w]
                    w = m["w2"]
                    foundwords.add(w)
                    fnd = True
                if not fnd:
                    wl1 = spacy_nlp(w)
                    if wl1.vector_norm:
                        matches: dict[float, str] = {}
                        matchingindices = []
                        for w20 in spacywords:
                            # w2si: float = similarity(wordcache, w20, wl1)
                            wdoc = spacywords[w20]["wdoc"]
                            w2si = wdoc.similarity(wl1)
                            if w2si > dist:
                                # print(w, " ", w20, " ", str(w2si))
                                if not w2si in matches:
                                    matches[w2si] = set([w20])
                                    matchingindices.append(w2si)
                                else:
                                    matches[w2si].add(w20)
                        if len(matches) > 0:
                            # w2stlist = sorted(matches, reverse=True)
                            w2stlist = sorted(matchingindices, reverse=True)
                            for w2si in w2stlist:
                                l = matches[w2si]
                                for mi2 in l:
                                  #  w21: str = l[mi2]
                                    w21 = mi2
                                    m = {"w2": w21, "s": w2si}
                                    all_matches[w] = m
                                    if w21.lower().find(w.lower()) == -1:
                                        print(w, " -> ", w21,
                                              " (", str(w2si), ")")
                                        # w = w21
                                        foundwords.add(w21)
                                        fnd = True
                        else:
                            if not w in word_dimension:
                                no_matches[w] = 1
                                continue
                            else:
                                fnd = True
                if fnd:
                    for fw in foundwords:
                        wnfd = True
                        dim: str = ""
                        if fw in word_dimension:
                            dim = word_dimension[fw]["dimension"]
                        if dim == "Maßnahme":
                            continue;
                        if len(dim) > 0:
                            if dim in wordlist_list_category:
                                dwl = wordlist_list_category[dim]
                                if not fw in dwl:
                                    dwl.append(fw)
                                    wordlist_list_category[dim] = dwl
                            else:
                                wordlist_list_category[dim] = [fw]
                            if not fw in wordlist_list_paragraph:
                                wordlist_list_paragraph.append(fw)
                            if not fw in wordlist_list_document:
                                wordlist_list_document.append(fw)

                            # new_ents.append(Span(doc, wl.start, wl.end, label=dim.upper()))
                            new_ents.append(
                                {"start": wl.start_char, "end": wl.end_char, "label": dim, "match": m})

                        if fw in ontology:
                            superclasses: str = ontology[fw]
                            for superclass in superclasses:
                                if not superclass in wordlist_list_paragraph:
                                    dim2: str = ""
                                    if superclass in word_dimension:
                                        dim2 = word_dimension[superclass]["dimension"]
                                        if dim2 == "Maßnahme":
                                            continue;
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

    doc: any = spacy_nlp(document)
    for e in doc.ents:
        ents.append({'lemma': e.lemma_, 'label': e.label_})
    # for e in doc.noun_chunks:
    #     nouns.append({'lemma': e.lemma_, 'label': e.label_})
    place: str = ""
    fnd: bool = False
    paragraphs = split_in_sentences(document)
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

def matchingConcepts(word_dimension: dict[str, dict[str, any]],
                           word_supers: dict[str, list[str]],
                           pattern: list[dict[str, str]], 
                           badlist: list[str],
                           text: str,
                           dist: float,
                           corpus: str):
    # wordlistjs = wljs
    # pattern = pljs
    # badlist = bljs
    global nlp
    if nlp == None:
        loadCorpus(corpus, word_dimension)

    global spacywords
    if spacywords == [] and len(word_dimension) > 0:
        spacywords = getSpacyVectors(word_dimension, corpus)

    res = _matchingConcepts(spacywords, word_supers,
        pattern, badlist, text, dist)
    return res

def _matchingConcepts(spacywords: dict[str, dict[str, any]],
                          ontology: dict[str, list[str]],
                          pattern: list[str], badlist: list[str],
                          document: str,
                          dist: float) -> dict:
    wordlist_list_document: list[str] = []
    paragraphs: list[str] = split_in_sentences(document.replace('\n', ' '))
    for p in paragraphs:
        pt: str = p
        if len(pt) > 3:
            if pt in badlist:
                continue
            pt: str = matchPattern(pt, pattern)
            skip = False
            for bp in bad_paragraphs:
                if pt.find(bp) > -1:
                    skip = True
                    continue
            if skip:
                continue

            docp: any = spacy_nlp(pt)

            for wl in docp.noun_chunks:
                w: str = wl.lemma_
                if len(w) < 3:
                    continue
                w, _ignore = remove_stopwords(w)
                w = w.strip()
                if len(w) == 0:
                    continue
                if w in bad_phrases:
                    continue
                w = remove_blanks(w)
                fnd: bool = False
                foundwords = []
                if not fnd:
                    wl1 = spacy_nlp(w)
                    if wl1.vector_norm:
                        matches: dict[float, str] = {}
                        matchingindices = []
                        for w20 in spacywords:
                            # w2si: float = similarity(wordcache, w20, wl1)
                            wdoc = spacywords[w20]["wdoc"]
                            w2si = wdoc.similarity(wl)
                            if w2si > dist:
                                # print(w, " ", w20, " ", str(w2si))
                                if not w2si in matches:
                                    matches[w2si] = set([w20])
                                    matchingindices.append(w2si)
                                else:
                                    matches[w2si].add(w20)
                        if len(matches) > 0:
                            # w2stlist = sorted(matches, reverse=True)
                            w2stlist = sorted(matchingindices, reverse=True)
                            for w2si in w2stlist:
                                l = matches[w2si]
                                for mi2 in l:
                                  #  w21: str = l[mi2]
                                    w21 = mi2
                                    m = {"w2": w21, "s": w2si}
                                    # all_matches[w] = m
                                    # if w21.lower().find(w.lower()) == -1:
                                    print(w, " -> ", w21,
                                            " (", str(w2si), ")")
                                    # w = w21
                                    foundwords.append([w21, w2si])
                                    fnd = True
                        else:
                            if not w in ontology:
                                # no_matches[w] = 1
                                continue
                            else:
                                foundwords.append([w, 1.0])
                                fnd = True
                if fnd:
                    for fw in foundwords:
                         if not fw in wordlist_list_document:
                            wordlist_list_document.append(fw)
    t = wordlist_list_document
 # 'entities': ents,
    try:
        json.dumps(t)
        return t
    except:
        return {}
    
def split_in_sentences(text: str) -> list[str]:
    doc = spacy_nlp(text)
    return [str(sent).strip() for sent in doc.sents]

def extractLemmata(document: str, corpus: str) -> list[str]:

    global nlp
    if nlp == None:
        loadCorpus(corpus, {})

    wordlist_list_document: list[str] = []
    d2 = document.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    docp: any = spacy_nlp(d2)
    for wl in docp.noun_chunks:
        w: str = wl.lemma_
        w, wl0 = remove_stopwords(w)
        w = w.strip()
        w = remove_blanks(w)
        wl1 = spacy_nlp(w)
        if wl1.vector_norm:
            wordlist_list_document.append(w)
    return wordlist_list_document

# def extractTopicsFromText(tfile: str,
#                         pattern_topic: str, pattern_place: str, pattern_place_alt: str,
#                         wordcache: dict[str, dict[str, any]],
#                         ontology: dict[str,list[str]],
#                         categories: list[str],
#                         pattern: list[str], badlist: list[str],
#                         bparagraphs: bool, document: str,
#                         all_matches: dict[str,dict], no_matches: dict[str, int]) -> dict:
#         topic: str = ""
#         # t0: str = ""
#         wordlist_list_document: list[str] = []
#         intents: list[dict] = []
#         # docs_paragraph= []
#         wordlist_list_category: dict[str, list[str]] = {}
#         doc: any = spacy_nlp(document)
#         paragraphs: list[str] = split_in_sentences(document)
#         for p in paragraphs:
#             pt: str = p
#             if len(pt) > 0:
#                 if pt in badlist:
#                     print("Badlist:", pt)
#                     continue
#                 wnfd: bool = False
#                 pt2: str = matchPattern(pt, pattern)
#                 if pt2 != pt:
#                     wnfd = True
#                     pt = pt2
#                 if pt.find("Bearbeiter") > -1:
#                     continue
#                 # # if pt.find("Bearbeiter/in") > -1:
#                 #     continue
#                 # if pt.find("Bearbeiter/in\t\tZimmer") > -1:
#                 #     continue
#                 # if pt.find("Bearbeiter/in\tZimmer") > -1:
#                 #     continue
#                 if pt.find("Dienstgebäude") > -1:
#                     continue
#                 # if pt.find("Dienstgebäude:\nZimmer") > -1:
#                 #     continue
#                 if pt.find("Grundstück:") > -1:
#                     continue
#                 if pt.find("Grundstücke:") > -1:
#                     continue
#                 if pt.find("Anlage:") > -1:
#                     continue
#                 # if pt.find("Maßnahme") > -1:
#                 #         continue
#                 if pt.find("Anlagen:") > -1:
#                     continue
#                 pt = pt.replace(" Anlage ", "")

#                 docp: any = spacy_nlp(pt)
#                 # new_ents = [x for x in docp.ents]
#                 new_ents: list[dict[str, any]] = []
#                 # for ent in docp.ents:
#                 #   for h2 in hida:
#                 #         h2doc = hida[h2]["nlp"]
#                 #         h2si = h2doc.similarity(ent)
#                 #         if h2si > 0.95:
#                 # print("Hida: ", h2, " in ", ent.lemma_, str(h2si))
#                 wordlist_list_paragraph: list[str] = []
#                 for wl in docp.noun_chunks:
#                     w: str = wl.lemma_
#                     w = w.replace("- ", " ")
#                     w = w.replace(" , ", " ")
#                     w = remove_stopwords(w)
#                     w = w.strip()
#                     if len(w)==0:
#                         continue
#                     if w.find("Bezirksamt Treptow-Köpenick") > -1:
#                         continue
#                     if w.find("Am Treptower Park") > -1:
#                         continue
#                     if w.find("Grundstück") > -1:
#                         continue
#                     # if w.find("Maßnahme") > -1:
#                     #     continue
#                     if w.find("Bearbeiter") > -1:
#                         continue
#                     if w.find("Bearbeiter/in") > -1:
#                         continue
#                     if w.find("Dienstgebäude:") > -1:
#                         continue
#                     if w.find("Dienstgebäude") > -1:
#                         continue
#                     if w.find("Ort") > -1:
#                         continue
#                     if w.find("Seite") > -1:
#                         continue
#                     if w.find("\n\n\n  Gebäude") > -1:
#                         continue
#                     if w.find("Bezirksverordnetenversammlung") > -1:
#                         continue
#                     if w in no_matches:
#                         no_matches[w]+=1
#                         continue
#                     fnd: bool = w in ontology
#                     m = {}
#                     if not fnd and w in all_matches:
#                         m = all_matches[w]
#                         w = m["w2"]
#                         fnd = True
#                     if not fnd and wl.has_vector:
#                         matches: dict[float, str] = {}
#                         for w2 in wordcache:
#                             # w2doc = words[w2]["wdoc"]
#                             # w2si = w2doc.similarity(wl)
#                             w2si: float = similarity(wordcache, w2, wl)
#                             # print(w, " ", w2, " ", str(w2si))
#                             if w2si > 0.8:
#                                 matches[w2si] = w2
#                         if len(matches) > 0:
#                             w2stlist = sorted(matches, reverse=True)
#                             w2si: float = w2stlist[0]
#                             w2: str = matches[w2si]
#                             m = {"w2": w2, "s": w2si}
#                             all_matches[w] = m
#                             print(w, " -> ", w2, " (", str(w2si), ")")
#                             w = w2
#                             fnd = True
#                         else:
#                             no_matches[w] = 1
#                             continue
#                     if fnd:
#                         wnfd = True
#                         dim: str = ""
#                         if w in wordcache:
#                             dim = wordcache[w]["dimension"]
#                         if len(dim) > 0:
#                             if dim in wordlist_list_category:
#                                 dwl = wordlist_list_category[dim]
#                                 if not w in dwl:
#                                     dwl.append(w)
#                                     wordlist_list_category[dim] = dwl
#                             else:
#                                 wordlist_list_category[dim] = [w]
#                             if not w in wordlist_list_paragraph:
#                                 wordlist_list_paragraph.append(w)
#                             if not w in wordlist_list_document:
#                                 wordlist_list_document.append(w)

#                             # new_ents.append(Span(doc, wl.start, wl.end, label=dim.upper()))
#                             new_ents.append({ "start": wl.start_char,"end": wl.end_char, "label": dim, "match": m})

#                         if w in ontology:
#                             superclasses: str = ontology[w]
#                             for superclass in superclasses:
#                                 if not superclass in wordlist_list_paragraph:
#                                     dim2: str = ""
#                                     if superclass in wordcache:
#                                         dim2 = wordcache[superclass]["dimension"]
#                                     if len(dim2) > 0:
#                                         if dim2 in wordlist_list_category:
#                                             dwl = wordlist_list_category[dim2]
#                                             if not superclass in dwl:
#                                                 dwl.append(superclass)
#                                                 wordlist_list_category[dim2] = dwl
#                                         else:
#                                             wordlist_list_category[dim2] = [superclass]
#                                         if not superclass in wordlist_list_paragraph:
#                                             wordlist_list_paragraph.append(superclass)
#                                         if not superclass in wordlist_list_document:
#                                             wordlist_list_document.append(superclass)
#                                         # new_ents.append(Span(doc, wl.start, wl.end, label=w.upper()))
#                 if wnfd == True:
#                     # t0 = t0 + "\n" + p
#                     # docp.ents = new_ents
#                     if bparagraphs:
#                         # html = displacy.render(doc,style="ent", options=options)
#                         # html = displacy.render(docp,style="ent")
#                         # html = Markup(html.replace("\n\n","\n"))
#                         intents.append(
#                             {'paragraph': p, 'words': wordlist_list_paragraph, "entities": new_ents})
#                 # else:
#                 #     intents.append(
#                 #         {'paragraph': p, 'words': wordlist_list_paragraph, "entities": new_ents})
#                 # docs_paragraph.append(docp)
#         ents: list[dict] = []
#         nouns = []
# 
#         #     ".docx", "").replace(".", " "))
#        # print(tfile + ": " + str(intents))
#         print(tfile)
#         for e in doc.ents:
#             ents.append({'lemma': e.lemma_, 'label': e.label_})
#         # for e in doc.noun_chunks:
#         #     nouns.append({'lemma': e.lemma_, 'label': e.label_})
#         place: str = ""
#         fnd: bool = False
#         for p in paragraphs:
#             txt: str = p
#             start_topic: int = txt.find(pattern_topic)
#             if start_topic != -1:
#                 fnd = True
#                 topic: str = txt[start_topic+10:].split('\n')[0]
#                 topic = topic.replace("\t", "")
#                 doc2: any = spacy_nlp(topic)
#                 for e in doc2.ents:
#                     ents.append({'lemma': e.lemma_, 'label': e.label_})
#                 for e in doc2.noun_chunks:
#                     nouns.append({'lemma': e.lemma_, 'label': e.label_})
#             start_place: int = txt.find(pattern_place)
#             if start_place != -1:
#                 place = txt[start_place+12:].split('\n')[0]
#                 place = rex.getRegex(place).adresseUnvollstaendig
#             else:
#                 start_place = txt.find(pattern_place_alt)
#                 if start_place != -1:
#                     place = txt[start_place+13:].split('\n')[0]
#                     place = rex.getRegex(place).adresseUnvollstaendig
#         fnd = True
#         if fnd:
#             t = {'topic': topic, 'file': tfile.replace(".txt",".docx"),  'place': place,
#                  'keywords': wordlist_list_category,
#                  'intents': intents,
#                  'nouns': nouns }
#  # 'entities': ents,
#             try:
#                 json.dumps(t)
#                 return t
#             except:
#                 pass
#                 return {}


# async def extractTopicsFromFiles(files: list[str],
#                                 pattern_topic: str, pattern_place: str, pattern_place_alt: str,
#                                 wordcache: dict[str, dict[str, any]],
#                                 ontology: dict[str,list[str]],
#                                 categories: list[str],
#                                 pattern: list[str], badlist: list[str],
#                                 bparagraphs: bool):
#     tlist: list[dict] = []
#     all_matches: dict[str,dict] = {}
#     no_matches: dict[str, int]={}

#     for i in range(0, len(files)):
#         ext: str = files[i][-4:].lower()
#         if ext != ".txt":
#             continue
#         document: str = ""
#         with open(files[i]) as f:
#             document = f.read()
#             tfile: str = files[i]
#             t: dict = extractTopicsFromText(tfile,pattern_topic,pattern_place,pattern_place_alt,
#                         wordcache,ontology, categories,pattern,badlist,bparagraphs,document, all_matches,no_matches)
#             if t != {}:
#                 tlist.append(t)


#     return tlist, all_matches, no_matches

# def extractText():
#         # try:
#             target_dir = r"C:\Data\test\KIbarDok\\docx"
#             os.chdir(target_dir)
#             files = sorted(os.listdir(target_dir))
#             res = asyncio.run(extractText1(files))
#             return res
#         # except:
#         #     pass

# async def extractText1(files):
#     tlist = []
#     for i in range(0, len(files)):
#         ext = files[i][-5:].lower()
#         if ext != ".docx":
#             continue
#         try:
#             document = Document(files[i])
#         except:
#             continue
#         doctext = ""
#         for p in document.paragraphs:
#             txt = p.text
#             if len(txt) > 0:
#                 doctext = doctext + "\n" + txt
#         if len(doctext)>0:
#             doctext= doctext[1:]
#         tfile = files[i]
#         print(tfile)
#         t = {'file': tfile, 'text': doctext}
#         try:
#             json.dumps(t)
#             tlist.append(t)
#         except:
#             pass
#     with open('C:\\Data\\test\\text3.json', 'w', encoding='utf-8') as json_file:
#                 json.dump(tlist, json_file, indent=4, ensure_ascii=False)
#     return tlist

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
# def doc2txt(word, doc_path, docx_path):
#     try:
#         doc = word.Documents.Open(doc_path)
#         doc.SaveAs(docx_path, 2)  # wdFormatText
#         doc.Close()
#     except:
#         pass

# def doc2pdf(word, doc_path, docx_path):
#     try:
#         doc = word.Documents.Open(doc_path)
#         doc.SaveAs(docx_path, 17)  # pdf
#         doc.Close()
#     except:
#         pass

# def convert():
#      word = client.Dispatch('word.Application')

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
