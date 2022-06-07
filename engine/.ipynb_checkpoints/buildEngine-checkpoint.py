import pandas as pd
# import import_ipynb
from engine.preprocessing import *
from engine.indexer import *
from engine.matcher import *
from engine.query_optimizer import *
from engine.spellchecker import *
import gensim
from gensim.models import Word2Vec
from nltk.tokenize import sent_tokenize, word_tokenize
import engine.indexer as idx

abstractsDS1 = []
abstractsDS2 = []

model: gensim.models.word2vec.Word2Vec

def init_DS(ds) :
    global model
    if ds == 'ds1' :
        read_ds1()
        preprocess_ds1()
        # initIndex(abstractsDS1[:200])
        data = []
        for i in abstractsDS1[:200] :
            temp = []

            # tokenize the sentence into words
            for j in word_tokenize(i):
                temp.append(j.lower())

            data.append(temp)
            
        model = gensim.models.Word2Vec(data, min_count = 1, vector_size = 100, window = 5, sg = 1)
        print(type(model))
        # print(model.wv.most_similar("test")[0])
        initMatcher(ds)
              
    else :
        read_ds2()
        preprocess_ds2()
        initIndex(abstractsDS2[:200])
        data = []
        for i in abstractsDS2[:200] :
            temp = []

            # tokenize the sentence into words
            for j in word_tokenize(i):
                temp.append(j.lower())

            data.append(temp)
            
        model = gensim.models.Word2Vec(data, min_count = 1, vector_size = 100, window = 5, sg = 1)
        initMatcher(ds)

def read_ds1() :
    f1 = open('datasets/first/CISI.ALL')
    arrayOfDocs1 = f1.read().split('.I ')
    arrayOfDocs1.pop(0)


    for singleDocs in arrayOfDocs1:
        if(singleDocs.find('.W') != -1 and singleDocs.find('.X') != -1):
            abstractsDS1.append(singleDocs.split('.W')[1].split('.X')[0].strip())
        elif(singleDocs.find('.W') != -1):
            abstractsDS1.append(singleDocs.split('.W')[1])


def read_ds2():
    f2 = open('datasets/second/cacm.all')
    arrayOfDocs2 = f2.read().split('.I ')
    arrayOfDocs2.pop(0)

    for singleDocs in arrayOfDocs2:

        if(singleDocs.find('.W') != -1 ) :
            if(singleDocs.find('.B') != -1 ):
                abstractsDS2.append(singleDocs.split('.W')[1].split('.B')[0].strip())
            elif(singleDocs.find('.A') != -1):
                abstractsDS2.append(singleDocs.split('.W')[1].split('.A')[0].strip())
            elif(singleDocs.find('.K') != -1):
                abstractsDS2.append(singleDocs.split('.W')[1].split('.K')[0].strip())
            elif(singleDocs.find('.C') != -1):
                abstractsDS2.append(singleDocs.split('.W')[1].split('.C')[0].strip())
            elif(singleDocs.find('.N') != -1):
                abstractsDS2.append(singleDocs.split('.W')[1].split('.N')[0].strip())
            elif(singleDocs.find('.X') != -1):
                abstractsDS2.append(singleDocs.split('.W')[1].split('.X')[0].strip())


def preprocess_ds1():
    count = 0
    for doc in abstractsDS1 :
        abstractsDS1[count] = preprocess(doc)
        count += 1
    

def preprocess_ds2():
    count = 0
    for doc in abstractsDS2 :
        if(doc != None) :
            abstractsDS2[count] = preprocess(doc)
        count += 1
        

        
def get_model():
    return model;