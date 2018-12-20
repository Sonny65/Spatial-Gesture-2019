import nltk
from nltk import conlltags2tree, tree2conlltags
from nltk.tokenize import *

# corpus trainning data
from nltk.corpus import conll2000

# customize tagger
import nltk.tag, nltk.data
default_tagger = nltk.data.load(nltk.tag._POS_TAGGER)

# custom part of speech labels
# SADJ: adj be mistaken as none
# SV: special verb
# PRP: pronoun, personal
# LOC: predefined location on the blue print
# AS: Area and size question
model = {'dinning':'SADJ','living':'SADJ','bath':'SADJ','room':'LOC','show': 'SV_SH','put':'SV_MV'
        ,'move':'SV_MV','size':'AS',"big":"AS"}

# recontruct the tagger
tagger = nltk.tag.UnigramTagger(model=model, backoff=default_tagger)

# custom taggers for different part of the speech
# WH: Where
# SUFDESC: Description after the noun
# TAR: Target Part

chunkGram = r"""
                POS: {<SADJ><LOC>|<LOC>}
                TAR: {<PRP$.?|RB.?|JJ.?|DT>*<POS>}
                PATH: {<SV_SH><PRP><WRB><TO><VB><IN><TAR><TO><TAR>}
                SIZE: {<DT><AS>|<WRB><AS>}
                EDEICTIC_VERB_OBJ: {<WRB><MD><PRP><SV_MV>}
                EDEICTIC: {<WRB>|<SV_SH><PRP><WRB>*}
                """

# SUFDESC: {<IN><PRP$.?|RB.?|JJ.?|DT>*<NN>}
# DESC: {<PRP$.?|RB.?|JJ.?|DT>*(<PERSON><POS>)*}

def chunking(input):
    token = word_tokenize(input)

    tag = tagger.tag(token)

    nameEnt = nltk.ne_chunk(tag)

    chunkParser = nltk.RegexpParser(chunkGram)

    chunk = chunkParser.parse(nameEnt)

    return chunk

def relation_extraction(chunk):
    # sort out instruction type
    # EDEICTIC: Point to single point
    for subtree in chunk:
        if hasattr(subtree, 'label'):
            # EDEICTIC INSTRUCTION
            if subtree.label() == 'EDEICTIC':
                edeictic(chunk,'EDEICTIC')
                break
            # EDEICTIC VERB OBJ INSTRUCTION
            if subtree.label() == 'EDEICTIC_VERB_OBJ':
                edeictic(chunk,'EDEICTIC_VERB_OBJ')
                break
            # PATH ONE TO ONE
            if subtree.label() == 'PATH':
                path(subtree,'PATH')
                break
            # SIZE
            if subtree.label() == 'SIZE':
                size(chunk,'SIZE')
                break

def size(chunk,type):
    targets = []
    target = ""
    # find the target location
    for subtree in chunk:
        if hasattr(subtree, 'label'):
            if subtree.label() == 'TAR':
                for element in subtree:
                    if hasattr(element, 'label'):
                        if element.label() == 'POS':
                            for word in element:
                                target += word[0]+" "
            if target != "":
                targets += [target[:-1]]
                target = ""

    res = [type]
    for item in targets:
        res += [item]

    print res

def path(chunk,type):
    targets = []
    target = ""
    # find the target location
    for subtree in chunk:
        if hasattr(subtree, 'label'):
            if subtree.label() == 'TAR':
                for element in subtree:
                    if hasattr(element, 'label'):
                        if element.label() == 'POS':
                            for word in element:
                                target += word[0]+" "
            if target != "":
                targets += [target[:-1]]
                target = ""

    res = [type]
    for item in targets:
        res += [item]

    print res

def edeictic(chunk,type):
    targets = []
    target = ""
    # find the target location
    for subtree in chunk:
        if hasattr(subtree, 'label'):
            if subtree.label() == 'TAR':
                for element in subtree:
                    if hasattr(element, 'label'):
                        if element.label() == 'POS':
                            for word in element:
                                target += word[0]+" "
            if target != "":
                targets += [target[:-1]]
                target = ""

    res = [type]
    for item in targets:
        res += [item]

    print res

# def target(chi):


# main
while True:
    input = raw_input("Sentence:")

    chunk = chunking(input.lower())

    # print chunk

    relation_extraction(chunk)
