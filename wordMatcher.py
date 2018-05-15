from copy import deepcopy
from date import date
import KeywordFunction 
import random
import json
import re

TRAINING_SET_SIZE = 3
# Needs to be below 4
DAYS_AGO = 2
regex = re.compile('[\u4e00-\u9fff]')

with open("Data/stocknames.txt", "r", encoding="utf8") as stocksFile:
    allStocks = stocksFile.readlines()
    for i in range(len(allStocks)):
        allStocks[i] = allStocks[i][:-1]
    allStocks = set(allStocks)

with open("Data/chosen_stocks.txt", "r", encoding="utf8") as stocksFile:
    stocks = stocksFile.readlines()
    for i in range(len(stocks)):
        stocks[i] = stocks[i][:-1]
        
for stock in stocks:
    with open("Returns/" + stock + ".json", mode = "r", encoding = "utf8") as returnsFile:
        returns = json.loads(returnsFile.read())

    similarWords = KeywordFunction.getWord(stock)
    companies = set(map(lambda x : x[0], similarWords)) & allStocks

    dates = list(sorted(list(map(date, list(returns.keys())))))
    trainingOffset = random.randint(0, TRAINING_SET_SIZE)
    if trainingOffset - 1 < 0:
        lastD = trainingOffset - 1 + TRAINING_SET_SIZE
    else:
        lastD = trainingOffset - 1

    lastDay = dates[lastD::TRAINING_SET_SIZE]
    dates = dates[trainingOffset::TRAINING_SET_SIZE]
    lastReturns = {day: returns[day.toString()] for day in lastDay}
    returns = {day: returns[day.toString()] for day in dates}

    wordsPerDay = {}
    newsPerDay = {}
    testedDates = 0
    for day in dates:
        testedDates += 1
        if returns[day][1] == "":
            continue
        pCount = testedDates * 30 // len(dates)
        print("Training System: (" + "#" * pCount + "-" * (30 - pCount) + ")  " + str(int(pCount / 30 * 100)) + "%", end='\r') 
        currentDay = deepcopy(day)
        for i in range(DAYS_AGO):
            currentDay.back()

        with open("Intersection/" + currentDay.toDirString() + ".json", "r", encoding = "utf8") as intersectfile:
            intersect = json.loads(intersectfile.read())
            secondInt = deepcopy(intersect)
            for k, v in list(intersect.items()):
                if stock not in v:
                    del intersect[k]
            intersect = set(intersect.keys())

            for k, v in list(secondInt.items()):
                if len(set(v) & companies) == 0:
                    del secondInt[k]
            secondInt = set(secondInt)
            
        articleCount = 0
        words = {}
        with open("DailyNews/" + currentDay.toDirString() + ".json","r", encoding = "utf-8-sig") as newsfile:
            newsSet = json.loads(newsfile.read())["News"]
            for news in newsSet:
                if news["id"] in intersect:
                    articleCount += 1
                    for word in news["content"]:
                        words[word] = words.get(word, 0) + 1
                if news["id"] in secondInt:
                    for word in news["content"]:
                        words[word] = words.get(word, 0) + 0.1

        keptWords = set(filter(regex.match, words.keys()))
        for word in list(words.keys()):
            if word not in keptWords:
                del words[word]

        wordsPerDay[day.toDirString()] = words
        newsPerDay[day.toDirString()] = (articleCount, returns[day][1])

    newsPerDay["meta"] = { "Interval": TRAINING_SET_SIZE, "Offset": trainingOffset, "DaysAgo": DAYS_AGO}
    newsPerDay["previous"] = {}
    for day, ret in lastReturns.items():
        newsPerDay["previous"][day.toDirString()] = ret
    
    with open("MatchedWords/" + stock + ".json", mode = "w", encoding = "utf8") as wordsFile:
        wordsFile.write(json.dumps(wordsPerDay, ensure_ascii=False))
    
    with open("MatchedWords/" + stock + "_meta.json", mode = "w", encoding = "utf8") as wordsFile:
        wordsFile.write(json.dumps(newsPerDay, ensure_ascii=False))

    print("Training Complete!" + " " * 40)



