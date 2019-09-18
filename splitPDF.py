import os
from PyPDF2 import PdfFileReader as reader,PdfFileWriter as writer

# split.py
# new
#   |- 301
#   |- 501


def split(path,name):
    f=reader(path+'/'+name)
    page=f.getNumPages()
    part=500
    w=writer()
    if page>part:
        newPath=path+'/'+name.split('.')[0]
        os.mkdir(newPath)
        div=page//part
        for i in range(div):
            start=i*part
            end=(i+1)*part-1
            dirs=f'{newPath}/{i}_{name}'
            for p in range(start,end):
                pdf=f.getPage(i)
                w.addPage(pdf)
            w.write(open(dirs,'wb'))
    else:
        pass

def main():
    for fd in ['301','501']:
        ls=os.listdir(fd)
        for f in ls:
            split(fd,f)

if __name__=='__main__':
    main()
