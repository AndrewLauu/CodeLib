from itertools import product
import re
from collections import defaultdict
from datetime import datetime as dt

def getLast(id='37028119971101001', lastOnly=False):
    weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2, 0]
    ck = [1, 0, 'X', 9, 8, 7, 6, 5, 4, 3, 2]

    wsum = sum([int(i) * j for i, j in zip(id, weight)])
    observedValue = wsum % 11
    last = 12 - observedValue
    if last == 10:
        last = 'X'
    elif last > 10:
        last -= 11
    last = str(last)
    # last=ck[observedValue]
    if lastOnly:
        return last
    else:
        return id + last


def isValid(id,sex=None):
    last = getLast(id[:-1], lastOnly=True)
    validLast = last.lower() == id[-1].lower()

    y = int(id[6:10])
    m = int(id[10:12])
    d = int(id[12:14])
    try:
        validBirth=1900<=dt(y,m,d).year<=2021
    except:
        validBirth=False

    if sex in ['m','f']:
        sexValid=sex=={1:'m',0:'f'}[id[-2] % 2]
    elif sex is None:
        validSex=True
    else:
        validSex=False

    return validLast*validBirth*validSex


def getInner(id='370281##970702051X',sex=None):
    # defaultValue = [str(i) for i in range(10)]
    d = {6: (1, 2), 7: (8, 9, 0, 1, 2), 10: (0, 1), 12: (0, 1, 2, 3)}
    guessValue = defaultdict(lambda: range(10))
    guessValue.update(d)
    guessYear = range(1900, 2023)
    guessMonth = range(1, 13)
    guessDay = range(1, 32)

    guessResult = []
    span = [s.span()[0] for s in re.finditer('#', id)]
    nBlank = len(span)
    productGroup = [guessValue[i] for i in span]

    idL = list(id)
    # cmb = product(defaultValue, repeat=nBlank)
    cmb = product(*productGroup)
    for c in cmb:

        for cpos, idPos in enumerate(span):
            idL[idPos] = str(c[cpos])
        newID = ''.join(idL)
        if isValid(newID,sex):
            guessResult.append(newID)
    return guessResult


if __name__ == '__main__':
    getInner(id='370281##970702051X')
