import json

with open("Data/!dates.txt", "r", encoding="utf-8-sig") as dateFile:
    dates = dateFile.readlines()
    for i in range(len(dates)):
        dates[i] = dates[i][:-1]


dayData = {}

for day in dates:
    time = { t:0 for t in range(25)}
    with open("DailyNews/" + day + ".json", mode="r", encoding = "utf-8-sig") as newsFile:
        newsList = json.loads(newsFile.read())

        for news in newsList["News"]:
            time[int(news["time"].split(":")[0])] += 1

    dayData[day] = time

with open("Data/timeDistribution.json", "w", encoding="utf8") as distFile:
    distFile.write(json.dumps(dayData))