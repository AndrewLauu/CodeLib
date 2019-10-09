import MergeExcel as mxl
import openpyxl as xl
import time

today=time.strftime('%m.%d',time.localtime())
# 报销
mxl.merge(srcDir='报销',nHead=0,maxCol=3,dstDir=f'{today}-七部报销汇总.xlsx')
ws=xl.load_workbook(f'{today}-七部报销汇总.xlsx').active
bxSum=sum(ws['a':'a'])
print(bxSum)
