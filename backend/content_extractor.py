#!/usr/bin/python

import sys
import math
import nltk
from os import listdir

def get_polarity(text):
    return 1

def process_msg(f):
    # fetch time
    f.readline()
    time = f.readline()

    # skip to the contents
    line = f.readline()
    while len(line) > 1:
        line = f.readline()

    line = f.readline()
    while len(line) > 0:
        print get_polarity(line.split())
        line = f.readline()

def read_mails(path):
    # find all emails in the folder
    for fn in listdir(path + '/all_documents/'):
        fileName = path + '/all_documents/' + fn
        f = open(fileName, 'r')
        process_msg(f)
        f.close()

if len(sys.argv) != 2:
    print 'Please provide the email directory, e.g. ../data/lay-k'
else:
    try:
        read_mails(sys.argv[1])
    except:
        print 'Failed to retrieve the emails'
