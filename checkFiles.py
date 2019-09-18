import os

# 文件夹结构
# new
#  |- check.py
#  |- base.txt
#  |- pdf
#      |- *.pdf
#      |- *.pdf
#      |- *.pdf
#  |- folder


# base.txt
# 行号 项目 凭证号
# prefix work aid

ls=os.listdir('pdf')
ls=[i.split('.')[0] for i in ls]

with open('base.txt','r') as f:
    lines=f.readlines()
prefix=[]
work=[]
aid=[]
for l in lines:
    try:
        pre,wk,a=[i.strip() for i in l.split(',')]
    except ValueError:
        pre,wk,a=[i.strip() for i in l.split('\t')]
a
    prefix.append(pre)
    work.append(wk)
    aid.append(a)

PreDict=dict(zip(aid,prefix))
WorkDict=dict(zip(aid,work))

delta1=set(ls)-set(aid)#多拍
delta2=set(aid)-set(ls)#没拍
print('少拍:')
for i in delta2:
    print(i.replace('30107GL18',''),WorkDict[i])
print('多拍:')
for i in delta1:
    print(i.replace('30107GL18',''),WorkDict[i])

go_on=input('继续整理？')

if go_on=='y':
    for i in set(work):
        os.mkdir(f'{folder}/{i}')
    for f in ls:
        pre=preDict[f]
        path=f'folder/{work[f]}'
        os.rename(f'{pdf}/{f}.pdf',f'{path}/{f}.pdf')
