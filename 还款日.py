# -*- coding:utf-8 -*-
import json

import xlrd


def readDays():
    wb = xlrd.open_workbook('还款日.xls')

    ifpDict = {}
    for ws in wb.sheets():
        name = ws.name
        ifpDict[name] = {}
        for row in range(ws.nrows):
            bill, pay = [int(i) for i in ws.row_values(row)]
            ifpList = []
            for today in range(1, 32):
                ifp = test(bill, pay, today)
                ifpList.append(ifp)
            avgIfp = sum(ifpList) / len(ifpList)
            maxIfp = max(ifpList)
            gt40 = len([n for n in ifpList if n >= 40])
            f40t35 = len([n for n in ifpList if n in range(35, 40)])
            f35t30 = len([n for n in ifpList if n in range(30, 35)])
            f30t25 = len([n for n in ifpList if n in range(25, 30)])
            ls25 = len([n for n in ifpList if n < 25])
            # minIfp = min(ifpList)
            print(name, bill, pay, avgIfp)
            ifpDict[name][bill] = {
                'pay': pay,
                'avg': avgIfp,
                'max': maxIfp,
                '40+': gt40,
                '35-40': f40t35,
                '30-35': f35t30,
                '25-30': f30t25,
                '25-': ls25
            }
    with open('还款日.json', 'w', encoding='utf8') as f:
        json.dump(ifpDict, f, indent=2, ensure_ascii=False)


def test(bill, pay, today):
    '''
    :param bill: bill day
    :param pay: pay off bill
    :param today: purchase day
    :return ifp: interest free period
    '''
    # 按31天计算
    daysInMonth = 31
    ifp = 0
    #
    if pay >= bill:
        payDelay = pay - bill
    else:
        payDelay = pay + daysInMonth - bill

    if today > bill:
        ifp = daysInMonth + bill - today + payDelay
    elif today <= bill:
        ifp = bill - today + payDelay
    return ifp
    # print(today, ifp)


if __name__ == '__main__':
    readDays()
