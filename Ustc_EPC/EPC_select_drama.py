from EPC_select import select_lesson
import re
import time
import threading

class select_drama(select_lesson):
    def creat_thread(self,data):
        for i in range(2): # 从list中获取地址，创建线程
            url="http://epc.ustc.edu.cn/"+self.list[i]
            t=threading.Thread(target=self.post_html,args=(url,data))
            self.Theard.append(t)
        self.list.clear()

def check_login(iAi):
    while True:
        time.sleep(20)
        if not iAi.judge_login():
            break

def set_pause_time(h,m,s):
    pause_time=h*60*60+m*60+s-time.localtime()[3]*60*60-time.localtime()[4]*60-time.localtime()[5]
    if pause_time<0:
        pause_time=0
    return pause_time

def main():
    datas={
    'submit_type':'book_submit'
    }
    iAi=select_drama('http://epc.ustc.edu.cn/m_practice.asp?second_id=2004')
    iAi.judge_login()

    t=threading.Thread(target=check_login,args=(iAi,))
    t.start()

    time.sleep(set_pause_time(16,30,0))

    for i in range(20):
        iAi.capture_key()
        iAi.creat_thread(datas)
        iAi.select_les()
        print("")

    t.join(1)
    time.sleep(200)
    input("ENTER") # 按回车后退出

if __name__=="__main__":
    main()
