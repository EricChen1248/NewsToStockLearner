import json

with open("Data/stocknames.txt", "r", encoding="utf8") as stocksFile:
    stocks = stocksFile.readlines()
    for i in range(len(stocks)):
        stocks[i] = stocks[i][:-1]
    stocks = set(stocks)

with open("Data/common_stockname.txt", "r", encoding="utf8") as stocksFile:
    remove = stocksFile.readlines()
    for i in range(len(remove)):
        remove[i] = remove[i][:-1]
    stocks = stocks - set(remove)


with open("Data/!dates.txt", "r", encoding="utf-8-sig") as dateFile:
    dates = dateFile.readlines()
    for i in range(len(dates)):
        dates[i] = dates[i][:-1]

for date in dates:
    with open("Intersection/" + date + ".json", "w", encoding = "utf8") as intersectfile:
        with open("DailyNews/" + date + ".json","r", encoding = "utf-8-sig") as newsfile:
            print("Processing: " + date)
            newsSet = json.loads(newsfile.read())
            intersect = {}
            for news in newsSet["News"]:
                words = set(news["title"]).union(set(news["content"]))
                intersection = stocks & words
                intersect[news["id"]] = list(intersection)

            intersectfile.write(json.dumps(intersect, ensure_ascii=False))
