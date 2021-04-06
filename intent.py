import json
import os
import spacy
# from win32com import client as wc
# import pymongo

import schluesselregex as rex
from docx import Document

nlp = spacy.load("de_core_news_lg")
nlp.add_pipe('sentencizer')
 
# all_stopwords = nlp.Defaults.stop_words


def remove_stopwords(word):
    word = word.replace("(", " ")
    word = word.replace(")", " ")
    word = word.replace("/", " ")
    word = word.replace("II", " ")
    word = word.replace("I", " ")
    word = word.replace("Berliner ", " ")
    word = word.replace("GmbH", "")

    wl = nlp(word)
    tokens = [word for word in wl if not word.is_stop]
    return " ".join(str(x) for x in tokens)


def prepareWords(wordsjs):
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
    #     wdoc = nlp(words0)
    # topics[m] = wdoc

    words = {}
    wordlist = {}
    for m in wordsjs:
        hierachy = wordsjs[m]
        wordlist[m] = hierachy
        dim = ""
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

           # if (m == "Standsicherheit des Schornsteinkopfes"):
        #     continue
        # if (m == "Stätte der Leistung"):
        #     continue
        # if (m == "Erinnerungs- und Informationsstele"):
        #     continue
        m1 = remove_stopwords(m)
        m1 = m1.replace("- ", " ")
        m1 = m1.replace(" , ", " ")

        wdoc = nlp(m1)
        words[m] = {"wdoc": wdoc, "nostop": m1, "dimension": dim}
    return words, wordlist


# badlist = []
# with open("badlist.json", encoding='utf-8') as f:
#     badlistjs = json.loads(f.read())
#     for p in badlistjs:
#         badlist.append(p["paragraph"])

# pattern = []


def preparePattern(patternjs):
    plist = []
    for p in patternjs:
        patstr = p["paragraph"]
        head = ""
        tail = ""
        pos = patstr.find("XXX")
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


def matchPattern(s, pattern):
    s0 = s
    sl = len(s)
    for p in pattern:
        h = p["head"]
        t = p["tail"]
        dt = s.find(t)
        if dt > 0 and dt == sl-len(t):
            if len(h) > 0:
                if s.find(h) == 0:
                    print("Pattern: ", s[len(h):sl-len(t)])
                    return s[len(h):sl-len(t)]
            else:
                print("Pattern: ", s[:sl-len(t)])
                return s[:sl-len(t)]
    return s0


def extractTopicsAndPlaces(words, wljs, pljs, bljs, bparagraphs, text):
    # wordlistjs = wljs
    # pattern = pljs
    # badlist = bljs
    target_dir = r"C:\Data\test\KIbarDok\\doc1"
    os.chdir(target_dir)
    files = sorted(os.listdir(target_dir))
    if len(text) == 0:
        res, all_matches = extractTopicsAndPlaces1(
            files, "Vorhaben:", "Grundstück:", "Grundstücke:", words, wljs, pljs, bljs, bparagraphs)
    else:
        res, all_matches = extractTopicsAndPlaces2(
            files, "Vorhaben:", "Grundstück:", "Grundstücke:", words, wljs, pljs, bljs, text)

    print(all_matches)
    return res


def extractTopicsAndPlaces1(files, pattern1, pattern2, pattern2ax, words, wordlistjs, pattern, badlist, bparagraphs):
    tlist = []
    all_matches = {}
    for i in range(0, len(files)):
        ext = files[i][-5:].lower()
        if ext != ".docx":
            continue
        document = Document(files[i])
        topic = ""
        t0 = ""
        wordlist_list = []
        intents = []
        wordlist_list3 = {}
        for p in document.paragraphs:
            pt = p.text
            if len(pt) > 0:
                if pt in badlist:
                    print("Badlist:", pt)
                    continue
                pt = matchPattern(pt, pattern)
                if pt.find("Bearbeiter/in\t\tZimmer") > -1:
                    continue
                if pt.find("Bearbeiter/in\tZimmer") > -1:
                    continue
                if pt.find("Dienstgebäude:\nZimmer") > -1:
                    continue
                if pt.find("Grundstück:") > -1:
                    continue
                if pt.find("Grundstücke:") > -1:
                    continue
                if pt.find("Anlage:") > -1:
                    continue
                if pt.find("Anlagen:") > -1:
                    continue
                pt = pt.replace(" Anlage ", "")

                docp = nlp(pt)
                # for ent in docp.ents:
                #   for h2 in hida:
                #         h2doc = hida[h2]["nlp"]
                #         h2si = h2doc.similarity(ent)
                #         if h2si > 0.95:
                # print("Hida: ", h2, " in ", ent.lemma_, str(h2si))
                wnfd = False
                wordlist_list2 = []
                for wl in docp.noun_chunks:
                    w = wl.lemma_
                    w = w.replace("- ", " ")
                    w = w.replace(" , ", " ")
                    w = remove_stopwords(w)
                    # tokens_without_sw= [word for word in text_tokens if not word in all_stopwords]
                    # print(tokens_without_sw)
                    # w = w.replace("die ", " ")
                    # w = w.replace("des ", " ")
                    # w = w.replace("und ", " ")
                    if w.find("Bezirksamt Treptow-Köpenick") > -1:
                        continue
                    if w.find("Am Treptower Park") > -1:
                        continue
                    if w.find("Grundstück") > -1:
                        continue
                    if w.find("Ort") > -1:
                        continue
                    fnd = w in wordlistjs
                    if w in all_matches:
                        w = all_matches[w]["w2"]
                        fnd = True
                    if not fnd:
                        matches = {}
                        for w2 in words:
                            if not fnd:
                                w2doc = words[w2]["wdoc"]
                                w2si = w2doc.similarity(wl)
                                # print(w, " ", w2, " ", str(w2si))
                                if w2si > 0.8:
                                    matches[w2si] = w2
                        if len(matches) > 0:
                            w2stlist = sorted(matches, reverse=True)
                            w2si = w2stlist[0]
                            w2 = matches[w2si]
                            all_matches[w] = {"w2": w2, "s": w2si}
                            print(w, " -> ", w2, " (", str(w2si), ")")
                            w = w2
                            fnd = True
                    if fnd:
                        wnfd = True
                        dim = ""
                        if w in words:
                            dim = words[w]["dimension"]
                        if len(dim) > 0:
                            if dim in wordlist_list3:
                                dwl = wordlist_list3[dim]
                                if not w in dwl:
                                    dwl.append(w)
                                    wordlist_list3[dim] = dwl
                            else:
                                wordlist_list3[dim] = [w]
                            if not w in wordlist_list2:
                                wordlist_list2.append(w)
                            if not w in wordlist_list:
                                wordlist_list.append(w)
                        if w in wordlistjs:
                            pl = wordlistjs[w]
                            for pp in pl:
                                if not pp in wordlist_list2:
                                    dim2 = ""
                                    if pp in words:
                                        dim2 = words[pp]["dimension"]
                                    if len(dim2) > 0:
                                        if dim2 in wordlist_list3:
                                            dwl = wordlist_list3[dim2]
                                            if not pp in dwl:
                                                dwl.append(pp)
                                                wordlist_list3[dim2] = dwl
                                        else:
                                            wordlist_list3[dim2] = [pp]
                                        if not pp in wordlist_list2:
                                            wordlist_list2.append(pp)
                                        if not pp in wordlist_list:
                                            wordlist_list.append(pp)
                if wnfd == True:
                    t0 = t0 + "\n" + p.text
                    if bparagraphs:
                        intents.append(
                            {'paragraph': p.text, 'words': wordlist_list2})
        ents = []
        nouns = []
        tfile = files[i]
        doc = nlp(tfile.replace("_", " ").replace(
            ".docx", "").replace(".", " "))
       # print(tfile + ": " + str(intents))
        print(tfile)
        for e in doc.ents:
            ents.append({'lemma': e.lemma_, 'label': e.label_})
        # for e in doc.noun_chunks:
        #     nouns.append({'lemma': e.lemma_, 'label': e.label_})
        place = ""
        fnd = False
        for p in document.paragraphs:
            txt = p.text
            start_topic = txt.find(pattern1)
            if start_topic != -1:
                fnd = True
                topic = txt[start_topic+10:].split('\n')[0]
                topic = topic.replace("\t", "")
                doc2 = nlp(topic)
                for e in doc2.ents:
                    ents.append({'lemma': e.lemma_, 'label': e.label_})
                for e in doc2.noun_chunks:
                    nouns.append({'lemma': e.lemma_, 'label': e.label_})
            start_place = txt.find(pattern2)
            if start_place != -1:
                place = txt[start_place+12:].split('\n')[0]
                place = rex.getRegex(place).adresseUnvollständig
            else:
                start_place = txt.find(pattern2ax)
                if start_place != -1:
                    place = txt[start_place+13:].split('\n')[0]
                    place = rex.getRegex(place).adresseUnvollständig
        fnd = True
        if fnd:
            t = {'topic': topic, 'file': tfile,  'place': place, 'keywords': wordlist_list3, 'intents': intents,
                 'entities': ents,  'nouns:': nouns}
            try:
                json.dumps(t)
                tlist.append(t)
            except:
                pass
    return tlist, all_matches


def split_in_sentences(text):
    doc = nlp(text)
    return [str(sent).strip() for sent in doc.sents]


def extractTopicsAndPlaces2(files, pattern1, pattern2, pattern2ax, words, wordlistjs, pattern, badlist, text):
    tlist = []
    all_matches = {}
    # for i in range(0, len(files)):
    #     ext = files[i][-5:].lower()
    #     if ext != ".docx":
    #         continue
    #     document = Document(files[i])
    topic = ""
    t0 = ""
    wordlist_list = []
    intents = []
    wordlist_list3 = {}
    paragraphs = split_in_sentences(text)

    for pt in paragraphs:
        if len(pt) > 0:
            if pt in badlist:
                print("Badlist:", pt)
                continue
            pt = matchPattern(pt, pattern)
            if pt.find("Bearbeiter/in\t\tZimmer") > -1:
                continue
            if pt.find("Bearbeiter/in\tZimmer") > -1:
                continue
            if pt.find("Dienstgebäude:\nZimmer") > -1:
                continue
            if pt.find("Grundstück:") > -1:
                continue
            if pt.find("Grundstücke:") > -1:
                continue
            if pt.find("Anlage:") > -1:
                continue
            if pt.find("Anlagen:") > -1:
                continue
            pt = pt.replace(" Anlage ", "")

            docp = nlp(pt)
            # for ent in docp.ents:
            #   for h2 in hida:
            #         h2doc = hida[h2]["nlp"]
            #         h2si = h2doc.similarity(ent)
            #         if h2si > 0.95:
            # print("Hida: ", h2, " in ", ent.lemma_, str(h2si))
            wnfd = False
            wordlist_list2 = []
            for wl in docp.noun_chunks:
                w = wl.lemma_
                w = w.replace("- ", " ")
                w = w.replace(" , ", " ")
                w = remove_stopwords(w)
                # tokens_without_sw= [word for word in text_tokens if not word in all_stopwords]
                # print(tokens_without_sw)
                # w = w.replace("die ", " ")
                # w = w.replace("des ", " ")
                # w = w.replace("und ", " ")
                if w.find("Bezirksamt Treptow-Köpenick") > -1:
                    continue
                if w.find("Am Treptower Park") > -1:
                    continue
                if w.find("Grundstück") > -1:
                    continue
                if w.find("Ort") > -1:
                    continue
                fnd = w in wordlistjs
                if w in all_matches:
                    w = all_matches[w]["w2"]
                    fnd = True
                if not fnd:
                    matches = {}
                    for w2 in words:
                        if not fnd:
                            w2doc = words[w2]["wdoc"]
                            w2si = w2doc.similarity(wl)
                            # print(w, " ", w2, " ", str(w2si))
                            if w2si > 0.8:
                                matches[w2si] = w2
                    if len(matches) > 0:
                        w2stlist = sorted(matches, reverse=True)
                        w2si = w2stlist[0]
                        w2 = matches[w2si]
                        all_matches[w] = {"w2": w2, "s": w2si}
                        print(w, " -> ", w2, " (", str(w2si), ")")
                        w = w2
                        fnd = True
                if fnd:
                    wnfd = True
                    dim = ""
                    if w in words:
                        dim = words[w]["dimension"]
                    if len(dim) > 0:
                        if dim in wordlist_list3:
                            dwl = wordlist_list3[dim]
                            if not w in dwl:
                                dwl.append(w)
                                wordlist_list3[dim] = dwl
                        else:
                            wordlist_list3[dim] = [w]
                        if not w in wordlist_list2:
                            wordlist_list2.append(w)
                        if not w in wordlist_list:
                            wordlist_list.append(w)
                    if w in wordlistjs:
                        pl = wordlistjs[w]
                        for pp in pl:
                            if not pp in wordlist_list2:
                                dim2 = ""
                                if pp in words:
                                    dim2 = words[pp]["dimension"]
                                if len(dim2) > 0:
                                    if dim2 in wordlist_list3:
                                        dwl = wordlist_list3[dim2]
                                        if not pp in dwl:
                                            dwl.append(pp)
                                            wordlist_list3[dim2] = dwl
                                    else:
                                        wordlist_list3[dim2] = [pp]
                                    if not pp in wordlist_list2:
                                        wordlist_list2.append(pp)
                                    if not pp in wordlist_list:
                                        wordlist_list.append(pp)
            if wnfd == True:
                t0 = t0 + "\n" + pt
                intents.append(
                    {'paragraph': pt, 'words': wordlist_list2})
        ents = []
        nouns = []
    #     tfile = files[i]
    #     doc = nlp(tfile.replace("_", " ").replace(
    #         ".docx", "").replace(".", " "))
    #    # print(tfile + ": " + str(intents))
    # print(tfile)
    # for e in doc.ents:
    #     ents.append({'lemma': e.lemma_, 'label': e.label_})
    # for e in doc.noun_chunks:
    #     nouns.append({'lemma': e.lemma_, 'label': e.label_})
    place = ""
    fnd = False
    for txt in paragraphs:
        start_topic = txt.find(pattern1)
        if start_topic != -1:
            fnd = True
            topic = txt[start_topic+10:].split('\n')[0]
            topic = topic.replace("\t", "")
            doc2 = nlp(topic)
            for e in doc2.ents:
                ents.append({'lemma': e.lemma_, 'label': e.label_})
            for e in doc2.noun_chunks:
                nouns.append({'lemma': e.lemma_, 'label': e.label_})
        start_place = txt.find(pattern2)
        if start_place != -1:
            place = txt[start_place+12:].split('\n')[0]
            place = rex.getRegex(place).adresseUnvollständig
        else:
            start_place = txt.find(pattern2ax)
            if start_place != -1:
                place = txt[start_place+13:].split('\n')[0]
                place = rex.getRegex(place).adresseUnvollständig
    fnd = True
    if fnd:
        t = {'topic': topic, 'file': "",  'place': place, 'keywords': wordlist_list3, 'intents': intents,
                'entities': ents,  'nouns:': nouns}
        try:
            json.dumps(t)
            tlist.append(t)
        except:
            pass
    return tlist, all_matches

# def doc2docx(doc_path, docx_path):
#     word = wc.Dispatch('word.Application')
#     try:
#         doc = word.Documents.Open(doc_path)
#         doc.SaveAs(docx_path, 16)  # 16 doc2docx
#         doc.Close()
#     except:
#         pass
#     word.Quit()


# Pfad zu den Dateien


# with open('C:\\Data\\test\\doc_intents.json', 'w', encoding='utf-8') as json_file:
#     json.dump(res, json_file, indent=4, ensure_ascii=False)

# path = "C:\\Data\\test\\KIbarDok\\Treptow"
# docx_path = 'C:\\Data\\test\\KIbarDok\\docx'

# i=0
# for root, d_names, f_names in os.walk(path):
#     for f in f_names:
#         if f.endswith(".doc"):
#             i=i+1
#             if i>1200:
#                 doc2docx(os.path.join(root, f), os.path.join(docx_path, f.replace(".doc", ".docx")))
