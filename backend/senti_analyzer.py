#!/usr/bin/python

import sys
import math
import nltk
from os import listdir

posStats = {}
negStats = {}

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

def create_polarity(sentidata):
    polarity = {}
    for item in sentidata:
        if len(item)==6:
            senses = item[4].split()
            for sense in senses:
                if sense.split('#')[0] not in polarity:
                    polarity[sense.split('#')[0]] = (item[2], item[3])
    return polarity

def get_polarity(text, pol, smoothing, polarity):
    result = 0
    for w in text:
        if w.lower() in polarity and polarity[w.lower()][pol]!='0':
            result += math.log(float(polarity[w.lower()][pol]))
        else:
            result += math.log(smoothing)
    return result

def process_msg(f):
    # fetch time
    f.readline()
    timeList = f.readline().split()
    time = timeList[3] + timeList[4]

    # skip to the contents
    line = f.readline()
    while len(line) > 1:
        line = f.readline()

    sentidata = load_sentidata()
    polarity = create_polarity(sentidata)
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

def read_mails(path):
    # find all emails in the folder
    mailCount = 0
    for fn in listdir(path + '/all_documents/'):
        fileName = path + '/all_documents/' + fn
        f = open(fileName, 'r')
        process_msg(f)
        f.close()
        mailCount += 1
        if mailCount % 10 == 0:
            print 'Processed ' + str(mailCount) + ' mails.'

if len(sys.argv) != 2:
    print 'Please provide the email directory, e.g. ../data/lay-k'
else:
    try:
        read_mails(sys.argv[1])
        print posStats
        print negStats
    except:
        print 'Failed to retrieve the emails'
