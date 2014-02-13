#!/usr/bin/python

import sys
import math
import nltk
import json
import string
import emailAddress
from os import listdir

posStats = {}
negStats = {}
emailPositivity = {}
emailList = []
monthList = []
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

def getKey(item1):
    return item1[1].totalEmails

def getKeyMonth(item):
    data = item[0]
    month = months[data[0:3]]
    year = float(data[3:])
    return 200*year+month

def getKeyJSON(item):
    data = item
    month = months[data[0:3]]
    year = float(data[3:])
    return 200*year+month

def load_sentidata():
    f = open("SentiWordNet_3.0.0_20130122.txt")
    lines = f.readlines()
    f.close()
    sentidata = []
    for line in lines:
        if line[0]=='#' or line[0]==' ':
            continue
        sentidata.append(line.strip().split('\t'))
    return sentidata

sentidata = load_sentidata()

def create_polarity(sentidata):
    polarity = {}
    for item in sentidata:
        if len(item)==6:
            senses = item[4].split()
            for sense in senses:
                if sense.split('#')[0] not in polarity:
                    polarity[sense.split('#')[0]] = (item[2], item[3])
    return polarity

polarity = create_polarity(sentidata)

def get_polarity(text, pol, smoothing, polarity):
    result = 0
    for w in text:
        if w.lower() in polarity and polarity[w.lower()][pol]!='0':
            result += math.log(float(polarity[w.lower()][pol]))
        else:
            result += math.log(smoothing)
    return result

def process_msg(f, fileName):
    # fetch time
    f.readline()
    timeList = f.readline().split()
    time = timeList[3] + timeList[4]

    # skip to the contents
    line = f.readline()
    name=string.split(line)[1]
    while len(line) > 1:
        line = f.readline()

    smoothing = 1.0/len(polarity)

    posLikelihood = 0
    negLikelihood = 0

    line = f.readline()
    while len(line) > 0:
        posLikelihood += get_polarity(nltk.word_tokenize(line), 0,
                                      smoothing, polarity)
        negLikelihood += get_polarity(nltk.word_tokenize(line), 1,
                                      smoothing, polarity)
        line = f.readline()

    if not (time in posStats):
        posStats[time] = 0
        negStats[time] = 0

    if posLikelihood > negLikelihood:
        posStats[time] += 1
    else:
        negStats[time] += 1
    if (posLikelihood+negLikelihood) == 0:
        return 0
    try:
        emailPositivity[name].append((fileName, (posLikelihood / (posLikelihood+negLikelihood))*2-1))
    except:
        emailPositivity[name] = [(fileName, (posLikelihood / (posLikelihood+negLikelihood))*2-1)]

     # ian's code
    if time not in monthList:
        monthList.append(time)
    inList = 0
    for tempEmailList in emailList:
        if name == tempEmailList[0]:
            inList = 1
            tempEmail = tempEmailList[1]
            if posLikelihood > negLikelihood:
                tempEmail.addPosDate(time, 1)
            else:
                tempEmail.addNegDate(time, 1)
            tempEmail.totalEmails += 1
    if inList == 0:
        tempEmail = emailAddress.emailAddress(name)
        if posLikelihood > negLikelihood:
            tempEmail.addPosDate(time, 1)
        else:
            tempEmail.addNegDate(time, 1)
        tempEmail.totalEmails = 1
        emailList.append([name,tempEmail])


def read_mails(path):
    # find all emails in the folder
    mailCount = 0
    for fn in listdir(path + '/all_documents/'):
        fileName = path + '/all_documents/' + fn
        f = open(fileName, 'r')
        process_msg(f, fileName)
        f.close()
        mailCount += 1
        if mailCount % 100 == 0:
            print 'Processed ' + str(mailCount) + ' mails.'
if len(sys.argv) != 2:
    print 'Please provide the email directory, e.g. ../data/lay-k'
else:
    try:
        read_mails(sys.argv[1])
        print json.dumps(posStats)
        print json.dumps(negStats)
        with open('emailPos.json', 'w') as outfile:
            json.dump(emailPositivity, outfile)
        writeFile = open('test.json', 'w')

        #ian's code
        emailList.sort(key=getKey, reverse=True)
        maxLength = len(emailList)
        if maxLength > 10:
            maxLength = 10
        print >> writeFile, "var posData = ["
        for x in range(0,maxLength):
            temp = emailList[x]
            temp2 = temp[1]
            for month in monthList:
                if temp2.inPos(month) == False:
                    temp2.addPosDate(month, 0)
                if temp2.inNeg(month) == False:
                    temp2.addNegDate(month, 0)
            temp2.posDates.sort(key=getKeyMonth)
            temp2.negDates.sort(key=getKeyMonth)
            #print pos
            print >> writeFile, "{\"key\": \"" + temp2.email + "\","
            print >> writeFile, "\"values\" :"
            print >> writeFile, temp2.posDates
            print >> writeFile, "},"
        print >> writeFile, "];"
        print >> writeFile, "var negData = ["
        for x in range(0,maxLength):
            temp = emailList[x]
            temp2 = temp[1]
            #print pos
            print >> writeFile, "{\"key\": \"" + temp2.email + "\","
            print >> writeFile, "\"values\" :"
            print >> writeFile, temp2.negDates
            print >> writeFile, "},"
        print >> writeFile, "];"

        # convert the data into a usable format for the graphic
        posStatsList = []
        negStatsList = []
        for tempTuple in posStats.items():
            posStatsList.append(list(tempTuple))
        for tempTuple in negStats.items():
            negStatsList.append(list(tempTuple))

        posStatsList.sort(key=getKeyMonth)
        negStatsList.sort(key=getKeyMonth)

        #print the new pos and neg stats to the file
        print >> writeFile, "var stats = ["
        print >> writeFile, "{\"key\" : \"Positive Emails\" ,\n\"values\" :"
        print >> writeFile, posStatsList
        print >> writeFile, "},"
        print >> writeFile, "{\"key\" : \"Negative Emails\" ,\n\"values\" :"
        print >> writeFile, negStatsList
        print >> writeFile, "}];"
        writeFile.close()
    except:
        print 'Failed to retrieve the emails'
