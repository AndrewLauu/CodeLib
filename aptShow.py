import re
import json
import sys
import subprocess as sub

def getApt():
    p=sub.Popen('apt list --installed',
            stdout=sub.PIPE,
            stderr=sub.PIPE,
            shell=True)
    aptListB=p.stdout.readlines()
    aptList=[i.decode('utf8') for i in aptListB]
    aptList.pop(0)
    regApt=re.compile('^.+?(?=/)',re.M)
    name=[ regApt.search(i)[0] for i in aptList ]
    return name

def getSize(app):
#print(aptList[0])
    regSize=re.compile('(?<=Installed-Size: )\d+.\d* (?:MB|kB)')
    p=sub.Popen(f'apt show {app}',
            stdout=sub.PIPE,
            stderr=sub.PIPE,
            shell=True)
    info=p.stdout.read().decode('utf8')
    size=regSize.search(info)[0]
    return size

def main():
    nameList=getApt()
    size=[]
    count=1
    total=len(nameList)
    for i in nameList:
        sys.stdout.write(f'\rProcessing {count}/{total} : {i}          ')
        sys.stdout.flush()
        size.append(getSize(i))
        count+=1
    nameDict=dict(zip(nameList,size))
    with open('aptInfo','w') as f:
        json.dump(nameDict,f,indent=2,ensure_ascii=False)


if __name__=='__main__':
    main()
