import json
import numpy
from date import date
from copy import deepcopy

with open("Data/chosen_stocks.txt", "r", encoding="utf8") as stocksFile:
    stocks = stocksFile.readlines()
    for i in range(len(stocks)):
        stocks[i] = stocks[i][:-1]


for stock in stocks:
    print("Adjusting training scores", end = '\r')
    with open("MatchedWords/" + stock + ".json", mode = "r", encoding = "utf8") as wordsFile:
        words = json.loads(wordsFile.read())

    with open("MatchedWords/" + stock + "_meta.json", mode = "r", encoding = "utf8") as wordsFile:
        meta = json.loads(wordsFile.read())
        del meta["meta"]
        previous = meta["previous"]
        del meta["previous"]
    
    positives = {k: r[1] for k, r in meta.items() if r[1] != "" and r[1] > 0}
    negatives = {k: r[1] for k, r in meta.items() if r[1] != "" and r[1] < 0}

    posSum = sum(positives.values()) 
    posNorm = { day: ret / posSum for day, ret in positives.items()}
    negSum = sum(negatives.values()) 
    negNorm = { day: -ret / negSum for day, ret in negatives.items()}
    
    wordsScore = {}
    for day, word in words.items():
        totalWordCount =  sum(c for _, c in word.items())
        normWords = list(zip(word.keys(), [count / totalWordCount for _, count in word.items()]))
        lastDay = date(deepcopy(day).replace('.','/')).back().toDirString()
        try:
            if previous[lastDay][1] > 0 and day in posNorm:
                posBonus = 1.1
                negBonus = 1
            elif previous[lastDay][1] < 0 and day in negNorm:
                posBonus = 1
                negBonus = 1.1
            else:
                posBonus = 1
                negBonus = 1
        except KeyError:
            posBonus = 1
            negBonus = 1
        except TypeError:
            posBonus = 1
            negBonus = 1

        for w, count in normWords:
            wordsScore[w] = wordsScore.get(w, 0) + count * posNorm.get(day, 0) * posBonus + count * negNorm.get(day, 0) * negBonus

    stdev = numpy.std(list(wordsScore.values()), axis = 0)
    for word, count in list(wordsScore.items()):
        if abs(count) < stdev * 3:
            del wordsScore[word]
    
    with open("WordScores/" + stock + ".json", mode = "w", encoding = "utf8") as scoreFile:
        scoreFile.write(json.dumps(wordsScore, ensure_ascii=False))

    print(" " * 40, end = '\r')

    
        