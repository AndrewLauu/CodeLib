from itertools import chain, combinations_with_replacement as cwr, groupby
from prettytable import PrettyTable

def printTable(header,rows):
    table = PrettyTable(header)
    table.add_rows(rows)
    print(table)



# exchangeTable = {'spendPoint':
#              {'gift': 'giftValue', 'price': 'extra spendCash'}
#          }
exchangeTable = {
    734: {'gift': 1, 'price': 0},
    2200: {'gift': 3, 'price': 0},
    3667: {'gift': 5, 'price': 0},
    7334: {'gift': 10, 'price': 0},
}

owningPoint: int = int(input('owningPoint: ') or 0) or 4599

minPointSpend: int = min(exchangeTable.keys())
possibleExchangeWay = chain(
    *(
        cwr(exchangeTable.keys(), i)
        for i in range(owningPoint // minPointSpend + 1)
    )
)

# owningPoint - iSumPoint < minPointSpend
# 确保积分都花完
minSumPointSpend: int = owningPoint - minPointSpend

nowMaxGift = 0
nowMinPrice: int = 999_999_999_999_999

headers=['way','sumGift', 'sumPrice', 'unitPrice', 'remainingPoint']
workableWay = []
for way in possibleExchangeWay:
    nowSpendPoint = sum(way)
    # overflow or not enough
    if nowSpendPoint > owningPoint or nowSpendPoint <= minSumPointSpend:
        continue
    # print(pr, end='\r')

    sumGift = sum((exchangeTable[p]['gift'] for p in way))
    sumPrice = sum((exchangeTable[p]['price'] for p in way))
    # 取等于 减少数量；不取等于，保留多种方案，避免礼品存货不足
    if sumGift < nowMaxGift and sumPrice > nowMinPrice:
        continue
    nowMaxGift, nowMinPrice = sumGift, sumPrice
    unitPrice = round(nowSpendPoint / (sumGift - sumPrice), 3)
    workableWay.append(('|'.join(map(str, way)), sumGift, sumPrice, unitPrice, owningPoint - nowSpendPoint))

workableWay.sort(key=lambda x: x[3:])
printTable(headers, workableWay)
print(len(workableWay))

# 同性价比同剩余，取最短
newCollect = []
collectGroup = groupby(workableWay, key=lambda x: x[3:])
for _, j in collectGroup:
    newCollect.append(
        min(j, key=lambda x: len(x[0].split('|')))
    )
print('='*10)
print('同性价比同剩余，取最短')
printTable(headers, newCollect)
print(len(newCollect))

# 同剩余取性价比最高
newNewCollect = []
newCollect.sort(key=lambda x: x[-1])
collectGroup = groupby(newCollect, key=lambda x: x[-1])
for i, j in collectGroup:
    newNewCollect.append(
        min(j, key=lambda x: x[3])
    )
print('=' * 10)
print('同剩余取性价比最高')
printTable(headers, newNewCollect)
print(len(newNewCollect))

with open("result.csv", 'w') as f:
    f.write('collection,sum gift,sum price,p/cny,rest point\n')
    for i in newNewCollect:
        f.write(','.join(map(str, i)) + '\n')
