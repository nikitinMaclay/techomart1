import pymorphy2
from string import ascii_letters, digits


def word_separation(req):
    morph = pymorphy2.MorphAnalyzer()
    ind = 0
    for el in req:
        if el in ascii_letters or el in digits:
            ind = req.find(el)
            break
    words_eng = req[ind:]
    words_rus = req[:ind].split()
    try:
        words_rus = [morph.parse(el)[0].inflect({'sing', 'nomn'}).word
                     for el in words_rus]
    except AttributeError:
        words_rus = []
    if words_rus and not words_eng:
        return 1
    elif words_eng and not words_rus:
        return 2
    elif words_eng and words_rus:
        return 3


print(word_separation(input()))