import json
import os
from gensim.models import Word2Vec
from gensim import corpora

FOLDER = "BagOfWords"

# Generating Model
corpus = []
files = os.listdir("DailyNews")

print("Generating Vocab")
corpus = []
for i in range(0, len(files)//3):
    fileName = files[i]
    pCount = i * 100 * 3 // len(files)
    print("Generating Vocab: (" + "#" * pCount + "-" * (100 - pCount) + ")  " + str(int(pCount / 100 * 100)) + "%   " + files[i] + "     ", end='\r') 
        
    with open("DailyNews/" + fileName, mode = "r", encoding="utf-8-sig") as file:
        newsList = json.loads(file.read())["News"]
    
    for news in newsList:
        corpus.append(news["content"])

model = Word2Vec(corpus, size=100, window=10, min_count=10, workers=16)

# Serialization and Deserialization
model.save(os.path.join(FOLDER, "corpusDictionary.dict"))
model = Word2Vec.load(os.path.join(FOLDER, "corpusDictionary.dict"))

# "上漲","看好","攀升","上揚","獲利","業績","大漲","看旺","業績","營利"
# "下跌","下挫","衰退","重挫","大跌","崩跌","暴跌","挫跌","慘跌","走跌"

model.wv.most_similar(positive=["台積電"])






