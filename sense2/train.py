from parse import parse
from preprocess import preprocess
from fasttext_train_vectors import fasttext_vectors
from export import export_s2v
from precompute_cache import  precompute_cache

d = "C:\\Data\\test\\kibartmp\\sense2vec\\"
o1 = d + "output1"
o2 = d + "output2"
o3 = d + "output3"
o4 = d + "output4"

parse(d + "hida.txt",o1, "de_core_news_md",10,10000000000000)
preprocess(o1 + "//hida-1.spacy",o2,"de_core_news_md",10)
# glove_build_counts
# glove_train_vectors
fasttext_vectors(o3,o2,10,5,300,5,False,None)
export_s2v(o3 + "\\vectors.txt", o3 + "\\vocab.txt", o4, 0.0,0.0)
precompute_cache(o4,-1,100,1024,0,0,None)


