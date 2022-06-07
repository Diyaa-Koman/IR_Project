import pathlib

from num2words import num2words
from nltk.corpus import stopwords
from nltk import ngrams
import re
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer

n = 3

def convert_lower_case(data):
    return data.lower()


def remove_punctuation(data):
    symbols = "!\"#$%&()*+-/:;<=>?@[\]^_`{|}~,\n"
    for i in symbols:
        data = data.replace(i, ' ')
    return data


def remove_apostrophe(data):
    data = data.replace('\'', '')
    return data

def remove_dots(data):
    data = data.replace('.', ' ')
    return data

def remove_single_characters(data):
    new_text = ""
    for w in data.split():
        if len(w) > 1:
            new_text += w + ' '
    return new_text


def convert_numbers(data):
    for w in data.split():
        if w.isnumeric():
            data = data.replace(w, num2words(w))
    return data


def remove_stop_words(data):
    stop_words = set(stopwords.words('english'))
    new_text = ''
    for w in data.split():
        if w not in stop_words:
            new_text += w + ' '

    return new_text

def stemming(data) :

    ps = PorterStemmer()

    normalized_text= ''
    for w in data.split():
        normalized_text += ps.stem(w) + ' '

    return normalized_text


def lemmatisation(data):

    lemmatizer = WordNetLemmatizer()

    normalized_text = ''

    for token in data.split() :
        normalized_text += lemmatizer.lemmatize(token) + ' '
        
    return normalized_text


dictionary = {
    "u.s": "united states",
    "u.s.a": "united states of america",
    "u.n": "united nations",
    "r.p.f": "rally of the french people",
    "s.a.o": "secret army organisation",
    "i.e": "example",
    "m.p.s": "member of parliament of the united kingdom",
    "m.p": "member of the house of lords",
}


def expand(text: str):
    for key in dictionary.keys():
        text = text.replace(key, dictionary[key])
    return text


def reduce(text: str):
    abbreviations = re.findall(r"\w\.\w[.\w]*", text)
    for exp in abbreviations:
        text = text.replace(exp, exp.replace(".", ""))
    dash_separated = re.findall(r"\w-\w[-\w]*", text)
    for exp in dash_separated:
        text = text.replace(exp, exp.replace("-", ""))
    return text


def normalize(text):
    text = expand(text)
    text = reduce(text)
    return text

def extract_k_grams(text):
    the_grams = []
    for k in range(2, n+1):
        grams = ngrams(text.split(), k)
        for gram in grams:
            the_grams.append(''.join(list(gram)))

    return the_grams

def add_k_grams(data):
    data_with_grams = data
    k_grams = extract_k_grams(data)
    for item in k_grams:
        data_with_grams += ' ' + item
    return data_with_grams


def preprocess(data):
    data = convert_lower_case(data)
    data = normalize(data)
    data = remove_punctuation(data)
    data = remove_apostrophe(data)
    data = convert_numbers(data)
    data = remove_stop_words(data)
    data = stemming(data)
    data = lemmatisation(data)
    data = remove_punctuation(data)
    data = convert_numbers(data)
    data = remove_single_characters(data)
    data = remove_dots(data)
    data = add_k_grams(data)
    return data


def preprocess_query(data):
    data = convert_lower_case(data)
    data = normalize(data)
    data = remove_punctuation(data)
    data = remove_apostrophe(data)
    data = convert_numbers(data)
    data = remove_stop_words(data)
    data = stemming(data)
    data = lemmatisation(data)
    data = remove_punctuation(data)
    data = convert_numbers(data)
    data = remove_dots(data)
    data = remove_single_characters(data)
    
    return data


def postprocess_query(data):
    data = add_k_grams(data)
    return data
