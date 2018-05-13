import json
import random
import re
import threading
from date import date
from copy import deepcopy

class myThread (threading.Thread):
    def __init__(self, currentDay):
        threading.Thread.__init__(self)
        self.currentDay = currentDay

    def run(self):
        # print ("Testing: " + self.currentDay.toString())
        TestDate(deepcopy(self.currentDay))
        # print ("Completed testing for: " + self.currentDay.toString())


regex = re.compile('[\u4e00-\u9fff]')

with open("Data/chosen_stocks.txt", "r", encoding="utf8") as stocksFile:
    stocks = stocksFile.readlines()
    for i in range(len(stocks)):
        stocks[i] = stocks[i][:-1]


def TestDate(currentDay):
    for i in range(daysAgo):
        currentDay.back()

    with open("Intersection/" + currentDay.toDirString() + ".json", "r", encoding = "utf8") as intersectfile:
        intersect = json.loads(intersectfile.read())
        for k, v in list(intersect.items()):
            if stock not in v:
                del intersect[k]
        intersect = set(intersect.keys())

    articleCount = 0
    words = {}
    with open("DailyNews/" + currentDay.toDirString() + ".json","r", encoding = "utf-8-sig") as newsfile:
        newsSet = json.loads(newsfile.read())["News"]
        for news in newsSet:
            if news["id"] not in intersect:
                continue
            articleCount += 1
            for word in news["content"]:
                words[word] = words.get(word, 0) + 1

    keptWords = set(filter(regex.match, words.keys()))
    for word in list(words.keys()):
        if word not in keptWords:
            del words[word]

    totalWordCount =  sum(c for _, c in words.items())
    normWords = list(zip(words.keys(), [count / totalWordCount for _, count in words.items()]))

    dayScore = 0
    for w, count in normWords:
        dayScore += scores.get(w, 0) * count

    if dayScore * returns[day][1] < 0:
        wrongCount[0] += 1
    else:
        correct[0] += 1

for stock in stocks:
    correct = [0]
    wrongCount = [0]
    
    with open("WordScores/" + stock + ".json", mode="r", encoding="utf8") as scoreFile:
        scores = json.loads(scoreFile.read())

    with open("MatchedWords/" + stock + "_meta.json", "r", encoding="utf8") as metaFile:
        meta = json.loads(metaFile.read())
        trainingSetSize = random.randint(1, 6)
        originalOffset = meta["meta"]["Offset"]
        daysAgo = meta["meta"]["DaysAgo"]

    with open("Returns/" + stock + ".json", mode = "r", encoding = "utf8") as returnsFile:
        returns = json.loads(returnsFile.read())
    
    dates = list(sorted(list(map(date, list(returns.keys())))))
    trainingOffset = originalOffset
    while trainingOffset == originalOffset:
        trainingOffset = random.randint(0, trainingSetSize)

    dates = dates[trainingOffset::trainingSetSize]
    returns = {day: returns[day.toString()] for day in dates}

    wordsPerDay = {}
    newsPerDay = {}
    threads = []
    for day in dates:
        if returns[day][1] == "" or returns[day][1] == 0.0:
            continue
        
        
        t = myThread(deepcopy(day))
        t.start()
        threads.append(t)
        if len(threads) > 8:
            t = threads.pop(0)
            t.join()
            pCount = (correct[0] + wrongCount[0]) * 30 // len(dates) 
            print("Testing: (" + "#" * pCount + "-" * (30 - pCount) + ")  " + str(int(pCount / 30 * 100)) + "%", end='\r') 

    
    if len(threads) > 0:
        t = threads.pop(0)
        t.join()
        print("Testing: (" + "#" * pCount + "-" * (30 - pCount) + ")  " + str(int(pCount / 30 * 100)) + "%", end='\r') 

    print(stock + ": Correct: " + str(correct[0]) + " Wrong: " + str(wrongCount[0]) + " Correct Rate: " + str(round(correct[0] / (correct[0] + wrongCount[0]) * 100, 2)) + "%" + " " * 20)

