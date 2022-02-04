from sense2vec import Sense2Vec

d = "C:\\Data\\test\\kibartmp\\sense2vec\\"
o4 = d + "output4"

s2v = Sense2Vec().from_disk(o4)
query = "doppelverglasung|NOUN"
assert query in s2v
vector = s2v[query]
freq = s2v.get_freq(query)
most_similar = s2v.most_similar(query, n=10)
print(most_similar)
