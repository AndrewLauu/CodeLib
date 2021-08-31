import sys
import sqlite3
import os

arg=sys.argv
if arg and len(arg)==3:
    tmp,path,script=arg
    if not os.path.isfile(path):
        raise IOError('SQL database path required.')
else:
    raise TypeError('SQL database path and script are both required')

conn=sqlite3.connect(path)
c=conn.cursor()
c.execute(script)
result=c.fetchall()
# print(result)
conn.close()

if result:
    for i in result:
        stri=[str(j) for j in i]
        format_result='\t'.join(stri)
        print(format_result)
else:
    print('No result')


