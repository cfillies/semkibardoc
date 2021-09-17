

from pprint import pprint
from typing import Dict, Any, List, Tuple
import spacy
from gensim.parsing.preprocessing import preprocess_string
from gensim.models import CoherenceModel
from gensim.utils import simple_preprocess
import gensim.corpora as corpora
import gensim
import pymongo
# import json
import os
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv("MONGO_CONNECTION")
#uri = "mongodb://localhost:27017"

myclient = pymongo.MongoClient(uri)
# myclient._topology_settings

mydb = myclient["kibardoc"]


# https://www.machinelearningplus.com/nlp/topic-modeling-gensim-python/

nlp = None


def split_in_sentences(text: str) -> List[str]:
    doc = spacy_nlp(text)
    return [str(sent).strip() for sent in doc.sents]


def remove_stopwords(word: str) -> str:
    word = word.replace("(", " ")
    word = word.replace(")", " ")
    word = word.replace("/", " ")
    word = word.replace("II", " ")
    allowed_postags = ['NOUN', 'ADJ', 'VERB', 'ADV']
    wl = spacy_nlp(word)
    tokens = [
        word for word in wl if not word.is_stop and word.pos_ in allowed_postags]
    return " ".join(str(x) for x in tokens), tokens


def spacy_nlp(x: str):
    global nlp
    if nlp == None:
        nlp = spacy.load("de_core_news_md")
        nlp.disable_pipe("ner")
        nlp.disable_pipe("attribute_ruler")
        nlp.add_pipe('sentencizer')

    if len(x) > 1000000:
        x = x[0:999998]
    y = nlp(x)
    return y

# def make_bigrams(texts):
#     return [bigram_mod[doc] for doc in texts]

# def make_trigrams(texts):
#     return [trigram_mod[bigram_mod[doc]] for doc in texts]


def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    texts_out = []
    for sent in texts:
        doc = spacy_nlp(" ".join(sent))
        texts_out.append(
            [token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out


def tm_test(docs: any, word: str):
    data_words = []
    # allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']
    for doc in docs:
        txt = doc["text"]
        txt = txt.replace("\n", " ")
        paragraphs: List[str] = split_in_sentences(txt)
        print(doc["docid"], " ", doc["file"])
        for p in paragraphs:
            pt, ignore = remove_stopwords(p)
            p = preprocess_string(pt)
            if len(p) > 0:
                data_words.append(list(p))
            # print(data_words)

    with open('data_words.txt', 'w', encoding='utf-16') as f:
        pprint(data_words, f)
   # print(data_words)
    bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100)
    trigram = gensim.models.Phrases(bigram[data_words], threshold=100)
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    trigram_mod = gensim.models.phrases.Phraser(trigram)
    # print(bigram_mod)
    # print(trigram_mod)

    data_words_bigrams = [bigram_mod[doc] for doc in data_words]
    data_lemmatized = data_words_bigrams

    id2word = corpora.Dictionary(data_lemmatized)
    corpus = [id2word.doc2bow(text) for text in data_lemmatized]
    # print(corpus[:1])
    # print([[(id2word[id], freq) for id, freq in cp] for cp in corpus[0:10]])

    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                id2word=id2word,
                                                num_topics=20,
                                                random_state=100,
                                                update_every=1,
                                                chunksize=100,
                                                passes=10,
                                                alpha='auto',
                                                per_word_topics=True)

    # a measure of how good the model is. lower the better.
    print('\nPerplexity: ', lda_model.log_perplexity(corpus))

    # coherence_model_lda = CoherenceModel(model=lda_model, texts=data_lemmatized, dictionary=id2word, coherence='c_v')
    # coherence_lda = coherence_model_lda.get_coherence()
    # print('\nCoherence Score: ', coherence_lda)

    with open(word + '_internet_lda.txt', 'w', encoding='utf-16') as f:
        pprint(lda_model.print_topics(), f)


def extractDocs(word: str):
    samples = mydb["samples"]
    # extractText("C:\\Data\\test\\topics",
    #             samples, "http://localhost:9998")
    texts = []
    for s in samples.find({"path": "C:\\Data\\test\\topics\\" + word})[:]:
        texts.append(s)
    tm_test(texts, word)


# extractDocs("fenster")
# extractDocs("fassade")
# extractDocs("dachausbau")
# extractDocs("baumfällung")
# extractDocs("werbung")


def tm_test2(docs: any, word: str):
    data_words = []
    allowed_postags = ['NOUN', 'ADJ', 'VERB', 'ADV']
    # for doc in docs:
    #     txt = doc["text"]
    for p in docs:
        # txt = doc["text"]
        # txt = txt.replace("\n", " ")
        # paragraphs: List[str] = split_in_sentences(txt)
        # for p in paragraphs:
        pt, ignore = remove_stopwords(p)
        p = preprocess_string(pt)
        if len(p) > 0:
            data_words.append(list(p))
        # print(data_words)

    # print(data_words)
    bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100)
    trigram = gensim.models.Phrases(bigram[data_words], threshold=100)
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    trigram_mod = gensim.models.phrases.Phraser(trigram)
    # print(bigram_mod)
    # print(trigram_mod)

    data_words_bigrams = [bigram_mod[doc] for doc in data_words]
    data_lemmatized = data_words_bigrams

    id2word = corpora.Dictionary(data_lemmatized)
    corpus = [id2word.doc2bow(text) for text in data_lemmatized]
    # print(corpus[:1])
    # print([[(id2word[id], freq) for id, freq in cp] for cp in corpus[0:10]])

    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                id2word=id2word,
                                                num_topics=20,
                                                random_state=100,
                                                update_every=1,
                                                chunksize=100,
                                                passes=10,
                                                alpha='auto',
                                                per_word_topics=True)

    # a measure of how good the model is. lower the better.
    print('\nPerplexity: ', lda_model.log_perplexity(corpus))

    # coherence_model_lda = CoherenceModel(model=lda_model, texts=data_lemmatized, dictionary=id2word, coherence='c_v')
    # coherence_lda = coherence_model_lda.get_coherence()
    # print('\nCoherence Score: ', coherence_lda)

    with open(word + '_lda.txt', 'w', encoding='utf-16') as f:
        pprint(lda_model.print_topics(), f)


def extractDocs2(word):
    topics = mydb["topics"]
    # extractText("C:\\Data\\test\\topics",
    #             samples, "http://localhost:9998")
    texts = []
    # for s in samples.find({"path": "C:\\Data\\test\\topics\\baumfällung"})[:]:
    #     texts.append(s)
    # for s in samples.find({"path": "C:\\Data\\test\\topics\\werbung"})[:]:
    #     texts.append(s)
    # for topic in topics.find({ "intents.words": word }, { "intents.paragraph": 1, "intents.words": 1 })[:]:
    for topic in topics.find({"intents.words": word})[:]:
        for intent in topic["intents"]:
            if "words" in intent:
                words = intent["words"]
                if word in words:
                    texts.append(intent["paragraph"])
    with open(word + '_texts.txt', 'w', encoding='utf-16') as f:
        f.writelines(texts)
    tm_test2(texts, word)

# extractDocs2("Fenster")
# extractDocs2("Fassade")
# extractDocs2("Dachausbau")
# extractDocs2("Baum")


def extractDocs3():
    col = mydb["metadata2"]
    dlist = []
    for doc in col.find():
        if doc["text"] and len(doc["text"]) > 10:
            # dlist.append(doc)s
            pa = doc["path"].replace("E:\\Lichtenberg\\Dokumentationen\\","")
            fi = doc["file"] + '.txt'
            pa = pa.replace("\\","_")
            pa = 'C:\\Data\\test\\topics\\Lichtenberg\\Dokumentationen\\' + pa
            if not os.path.isdir(pa):
                os.mkdir(pa)
            file_path = os.path.join(pa, fi)
            text = doc["text"]
            text = text.replace("\n"," ")
            text = text.replace("\r"," ")
            with open(file_path, 'w', encoding='utf-16') as f:
                pprint(text, f)
    # tm_test(dlist[:1000], "")


extractDocs3()
