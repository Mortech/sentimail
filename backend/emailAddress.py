__author__ = 'Ian'
class emailAddress:

    def __init__(self, fileName):
        self.email = fileName
        self.posDates = []
        self.negDates = []
        self.totalEmails = 0

    def addPosDate(self, date, bool):
        inDates = 0
        for temp in self.posDates:
            if temp[0] == date:
                temp[1] += 1
                inDates = 1
                break
        if inDates == 0:
            if bool == 1:
                self.posDates.append([date,1])
            else:
                self.posDates.append([date,0])
    def addNegDate(self, date, bool):
        inDates = 0
        for temp in self.negDates:
            if temp[0] == date:
                temp[1] += 1
                inDates = 1
                break
        if inDates == 0:
            if bool == 1:
                self.negDates.append([date,1])
            else:
                self.negDates.append([date,0])

    def inPos(self, time):
        for temp in self.posDates:
            if temp[0] == time:
                return True
        return False

    def inNeg(self, time):
        for temp in self.negDates:
            if temp[0] == time:
                return True
        return False

    email = ''
    months = {
        "Jan" : 1,
        "Feb" : 2,
        "Mar" : 3,
        "Apr" : 4,
        "May" : 5,
        "Jun" : 6,
        "Jul" : 7,
        "Aug" : 8,
        "Sep" : 9,
        "Oct" : 10,
        "Nov" : 11,
        "Dec" : 12
    }