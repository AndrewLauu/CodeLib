import os

dir = 'd:\\Program Files\\apktool\\c - 副本\\smali\\'
files = os.listdir(dir)
i = 0
j = 0
for file in files:

    path = os.path.join(dir, file)
    if os.path.isfile(path):
        i += 1
        with open(path, "r+") as f:
            text = f.read()
            if text.find('com/google/android/calculator') != -1:
                j += 1
                textRep = text.replace('com.google.android.calculator', 'com.android.calculator2')
                f.truncate()
                f.write(textRep)
            else:
                continue
    else:
        continue
print(str(i) + "\n" + str(j))
