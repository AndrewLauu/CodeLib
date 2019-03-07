import re
import subprocess as s
import time

print('imported pkgs')


def ping(ip):
    p = s.Popen(["ping.exe", ip],
                stdin=s.PIPE,
                stdout=s.PIPE,
                stderr=s.PIPE,
                shell=True)
    result = p.stdout.read().decode("gbk")
    # print(result)
    regMinT = u'最短 = \d+'  # Minimum = 37ms, Maximum = 38ms, Average = 37ms   最短 = 37ms，最长 = 77ms，平均 = 48ms
    regMaxT = u'最长 = \d+'
    regAvgT = u'平均 = \d+'
    regDit = u'\d+'
    regError = u'请求超时'
    # print(result)
    time.sleep(2)
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
    return minT, maxT, avgT, flag


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

    minList = maxList = avgList = []
    logName = 'ping.' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.md'
    with open(logName, 'w') as log:
        log.write('name|ip|Min|Max|Avg\n---|---|---|---|---\n')


    for name, ip in ip_dict.items():
        # ping 5 times
        for count in range(5):
            print(f'Pinging {name} for {count + 1}...')
            minT, maxT, avgT, flag = ping(ip)
            if not flag:
                print("Failed")
                continue
            else:
                minList.append(minT)
                maxList.append(maxT)
                avgList.append(avgT)
                time.sleep(2)
        try:
            avgMin = round(sum(minList) / len(minList), 4)
            avgMax = round(sum(maxList) / len(maxList), 4)
            avgAvg = round(sum(avgList) / len(avgList), 4)
        except ZeroDivisionError:
            continue

        print(f"ping {name}: 最短 {avgMin}ms, 最长{avgMax}ms, 平均{avgAvg}ms")

        with open(logName, 'a') as log:
            # log.write(ip + "|" + name + '\n')
            # for vallist in [minList, maxList, avgList]:
            #     for val in vallist:
            #         log.write(str(val) + "|")
            #     log.write("\n")
            log.write(f"{name}|{ip}|{avgMin}|{avgMax}|{avgAvg}\n")
        time.sleep(5)


if __name__ == "__main__":
    main()
