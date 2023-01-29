from itertools import chain, combinations_with_replacement as cwr, groupby
from pprint import pprint

gifts = {
    5000: {'gift': 10, 'price': 1},
    4000: {'gift': 10, 'price': 3},
    2000: {'gift': 5, 'price': 1.5},
    7000: {'gift': 20, 'price': 8},
    10000: {'gift': 30, 'price': 13},
    3000: {'gift': 10, 'price': 5},
    # 2000: {'gift': 10, 'price': 7}
}

owningPoint = int(input('owningPoint: ') or 0) or 18933 + 1500

minPoint = min(gifts.keys())
productResult = chain(
    *(
        cwr(gifts.keys(), i)
        for i in range(owningPoint // minPoint + 1)
    )
)
minResult = owningPoint - minPoint

nowMaxGift = 0
nowMinPrice = 999_999_999

collect = []
for pr in productResult:
    iSumPoint = sum(pr)
    # overflow or not enough
    if iSumPoint > owningPoint or iSumPoint <= minResult:
        continue
    # print(pr, end='\r')

    sumGift = sum((gifts[i]['gift'] for i in pr))
    sumPrice = sum((gifts[i]['price'] for i in pr))
    # 取等于 减少数量；不取等于，保留多种方案，避免存货不足
    if sumGift < nowMaxGift and sumPrice > nowMinPrice:
        continue
    nowMaxGift, nowMinPrice = sumGift, sumPrice
    unitPrice = round(iSumPoint / (sumGift - sumPrice), 3)
    collect.append(('|'.join(map(str, pr)), sumGift, sumPrice, unitPrice, owningPoint - iSumPoint))

collect.sort(key=lambda x: x[3:])
pprint(collect)
print(len(collect))

# 同效率同剩余，取最短
newCollect = []
collectGroup = groupby(collect, key=lambda x: x[3:])
for i, j in collectGroup:
    newCollect.append(
        min(j, key=lambda x: len(x[0]))
    )
pprint(newCollect)
print(len(newCollect))

# 同剩余取效率最高
newNewCollect = []
newCollect.sort(key=lambda x: x[-1])
collectGroup = groupby(newCollect, key=lambda x: x[-1])
for i, j in collectGroup:
    newNewCollect.append(
        min(j, key=lambda x: x[3])
    )
pprint(newNewCollect)
print(len(newNewCollect))

with open("result.csv", 'w') as f:
    f.write('collection,sum gift,sum price,p/cny,rest point\n')
    for i in newNewCollect:
        f.write(','.join(map(str, i)) + '\n')
