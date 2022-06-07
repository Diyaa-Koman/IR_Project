from numpy import unique
import gensim
from gensim.models import Word2Vec
import engine.buildEngine as be

allowed_edits = 2

# for test
# vocabulary = ["hello", "united", "states", "war", "tonight"]


def optimize_query(processed_query: str, vocabulary):
    optimized_query = []
    split_query = processed_query.split()
    for token in split_query:
        if token in vocabulary:
            optimized_query.append(token)
        else:
            print("Query spell checker: " + token + " not in vocabulary")
            min_replacement = ''
            for word in vocabulary:
                min_change = allowed_edits + 1
                edt_dis = edit_distance(token, word)
                if edt_dis <= allowed_edits:
                    min_change = edt_dis
                    if edt_dis < min_change:
                        min_replacement = word
                    else:
                        min_replacement = better_replacement(token, min_replacement, word)
            if min_replacement != '':
                print("Replaced with " + min_replacement)
                optimized_query.append(min_replacement)
    return ' '.join(optimized_query)


def better_replacement(original, replacement1, replacement2):
    org = (list(original))
    rep1 = (list(replacement1))
    rep2 = (list(replacement2))
    score1 = 0
    score2 = 0
    for i in rep1:
        if i in org:
            score1 = score1 + 1
        else:
            score1 = score1 - 1
    for i in rep2:
        if i in org:
            score2 = score2 + 1
        else:
            score2 = score2 - 1
    for i in org:
        if i in rep1:
            score1 = score1 + 1
        if i in rep2:
            score2 = score2 + 1
    if score1 > score2:
        return replacement1
    else:
        return replacement2


def edit_distance(string1, string2):
    smaller = ''
    if len(string1) > len(string2):
        difference = len(string1) - len(string2)
        smaller = string2
        # string1[:difference]

    elif len(string2) > len(string1):
        difference = len(string2) - len(string1)
        smaller = string1
        # string2[:difference]

    else:
        smaller = string1
        difference = 0

    if difference > allowed_edits:
        return difference

    for i in range(len(smaller)):
        if string1[i] != string2[i]:
            difference += 1
            if difference > allowed_edits:
                break

    return difference

    
def use_word_to_vec(processed_query: str, vocabulary):
    optimized_query = []
    split_query = processed_query.split()
    for token in split_query:
        if token in vocabulary:
            optimized_query.append(token)
        else:
            print("Query spell checker: " + token + " not in vocabulary")
            # try :
            best_word = be.get_model().wv.most_similar(token)
            print("Replaced with " + best_word)
            optimized_query.append(best_word)
            # except :
            #     optimized_query.append(token)
                
    return ' '.join(optimized_query)


def get_tags_by_image(image):
    import requests

    api_key = 'acc_cea2db248a627b9'
    api_secret = '923d23592e7815901542797d0523d791'
    # image_path = '/path/to/your/image.jpg'

    response = requests.post(
        'https://api.imagga.com/v2/uploads',
        auth=(api_key, api_secret),
        files={'image': image})
    print(response.json())

    upload_id = response.json()['result']['upload_id']
    # print(upload_id)
    response = requests.get(
        'https://api.imagga.com/v2/tags?image_upload_id=%s' % (upload_id),
        auth=(api_key, api_secret))

    # print(response.json()['result']['tags'])
    return response.json()['result']['tags']