import shutil
import os
import time
import hashlib

def main():
    print("=======================")
    
    opt_code = input('File Operation Type\n[record_code[0,1] + mode_option[1,2]\nrecord_code:record=1\tNO record=0\nmode_type:Visibilize=1;\tUnvisibilize=2:\n')
    rec_code = opt_code[0]
    mode_code = opt_code[-1]

    print("=======================")
    
    vis = "E:\\Advanced_Control"
    unvis = "E:\\Advanced_Control.{ED7BA470-8E54-465E-825C-99712043E01C}"
    try:
        #可见化
        if mode_code == "1":
            psw_chk()
            os.rename(unvis,vis)
##            shutil.move(unvis, vis)
            print("mode_1 Finished")
            rec(mode_code, rec_code)
            '''记录时间'''
            print("=======================")
            input()

        #不可见化
        elif mode_code == "2":
            print("Progressing...")
            rec(mode_code, rec_code)
            '''记录时间'''
            os.rename(vis,unvis)
            ##shutil.move(vis, unvis)
            print("mode_2 Finished")
            print("=======================")
            input()

##        elif mode_code == "3"
##            print("激活隐藏模式")
##            print("=======================")
##            input("Input new password: ")
        else:
            print("1 or 2")
            main()
            print("=======================")
    except IOError:
        print("No that address,restart")
        main()

def psw_chk():
    psw = input("Input password: ").encode("utf-8")
    h_psw = hashlib.md5(psw).hexdigest()
    orig_h_psw = '7694f4a66316e53c8cdd9d9954bd611d'
##    print(h_psw)
    #密码验证
    if h_psw == orig_h_psw:
        return
    else:
        print("Password validation failed")
        main()

def rec(mode_code, rec_code):
    #记录模式
    if rec_code == "1":
        tmode = '%Y-%m-%d %H:%M:%S'
        if mode_code == "1":
            text = "开启：" + time.strftime(tmode,time.localtime())
        elif mode_code == "2":
            text = "\n关闭：" + time.strftime(tmode,time.localtime())+"\n"
        try:
            with open("E:\\Advanced_Control\\1.txt","a+") as f:
                text = f.read() + text
                f.write(text)
            print("写文件完成")
        except IOError:
            print("写文件出错")
        finally:
            return
    #不记录
    elif rec_code == "0":
        print("未做记录")
        return
    
if __name__ == '__main__':
    main()
