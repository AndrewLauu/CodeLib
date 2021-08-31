import random

def mtkl(cnt): 
    inCir=0
    for j in range(cnt):
        x=random.random()
        y=random.random()
        print(f'{j}/{cnt}',end='\r')
        if (x**2+y**2)**0.5<=1:
            inCir+=1
    pi=4*inCir/cnt
    print('mtkl',pi,end='\n\n')

def form(cnt):
    pi=0
    for k in range(cnt):
        re=(4/(8*k+1)+2/(8*k+4)+1/(8*k+5)+1/(8*k+6))
        re=re/pow(16,k)
        pi+=re
        print(f'{k}/{cnt}',end='\r')
    print('form',pi,end='\n\n')

for i in range(3,6):
    cnt=10**i
    print(cnt,end='\n')
    mtkl(cnt)
    form(cnt)


