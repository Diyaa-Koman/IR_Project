import re
from textblob import TextBlob


def reduce_lengthening(query):
    pattern = re.compile(r'(.)\1{2,}')
    return pattern.sub(r'\1\1', query)


def correct_spelling(query):
    return TextBlob(query).correct()


def print_suggestion(query):
    suggested_query = reduce_lengthening(query.lower())
    suggested_query = correct_spelling(suggested_query)
    if suggested_query.lower() != query.lower():
        return (f'Suggested Query: {suggested_query}')
