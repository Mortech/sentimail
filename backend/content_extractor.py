#!/usr/bin/python

import sys
import math
import nltk
from os import listdir

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
    time = f.readline()

    # skip to the contents
    line = f.readline()
    while len(line) > 1:
        line = f.readline()

    sentidata = load_sentidata()
    polarity = create_polarity(sentidata)
    smoothing = 1.0/len(polarity)

    pos_likelihood = 0
    neg_likelihood = 0

    line = f.readline()
    while len(line) > 0:
        pos_likelihood += get_polarity(nltk.word_tokenize(line), 0,
                                       smoothing, polarity)
        neg_likelihood += get_polarity(nltk.word_tokenize(line), 1,
                                       smoothing, polarity)
        line = f.readline()

    return pos_likelihood > neg_likelihood

def read_mails(path):
    # find all emails in the folder
    for fn in listdir(path + '/all_documents/'):
        fileName = path + '/all_documents/' + fn
        f = open(fileName, 'r')
        print process_msg(f)
        f.close()

if len(sys.argv) != 2:
    print 'Please provide the email directory, e.g. ../data/lay-k'
else:
    try:
        read_mails(sys.argv[1])
    except:
        print 'Failed to retrieve the emails'
