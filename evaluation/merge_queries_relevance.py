import engine.matcher as mt
from itertools import islice
from sklearn.metrics import precision_score
from array import array
import numpy as np
from engine.buildEngine import *




queries_file_path = 'evaluation/resources/CISI.QRY'
relevance_file_path = 'evaluation/resources/CISI.REL'
delimiter = '\n'

rq = {}
aq = {}
p = 0
r = 0
query_avg = []
queries = []


def read_file(path):
    f = open(path, 'r')
    data = f.read().split(delimiter)
    f.close()
    return data


def construct_dictionaries():
    init_DS('ds1')

    f1 = open(queries_file_path)
    arrayOfDocs1 = f1.read().split('.I ')
    arrayOfDocs1.pop(0)

    for singleDocs in arrayOfDocs1:
        if(singleDocs.find('.W') != -1 and singleDocs.find('.X') != -1):
            queries.append(singleDocs.split('.W')[1].split('.X')[0].strip())
        elif(singleDocs.find('.W') != -1):
            queries.append(singleDocs.split('.W')[1].strip())
    
    relevance = read_file(relevance_file_path)
    
    for rel in relevance :
        rel = rel.split();
        key = " ".join((queries[int(rel[0]) - 1]).split())
        if(key not in rq.keys()) :
            rq[key] = [int(rel[1])]
        else :
            rq[key].append(int(rel[1]))
            
    mt.initMatcher('ds1')
    get_precision_recall()
    # get_ranked_precision()


def get_precision_recall(): 
    
    count = 0
    qry_count = 0
    pre_tot = 0.0
    recall_tot = 0.0
    mrr = 0.0
    for query in queries:
        print(f'Performing Query {count + 1}')
        count += 1
        query = " " . join(query.split())
        aq[query] = mt.match(query)
        for i,v in enumerate(aq[query]) :
            aq[query][i] = (int)(v[0].split('doc_')[1])
          

        if(query in rq.keys()) :
            
            qry_count += 1
            arr1 = (rq[query])
            arr2 = (aq[query])
            str_right_val = 0
            for k,token in enumerate(arr2) :
                if token in arr1 :
                    str_right_val = k + 1
                    break
            
            arr = np.intersect1d(arr1 , arr2)
            if str_right_val != 0 :
                mrr += float(1 / str_right_val);
            
            recall = (float)(len(arr) / len(arr1))
            pre = (float)(len(arr) / len(arr2))
            recall_tot += recall            
            pre_tot += pre
            
            print(f'P : {pre}')
            print(f'R : {recall}')
        print('--------------------------------')
        

    print(f'AVR_P : {(float)(pre_tot / qry_count)}')
    print(f'AVR_R : {(float)(recall_tot / qry_count)}')
    print(f'MRR : {(float)(mrr / qry_count)}')

    

    # print(f'MAP = {sum(query_avg) / len(query_avg)}')
    
    
def get_ranked_precision(): 
    
    count = 0
    qry_count = 0
    pre_tot = 0.0
    recall_tot = 0.0
    mrr = 0.0
    for query in queries:
        print(f'Performing Query {count + 1}')
        count += 1
        query = " " . join(query.split())
        aq[query] = mt.match(query)
        aq[query] = aq[query][:10]
        for i,v in enumerate(aq[query]) :
            aq[query][i] = (int)(v[0].split('doc_')[1])
          

        if(query in rq.keys()) :
            qry_count += 1
            arr1 = (rq[query])
            arr2 = (aq[query])
            
            str_right_val = 0
            for k,token in enumerate(arr2) :
                if token in arr1 :
                    str_right_val = k + 1
                    break
            
            arr = np.intersect1d(arr1 , arr2)
            if str_right_val != 0 :
                mrr += float(1 / str_right_val);
            
            pre = (float)(len(arr) / float(10.0))
            recall = (float)(len(arr) / len(arr1))
            evaluate_query(query)
            pre_tot += pre
            recall_tot += recall
            print(f'P : {pre}')
            print(f'R : {recall}')
        print('--------------------------------')
        

    print(f'AVR_P : {(float)(pre_tot / qry_count)}')
    print(f'AVR_R : {(float)(recall_tot / qry_count)}')
    

    print(f'MAP = {sum(query_avg) / len(query_avg)}')
    print(f'MRR : {(float)(mrr / qry_count)}')
    

def get_recall_index(recall, recall_at_k):
    for index, element in enumerate(recall_at_k):
        if element >= recall:
            return index
    return -1


def get_ranked_precision_recall(precision_at_k, recall_at_k):
    ranked_precision = []
    ranked_recall = []
    for i in range(0, 10):
        index = get_recall_index(i / 10, recall_at_k)
        if index == -1: break
        ranked_recall.append(i / 10)
        ranked_precision.append(precision_at_k[index])
    query_avg.append(get_average_precision(ranked_precision))


def get_average_precision(ranked_precision):
    if(len(ranked_precision) == 0) :
        return 0;
    return sum(ranked_precision) / len(ranked_precision)


def evaluate_query(query):
    query_rq = rq[query]
    query_aq = aq[query]
    precision_at_k = []
    recall_at_k = []
    union = 0
    for i, entry in enumerate(query_aq):
        document = entry
        if document in query_rq:
            union += 1
        precision_at_k.append(union / (i + 1))
        recall_at_k.append(union / len(query_rq))
        if union == len(query_rq):
            break
    get_ranked_precision_recall(precision_at_k, recall_at_k)


def normal_prec_rec(query):
    global p
    global r
    query_rq = rq[query]
    query_aq = aq[query]
    union = 0
    for i, entry in enumerate(query_aq):
        document = entry[0].split('.')[0]
        if document in query_rq:
            union += 1
    p += union / len(list(query_aq))
    r += union / len(query_rq)
    print(f'P:{union / len(list(query_aq))}')
    print(f'R:{union / len(query_rq)}')


construct_dictionaries()
