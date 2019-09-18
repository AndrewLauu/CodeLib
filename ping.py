# $USR/bin/python
# -*- coding=utf8 -*-

import re
import subprocess as s
import time
import platform as plf
import sys

print('imported pkgs')


def ping(ip):
    os=plf.system()
    if os=='Linux':
        script=f'ping -q -c 10 -i 1 -W 5 {ip}'
        regRtt='rtt min/avg/max/mdev = (\d+.\d+)/(\d+.\d+)/(\d+.\d+)/(\d+.\d+) ms'#rtt min/avg/max/mdev = 5.872/182.145/538.362/195.752 ms

    elif os=='Windows':
        script='ping.exe {ip}'
        regMinT = u'最短 = \d+'  # Minimum = 37ms, Maximum = 38ms, Average = 37ms   最短 = 37ms，最长 = 77ms，平均 = 48ms
        regMaxT = u'最长 = \d+'
        regAvgT = u'平均 = \d+'
        regDit = u'\d+'
        regError = u'请求超时'
    p = s.Popen(script,
                stdin=s.PIPE,
                stdout=s.PIPE,
                stderr=s.PIPE,
                shell=True)
    result = p.stdout.read().decode('utf8')
    else:
        raise OSError(f'Platform {os} is not supported.')

   # print(result)
    time.sleep(2)
    '''
    if re.search(regError, result):
        flag = False
        minT = maxT = avgT = 99999
    else:
        flag = True
        minT = re.search(regMinT, result).group()
        maxT = re.search(regMaxT, result).group()
        avgT = re.search(regAvgT, result).group()
        minT = int(re.search(regDit, minT).group())
        maxT = int(re.search(regDit, maxT).group())
        avgT = int(re.search(regDit, avgT).group())
        '''

    rtt=re.search(regRtt,result)
    if rtt:
#        rtt=[int(i) for i in rtt_ori]
        minT=float(rtt[1])
        avgT=float(rtt[2])
        maxT=float(rtt[3])
        mdevT=float(rtt[4])
        flag=True
    else:
        flag=False
        minT=avgT=maxT=mdevT=9999

    return minT, maxT, avgT, mdevT,flag


def main():
    ip_dict = {
        'ali_1': '223.5.5.5',
        'ali_2': '223.6.6.6',
        'DNS 派_1': '101.226.4.6',
        'DNS 派_2': '218.30.118.6',
        'DNS 派_3': '123.125.81.6',
        'DNS 派_4': '140.207.198.6',
        '百度': '180.76.76.76',
        'DNSPod_1': '119.29.29.29',
        'DNSPod_2': '119.28.28.28',
        'DNSPod_3': '182.254.118.118',
        'DNSPod_4': '182.254.116.116',
        '114_1': '114.114.114.114',
        '114_2': '114.114.115.115'
    }
    print('Loaded IP addresses')

    logName = f'ping.{time.strftime("%Y-%m-%d", time.localtime(time.time()))}.md'
    with open(logName, 'w') as log:
        log.write('name|ip|Min|Max|Avg|Mdev\n---|---|---|---|---|---\n')


    for name, ip in ip_dict.items():
        minList =[]
        maxList = []
        avgList = []
        mdevList=[]
        # ping 5 times
        for count in range(5):
            sys.stdout.write(f'\rPing {name} for {count + 1}...\r')
            sys.stdout.flush()
            minT, maxT, avgT, mdevT,flag = ping(ip)
            
            if flag:
                minList.append(minT)
                maxList.append(maxT)
                avgList.append(avgT)
                mdevList.append(mdevT)
                time.sleep(2)
            else:
                print("Failed")
                continue
        try:
            minMin = min(minList)
            maxMax = max(maxList)
            avgAvg = round(sum(avgList) / len(avgList), 4)
            avgMdev = round(sum(mdevList) / len(mdevList), 4)
        except(ZeroDivisionError,ValueError):
            continue

        print(f"ping {name}: 最短 {minMin} ms, 最长{maxMax} ms, 平均{avgAvg} ms, 标准差 {avgMdev} ms")

        with open(logName, 'a') as log:
            # log.write(ip + "|" + name + '\n')
            # for vallist in [minList, maxList, avgList]:
            #     for val in vallist:
            #         log.write(str(val) + "|")
            #     log.write("\n")
            log.write(f"{name}|{ip}|{minMin}|{maxMax}|{avgAvg}|{avgMdev}\n")
        time.sleep(3)


if __name__ == "__main__":
    main()
