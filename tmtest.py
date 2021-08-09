import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

from gensim.parsing.preprocessing import preprocess_string
import spacy
from typing import Dict, Any, List, Tuple

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
    wl = spacy_nlp(word)
    tokens = [word for word in wl if not word.is_stop]
    return " ".join(str(x) for x in tokens), tokens


def spacy_nlp(x: str):
    global nlp
    if nlp == None:
        nlp = spacy.load("de_core_news_md")
        nlp.disable_pipe("ner")
        nlp.disable_pipe("attribute_ruler")
        nlp.add_pipe('sentencizer')

    y = nlp(x)
    return y


def tm_test(doc: any):
    txt = doc["text"]
    txt = txt.replace("\n", " ")
    

    paragraphs: List[str] = split_in_sentences(txt)
    data_words= []
    for p in paragraphs:
        pt, ignore = remove_stopwords(p)
        data_words.append(list(preprocess_string(pt)))
        print(data_words)
        # bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100)

    bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100)
    trigram = gensim.models.Phrases(bigram[data_words], threshold=100)
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    trigram_mod = gensim.models.phrases.Phraser(trigram)
    print(bigram_mod)
    print(trigram_mod)
