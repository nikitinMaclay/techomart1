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
    words_rus = [morph.parse(el)[0].inflect({'sing', 'nomn'}).word
                 for el in words_rus if "NOUN" in morph.parse(el)[0].tag]
    words_rus = " ".join(words_rus)
    if words_rus and not words_eng:
        return f"{words_rus}"
    elif not words_rus and words_eng:
        return f"{words_eng}"
    elif words_rus and words_eng:
        return f"{words_rus} {words_eng}"
    return ""