import re
import subprocess as sub
# os.system(cmd) execute only without return
# os.popen depreciated

p = sub.Popen(
    "pip list",
    stdout=sub.PIPE,
    # stderr=sub.PIPE,
    shell=True
)
pipLines = p.stdout.readlines()
# pipLinesCount = len(pipLines)
regVersion = "\s*(\d+\.)+(\d+\s+)"
pipList = []
#for i in range(2, pipLinesCount - 1):
for i in pipLines[1:]:
    pip = pipLines[i].decode("utf-8")
    pipName = re.sub(regVersion, "", pip)
    pipList.append(pipName)
# p.stdout.close()
# print(pipList)
print(pipList)
# pipList

for pip in pipList:
    require={pip:}
