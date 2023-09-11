from random import randint,shuffle,choice,sample
import json
import os


def change(bars):
    nHeaven=randint(1,len(bars)-1)
    heaven=sample(bars,nHeaven)
    earth=list(set(bars)-set(heaven))
    shuffle(earth)
    print(f'    ### Got heaven={nHeaven}:{heaven}')
    print(f'    ### Got earth={len(earth)}:{earth}')
    human=earth.pop(randint(0,len(earth)-1))
    print(f'    ### Got human: {human}')
    
    L54,L23=[],[]
    remain=[]
    L54.append(human)
    print('    ### Removing from earth')
    while len(earth)>4:
        rm=sample(earth,4)
        remain+=rm
        earth=list(set(earth)-set(rm))
        shuffle(earth)
    L54+=earth
    
    while len(heaven)>4:
        rm=sample(heaven,4)
        print(f'    ### Removing from heaven {rm}')
        remain+=rm
        heaven=list(set(heaven)-set(rm))
        shuffle(heaven)
    L23+=heaven
    shuffle(remain)
    print(f'    ### Got remaining={len(remain)}: {remain}')
    return remain


def getYao():
    bars=list(range(1,51))
    shuffle(bars)
    taiji=bars.pop(randint(0,49))
    print(f'  ## Got Taiji: {taiji}')
    
    for ch in range(3):
        print(f'第{ch+1}变'.center(WIDTH,'-'))
        bars=change(bars)
    return int(len(bars)/4)
    
def getDes(trigram,yao=None):
    # key must be string
    trigramsNo=str(int(''.join([str(i) for i in trigram]),2))
    if yao:
        print(trigramsDict[trigramsNo]['yaos'][yao-1])
        return
    name=trigramsDict[trigramsNo]['name']
    odr=trigramsDict[trigramsNo]['order']
    fig=trigramsDict[trigramsNo]['fig']
    fn=trigramsDict[trigramsNo]['fullname']
    dsp=trigramsDict[trigramsNo]['description']

    print(f'第{odr}卦，{fig} {name}-{fn}')
    print(dsp)


def getExplain(result):

    trigram=[i%2 for i in result]
    print('得卦'.center(WIDTH,'='))
    getDes(trigram)
   
    # get change
    moving=[]
    chYao=[]

    for i,y in enumerate(result):
        if y==6:
            moving.append(i+1)
            chYao.append(1)
        elif y==9:
            moving.append(i+1)
            chYao.append(0)
        else:
            chYao.append(y%2)

    if not moving:
        return
    print(f'{moving}爻变，得变卦'.center(WIDTH,'='))
    getDes(chYao)

    print('爻辞，'.center(WIDTH,'='))
    match len(moving):
        case 0|3|6:
            pass
        case 1:
            getDes(trigram,moving[0])
        case 2:
            getDes(trigram,max(moving))
            getDes(trigram,min(moving))
        case 4:
            getDes(trigram,min(set(range(1,7))-set(moving)))
        case 5:
            getDes(chYao,min(set(range(1,7))-set(moving)))
            getDes(chYao,max(set(range(1,7))-set(moving)))

if __name__=='__main__':
    WIDTH=os.get_terminal_size().columns-4
    result=[]
    trigramsDict=json.load(open('trigrams.json','r'))
    for y in range(6):
        print(f'取第{y+1}爻'.center(WIDTH,'='))
        yao=getYao()
        result.append(yao)

    #yaoDict={9:'⚊°',8:'⚋',7:'⚊',6:'⚋°'}
    #yaofig=[yaoDict[i] for i in result[::-1]]
    #print('\n'.join(yaofig))
    
    print(result)
    getExplain(result)


