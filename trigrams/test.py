from random import randint,shuffle,choice,sample
import json


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
        print('-'*6)
        print(f'  ## Performing {ch+1} change')
        bars=change(bars)
        print('-'*6)
    return int(len(bars)/4)
    
def getDes(yao):
    trigramsNo=str(eval('0b'+''.join(yao)))
    name=trigramsDict[trigramsNo]['name']
    fig=trigramsDict[trigramsNo]['fig']
    fn=trigramsDict[trigramsNo]['fullname']
    dsp=trigramsDict[trigramsNo]['description']
    print(yao)
    print(name,fig,fn,dsp)


if __name__=='__main__':
    result=[]
    trigramsDict=json.load(open('trigrams.json','r'))
    for y in range(6):
        print('='*6)
        print(f'# Getting {y+1} yao')
        yao=getYao()
        result.append(yao)
        print(f'# Got {y+1} yao: {yao}')
        print('='*6)
    #print(result)

    #yaoDict={9:'⚊°',8:'⚋',7:'⚊',6:'⚋°'}
    #yaofig=[yaoDict[i] for i in result[::-1]]
    #print('\n'.join(yaofig))
    moving=[]
    reChange=[]
    for i,y in enumerate(result):
        if y==6 or y==9:
            moving.append(i+1)
            # mature yao change into young yao
            reChange.append(int(y/2))
        else:
            reChange.append(y)
    
    yao=[str(i%2) for i in result]
    print('original trigrams')
    getDes(yao)
    if reChange:
        print(moving,'yao moving')
        print('========')
        print('change trigrams')
        chYao=[str(i%2) for i in reChange]
        getDes(chYao)

