# -*- coding:utf8 -*-

from PyPDF2 import PdfFileReader as reader, PdfFileWriter as writer
from tkinter import Tk, Button, Checkbutton, BooleanVar, filedialog, Label,StringVar
from tkinter.font import Font


def fileRead():
    # global filenames
    filenames = filedialog.askopenfilenames(filetypes=[('pdf', '*.pdf'), ('All Files', '*')])
    strPath=','.join(filenames).lower()
    path.set(strPath)
    label.config(text=f'{len(filenames)} file(s) selected.')


def rotate(filenames, angle, cover):
    for inFp in filenames.get().split(','):
        inPdf = reader(inFp)
        n = inPdf.getNumPages()
        outPdf = writer()
        outFp = inFp if cover.get() else inFp.replace('.pdf','_rotate.pdf')

        for i in range(n):
            p = inPdf.getPage(i).rotateClockwise(angle)
            outPdf.addPage(p)
            outPdf.write(open(outFp, 'wb'))


root = Tk()
root.title('PDF rotate')
root.geometry('500x250')
root.resizable(width=True, height=True)
font=Font(size=20)

angle = 90

path=StringVar()
select = Button(root, text="select", command=fileRead,font=font)
select.pack()

label = Label(text='null',font=font)
label.pack()


cover = BooleanVar()
chk = Checkbutton(root, text="cover?", variable=cover, onvalue=True, offvalue=False,font=font)
chk.pack()

write = Button(root, text="write", command=lambda: rotate(path, angle, cover),font=font)
write.pack()
root.mainloop()
