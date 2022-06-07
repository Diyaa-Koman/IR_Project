import os
import pathlib
from math import log10

tf = {}
df = {}
documents = {}
vocabulary = {}
document_tokens_count = {}
documents_count = 0
index = {}
index_array = []

    
def calculate_tf_df(data):
    global documents
    global documents_count
    global vocabulary
    documents = data
    documents_count = len(documents)
    count = 0
    for doc in documents:
        docName = 'doc_{}'.format(count)
        count+=1
        document_tokens_count[docName] = len(doc)
        for token in doc.split():
            # print(token)
            try:
                df[token].add(docName)
            except:
                df[token] = {docName}
            try:
                tf[(token, docName)] += 1
            except:
                tf[(token, docName)] = 1
    vocabulary = {x[0] for x in tf.keys()}

def get_tf(doc, term):
    return tf[(doc, term)]


def get_df(term):
    return len(df[term])


def get_vocabulary():
    return


def get_list_of_documents(data):
    return data
    # fn = pathlib.Path(__file__).parent / '../data/corpus_processed'
    # return os.listdir(fn)


def calculate_tf_idf(term, doc):
    try:
        term_tf = tf[term, doc] / document_tokens_count[doc]
    except:
        term_tf = 0
    term_df = len(df[term])
    term_idf = log10(documents_count / (term_df + 1))
    return term_tf * term_idf


def build_index():
    global index
    count = 0
    for v in vocabulary:
        for d in documents:
            docName = 'doc_{}'.format(count)
            count+=1
            try:
                index[v].add((d, calculate_tf_idf(v, docName)))
            except:
                index[v] = {(d, calculate_tf_idf(v, docName))}
        count = 0
    return index


def build_index_array():
    count = 0
    for v in vocabulary:
        row = []
        for d in documents:
            docName = 'doc_{}'.format(count)
            count+=1
            row.append(calculate_tf_idf(v, docName))
        index_array.append(row)
        count = 0
    return index_array


def initIndex(data):
    print('Building Index...')
    calculate_tf_df(data)
    build_index_array()
    print('Index built.')