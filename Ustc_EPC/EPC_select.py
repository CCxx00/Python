from EPC_checkcode import internet_Ai
import re
import time
import threading

class select_lesson(internet_Ai):
    def post_html(self,post_url,post_data): # 改写父类post_html()
        print("开始选课:"+post_url)
        super().post_html(post_url,post_data=post_data) # 调用父类post_html()
        print("选课完成:"+post_url)

    def judge_login(self):
        if(re.findall("登录后可以查看详细信息",self.get_html(self.url).get_text())): #寻找html页面中是否有登陆后。。。
            print("未登录")
            return False
        else:
            print("已登录")
            return True

    def capture_key(self):
        for form in self.get_html(self.url).find_all('form',{'action':re.compile("m_practice.asp?")}): #寻找所有action中带有m_practice.asp?的form
            if(form.find_all('input',attrs={'type':'submit'})):
                self.list.append(form.get('action')) # 保存关键词
                # print(form.get('action'))
            else:
                print("无课可选")
                return False
        return True

    def creat_thread(self,data):
        for li in self.list: # 从list中获取地址，创建线程
            url="http://epc.ustc.edu.cn/"+li
            t=threading.Thread(target=self.post_html,args=(url,data))
            self.Theard.append(t)
        self.list.clear()

    def select_les(self):
        for t in self.Theard: # 开启所有创建的线程
            t.start()

def main():
    datas={
    'submit_type':'book_submit'
    }
    iAi=select_lesson('http://epc.ustc.edu.cn/m_practice.asp?second_id=2001')
    while(True):
        if(iAi.judge_login()):
            if(iAi.capture_key()):
                 iAi.creat_thread(datas)
                 iAi.select_les()
                 break
        else:
            break
        time.sleep(20)

if __name__=="__main__":
    main()
