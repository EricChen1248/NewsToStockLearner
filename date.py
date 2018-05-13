daysPerMonth = {1:31,2:29,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}

class date:
    def __init__(self, dateStr):
        self.month = int(dateStr.split('/')[0])
        self.day = int(dateStr.split('/')[1])

    def next(self):
        self.day += 1
        if self.day > daysPerMonth[self.month]:
            self.day = 1
            self.month += 1

    def back(self):
        self.day -= 1
        if self.day <= 0:
            self.month -= 1
            self.day = daysPerMonth[self.month]
        return self

    def toString(self) -> str:
        return self.toShortString() + "/2016"
    
    def toShortString(self) -> str:
        return str(self.month) + "/" + str(self.day)

    def toDirString(self) -> str:
        return self.toString().replace('/','.')

    def equals(self, other) -> bool:
        return self.day == other.day and self.month == other.month

    def __lt__(self, other) -> bool:
        return