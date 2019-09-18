from itertools import product as pt
def bus(price,sumv):
    s=0
    dic={-1:-1}
    x,y,xy,yy=price
    xq =range(int(sumv/x)+1)
    yq =range(int(sumv/y)+1)
    xyq =range(int(sumv/xy)+1)
    yyq =range(int(sumv/yy)+1)
    ways= pt(xq,yq,xyq,yyq)
    for q in ways:
        si=sum([x*y for x,y in zip(price,q)])
        if si>sumv:
            continue
        elif si==sumv:
            print('xq,yq,xyq,yyq')
            print(q)
            print(si)
        elif si>s:
            s=si
        else:
            continue
        if s in dic.keys():
            li=[dic[s]]
            dic[s]=li.append(q)
        else:
            dic[s]=q
    print('xq,yq,xyq,yyq')
    print(dic[s])
    print(s)

def main():
    city=input('city: ')
    remain=float(input('remain: '))
    if city=='qd':
        price=(0.8,1.6,1.8,2.4)
    elif city=='jn':
        price=(0.8,1.6,2,2.8)
    bus(price,remain)

if __name__=='__main__':
    main()
