#!/usr/bin/env python3
import argparse
import re
import sys
from texttable import Texttable #for output in table form
from pywordseg import * #for chinese word spegmentation
from googletrans import Translator #for english translation
from pypinyin import * #for pinyin and bopomofo
import pinyin.cedict #for dictionary if google fails

# ARGUMENTS
parser = argparse.ArgumentParser(description='A python script that reads a chinese text file and outputs the text as list of words with PinYin, BoPoMoFo, and English translation. The outputfile can be used with pandoc markdown+grid_tables format')

parser.add_argument("-i", help = "input filename")
parser.add_argument("-o", help = "output filename")
args = parser.parse_args()

if len(sys.argv) < 2:
    parser.print_help()
    sys.exit(1)

# PREPARE FILES
with open(args.i, "r") as input:
    source = input.read()

outfile = open(args.o, "w")

# PREPARE TRANSLATOR
translator = Translator()
seg = Wordseg(embedding='elmo', elmo_use_cuda=False, mode="TW")
# seg = Wordseg(embedding='w2v', elmo_use_cuda=False, mode="TW"

# prepare text
def zng(paragraph):
    for sent in re.findall(u'[^!?。？！\.\!\?]+[!?。？！\.\!\?]?', paragraph, flags=re.U):
        yield sent

sentences = list(zng(source))

# get first element from dictonary entry
def firstElement(item):
    if item is  None:
        r="-"
    else:
        r=item[0];
    return r

n  = 0
ns = len(sentences)
for source in sentences:
    n = n+1
    print(n,"/",ns," ",round(n/ns*100),'%')
    translator = Translator()
    result=seg.cut([source])[0]
    try:
        er = translator.translate(result,'en','zh-tw')
        er = [i.text for i in er]
    except:
        print("google is down")
        er = [pinyin.cedict.translate_word(i) for i in result]
        er = list(map(firstElement, er))

    t = Texttable()
    t.header(['Chinese', 'BoPoMoFo', 'PinYin', 'English'])
    i = 0
    for item in result:
        py = "".join(lazy_pinyin(item,style=Style.TONE))
        bp = "".join(lazy_pinyin(item, style=Style.BOPOMOFO))
        t.add_row([item,bp,py,er[i]])
        i = i + 1

    outfile.write(t.draw())
    outfile.write('\n\n\n\  \n\n')
    outfile.flush()

outfile.close()
