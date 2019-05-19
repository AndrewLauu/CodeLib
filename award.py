#读档
with open('award.txt','r') as f:
    txt=f.read().strip().strip('\ufeff\n\u3000\u3000')
txtlist=txt.split('\n\n\u3000\u3000')
names=txtlist[0::2]
profile=txtlist[1::2]
# 格式化
names=[name.replace(' ','') for name in names]
pro_list=[p.split('。', num=1) for p in profile]
pdict=dict(zip(name,pro_list))
info_tab1=['name','gender','party','birth','death','home','title']
info_tab2=['name','gender','party','birth','home','title']

for k, v in pdict:
    infodict={}
    info=v[0].split('，')
    # todo info整合字典
    # 是否组织及去世
    pname=info[0]
    pdeath=info[5][-2:-1]=='去世'
    if pname == k and pdeath:
        title=list('，'.join(info[7:]))
        info=info[:6]+title
        infodict=dict(zip(info_tab1,info))
    elif pname == k and not pdeath:
        title=list('，'.join(info[6:]))                  info=info[:5]+title
        infodict=dict(zip(info_tab2,info))
    elif not pname:
        info=[k]+['group']*5+info
        infodict=dict(zip(info_tab2,info))
    infodict['intro']=info[1]
    pdict[k]=infodict
print(pdict[0])
