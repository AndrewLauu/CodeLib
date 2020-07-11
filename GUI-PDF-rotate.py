# -*- coding:utf8 -*-

from PyPDF2 import PdfFileReader as reader, PdfFileWriter as writer
from tkinter import Tk, Button, Label, Checkbutton, Radiobutton, filedialog
from tkinter import StringVar, W
from tkinter.font import Font
from tkinter.messagebox import showinfo


def fileRead():
    filenames = filedialog.askopenfilenames(filetypes=[('pdf', '*.pdf')])
    strPath = ','.join(filenames).lower()
    path.set(strPath)
    label1.config(text=f'2. 选中 {len(filenames)} 个文件')


def rotate(filenames, angle, overwrite):
    for inFp in filenames.get().split(','):
        inPdf = reader(inFp)
        n = inPdf.getNumPages()
        outPdf = writer()
        outFp = inFp if overwrite.get() else inFp.replace('.pdf', '_rotate.pdf')

        for i in range(n):
            p = inPdf.getPage(i).rotateClockwise(int(angle.get()))
            outPdf.addPage(p)
            outPdf.write(open(outFp, 'wb'))
    showinfo(message="完成，保存在源文件所在文件夹")


root = Tk()
root.title('PDF rotate')
root.geometry('400x400')
root.resizable(width=True, height=True)
font = Font(size=14)

path = StringVar()
select = Button(root, text="1. 选择PDF文件", command=fileRead, font=font)
select.grid(sticky=W, pady=30, padx=40, columnspan=3)

label1 = Label(text='2. 检查文件数', font=font)
label1.grid(sticky=W, pady=30, padx=40, columnspan=3)

label2 = Label(text='3. 旋转角度（顺时针）', font=font)
label2.grid(sticky=W, padx=40, columnspan=3)

angle = StringVar()
angle.set('90')
angle90 = Radiobutton(root, text='90°', variable=angle, value='90', font=font)
angle180 = Radiobutton(root, text='180°', variable=angle, value='180', font=font)
angle270 = Radiobutton(root, text='270°', variable=angle, value='270', font=font)
angle90.grid(sticky=W, padx=40, row=4, column=0)
angle180.grid(sticky=W, row=4, column=1)
angle270.grid(sticky=W, row=4, column=2)

overwrite = StringVar()
chk = Checkbutton(root, text="4. 覆盖源文件？", variable=overwrite, onvalue='1', offvalue='',
                  font=font)
chk.grid(sticky=W, pady=30, padx=40, columnspan=3)

write = Button(root, text="5. 旋转并输出", font=font, command=lambda: rotate(path, angle, overwrite))
write.grid(sticky=W, padx=40, columnspan=3)

root.mainloop()
