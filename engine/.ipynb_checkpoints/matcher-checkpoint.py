import numpy as np
import pandas as pd
from pandas import DataFrame
from numpy import dot
from numpy.linalg import norm
import engine.indexer as idx
from engine.preprocessing import preprocess_query, postprocess_query
from engine.query_optimizer import optimize_query , use_word_to_vec

# from processing.preprocessing import preprocess_query, postprocess_query
# from processing.query_optimizer import optimize_query

# 1 - function that creates a normalized vector in general
# 2 - convert query tokens into a normalized vector
# 3 - foreach document create a normalized vector for the query tokens
# 4 - calculate cosine distance between each document vector and query vector
# 5 - return related documents

index: DataFrame
vocabulary = set

def initMatcher(ds):
    print('init matcher ...')
    global index
    global vocabulary
    nameFile = 'index_ds1.csv' if (ds == 'ds1') else 'index_ds2.csv'
    
    try:
        index = pd.read_csv(nameFile, index_col=0)
        vocabulary = list(index.index)
        # print(vocabulary)
    except:
        docNames = []
        count = 0
        for i in idx.documents :
            docNames.append('doc_{}'.format(count))
            count += 1
        vocabulary = idx.vocabulary
        # print(vocabulary)
        index = DataFrame(data=idx.index_array, columns=docNames, index=idx.vocabulary)
        index.to_csv(nameFile)

def normalize_vector(vector):
    array = np.array(vector)
    total = array.sum()
    return array / total


def normalize_query(tokens):
    if len(tokens) == 0 :
        return np.full(len(tokens), None)
    return np.full(len(tokens), 1 / len(tokens))


def normalize_documents(index: DataFrame, query_tokens):
    documents = index.loc[query_tokens, :]
    documents_sum = documents.sum(axis=0)
    documents = documents.divide(documents_sum, axis=1).fillna(0)
    documents = documents.loc[:, (documents != 0).any(axis=0)]
    return documents


def calculate_cosine_distances(normalized_documents: DataFrame, normalized_query):
    relevant_documents = set()
    for i in range(0, len(normalized_documents.columns)):
        column = normalized_documents.iloc[:, i].to_numpy()
        relevant_documents.add(
            (normalized_documents.columns[i], dot(normalized_query, column) / (norm(normalized_query) * norm(column))))
    return sorted(relevant_documents, key=lambda tup: tup[1], reverse=True)


def match(query):
    processed_query = preprocess_query(query)
    # processed_query = optimize_query(processed_query, vocabulary)
    processed_query = use_word_to_vec(processed_query, vocabulary)
    processed_query = postprocess_query(processed_query)
    tokens = processed_query.split()
    tokens = [t for t in tokens if t in vocabulary]
    documents = normalize_documents(index, tokens)
    return calculate_cosine_distances(documents, normalize_query(tokens))

