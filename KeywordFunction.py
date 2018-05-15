import os
from gensim.models import Word2Vec
from gensim import corpora

FOLDER = "BagOfWords"
model = Word2Vec.load(os.path.join(FOLDER, "corpusDictionary.dict"))

# "上漲","看好","攀升","上揚","獲利","業績","大漲","看旺","業績","營利"
# "下跌","下挫","衰退","重挫","大跌","崩跌","暴跌","挫跌","慘跌","走跌"

def getWord(positive = None, negative = None):
    return model.wv.most_similar(positive=positive, negative=negative)

