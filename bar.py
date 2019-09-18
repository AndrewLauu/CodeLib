import time

#
# import progressbar as p
# from progressbar import Bar

''''''
# import progressbar as p
#
# with p.ProgressBar(max_value=100,prefix="* ",suffix=" #") as bar:
#     for i in range(101):
#         time.sleep(0.02)
#         bar.update(i)

# * 100% (100 of 100) |##################| Elapsed Time: 0:00:02 Time:  0:00:02 #
''''''

# read: extended Shortcut mode second recommended

# from progressbar import Bar
# import progressbar as p
#
# w = [
#     Bar(left="*[", right=']', marker=">", fill="-"), " ",
#     p.FileTransferSpeed(), " #"
# ]
# pb = p.ProgressBar(widgets=w)
# for i in pb(range(51)):
#     time.sleep(0.1)
# sys.stdout.flush()

# *[>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>---]  10.0 B/s #

''''''
# read: console mode not recommended
# import progressbar as p
#
# for i in p.progressbar(range(10), redirect_stdout=True):
#     print(i)
#     time.sleep(0.1)

#  10% (1 of 10) |##                       | Elapsed Time: 0:00:00 ETA:   0:00:000
#  20% (2 of 10) |#####                    | Elapsed Time: 0:00:00 ETA:   0:00:001
#  30% (3 of 10) |#######                  | Elapsed Time: 0:00:00 ETA:   0:00:002
# 3
#  40% (4 of 10) |##########               | Elapsed Time: 0:00:00 ETA:   0:00:004
#  50% (5 of 10) |############             | Elapsed Time: 0:00:00 ETA:   0:00:005
#  60% (6 of 10) |###############          | Elapsed Time: 0:00:00 ETA:   0:00:006
#  70% (7 of 10) |#################        | Elapsed Time: 0:00:00 ETA:   0:00:007
#  90% (9 of 10) |######################   | Elapsed Time: 0:00:00 ETA:   0:00:008
# 9
# 100% (10 of 10) |########################| Elapsed Time: 0:00:01 Time:  0:00:01

''''''
# read: Unknown Time
# from progressbar import Bar
# import progressbar as p
#
# w = [Bar(left="*[", right=']', marker=">", fill="-"), " ", p.FileTransferSpeed(), " #"]
# bar = p.ProgressBar(max_value=p.UnknownLength, widgets=w)
# for i in range(51):
#     time.sleep(0.1)
#     bar.update(i)

# *[>---------------------------------------------------------------]  10.0 B/s #456

''''''
# read: Shortcut mode preferred

import progressbar as p
fileSize = 100000
w = [
    p.FileTransferSpeed(),
    p.Bar(left=" |", marker=">", fill="-", right="|"),
    p.DataSize(), f"/ {fileSize} KiB (", p.Percentage(), ')| ',
    p.ETA(),
]
for i in p.progressbar(range(1), widgets=w):  # , prefix="* ", suffix=" #"):
    time.sleep(0.05)
    for j in p.progressbar(range(50),widgets=w):
        time.sleep(0.01)

# 19.9 B/s |>>>>>>>>>>>>>>>>>>>>>>>>>| 51.0 B/ 100000 KiB (100%)| Time:  0:00:02
''''''

# from eprogress import MultiProgressManager,LineProgress
# import threading
#
#
# def test(pm):
#     for i in range(1, 31):
#         pm.update(threading.currentThread().getName(), i)
#         time.sleep(0.05)
#
#
# if __name__ == '__main__':
#     threads = []
#     pm = MultiProgressManager()
#     for i in range(3):
#         pm.put(f'Thread-{i+1}', LineProgress(total=30,title=str(i)))
#     for i in range(3):
#         name = f't{i}'
#         t = threading.Thread(target=test,args=(pm,))
#         t.start()
#         threads.append(t)
