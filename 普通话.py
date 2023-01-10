import time

import requests
import yagmail

print("imported libs successfully")


# 获取成绩单页的html
def get_html(txtName, txtIDCard):
    url = 'http://sd.cltt.org/Web/Login/PSCP01001.aspx'
    data = {
        # 来自Form Data,下面赋值
        '__VIEWSTATE': '',
        'txtStuID': '',
        'txtName': txtName,
        'txtIDCard': txtIDCard,
        'btnLogin': '查  询',
        'txtCertificateNO': '',
        'txtCardNO': ''
    }
    response = requests.post(url, data=data)
    html = response.content.decode('utf-8')
    return html
    # print(html)


# 解析html取出个人信息
def get_result(html, result=None):
    if html.find(r"Andrew") != -1:
        # 姓名
        name_start = html.find(r'姓名：')  # 起点记录查询位置
        name_end = html.find(r'证件号：')
        name_html = html[name_start + 190:name_end - 186]

        # 身份证
        id_start = html.find(r'证件号：')  # 起点记录查询位置
        id_end = html.find(r'准考证号：')
        id_html = html[id_start + 192:id_end - 786]

        # 等级
        level_start = html.find(r'等级：')  # 起点记录查询位置
        level_end = html.find(r'证书编号：')
        level_html = html[level_start + 171:level_end - 169]

        # 分数
        score_start = html.find(r'最终分：')  # 起点记录查询位置
        score_end = html.find(r'等级：')
        score_html = html[score_start + 173:score_end - 280]

        # 证书编号
        bookid_start = html.find(r'证书编号：')  # 起点记录查询位置
        bookid_end = html.find(r'省份：')
        bookid_html = html[bookid_start + 174:bookid_end - 280]

        # 准考证号
        k_start = html.find(r'准考证号：')  # 起点记录查询位置
        k_end = html.find(r'出生日期：')
        k_html = html[k_start + 173:k_end - 171]

        # print(new_html)
        if len(name_html) < 10:
            result = f"姓名/id:{name_html}/{id_html} \n等级:{level_html}/{score_html}分 \n证书编号:{bookid_html} \n准考证号:{k_html}"
            print("----------------------------------------------------------------")
            print(result)

    else:
        print("无结果")
        result = ""
    return result


def send_mail(msg):
    # 发送邮件，初始参数
    mailer = '123456#139.com'  # 发送方邮箱
    password = "cmcc"  # 填入发送方邮箱的授权码
    msg_to = ''  # 收件人邮箱
    Subject = "普通话成绩监控"
    yag = yagmail.SMTP(mailer, password, host='smtp.10086.cn', port=25, smtp_ssl=False)
    yag.send(msg_to, Subject, msg)
    print("发送成功")


# 主函数
def main():
    now = time.localtime().tm_hour
    if now < 8:
        print('非工作时间，休眠中...')
        time.sleep(1 * 60 * 60)
        main()
    elif now > 18:
        print('非工作时间，休眠中...')
        time.sleep(1 * 60 * 60)
        main()
    else:
        print("工作时间，启动中...")
        # txtName = input("请输入姓名：")
        # txtIDCard = input("请输入身份证号：")
        names = "Andrew"
        ids = "123456789123456789"
        # for i in range(len(names)):
        txtName = names
        txtIDCard = ids
        print(f"name: {names}\nid: {ids[0:3]}***{ids[-4:-1]}")
        html = get_html(txtName, txtIDCard)
        result = get_result(html)
        if result == "":
            for i in range(1, 0, -1):
                print(f"{i} hours 后重试")
                time.sleep(3600)
            print("===========")
            print("正在重试")
            main()
        else:
            msg = result
            print("获取到结果，正在发送邮件")
            send_mail(msg)
        # print(html)


if __name__ == "__main__":
    main()
