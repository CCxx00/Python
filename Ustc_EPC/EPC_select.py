from EPC_checkcode import internet_Ai
import re
import time
import threading

class select_lesson(internet_Ai):
    def judge_login(self):
        if(re.findall("登录后可以查看详细信息",self.get_html().get_text())): #寻找html页面中是否有登陆后。。。
            print("未登录")
            return False
        else:
            print("已登录")
            return True

    def capture_key(self):
        for form in self.get_html().find_all('form',{'action':re.compile("m_practice.asp?")}): #寻找所有action中带有m_practice.asp?的form
            if(form.find_all('input',attrs={'type':'submit'})):
                self.list.append(form.get('action')) # 保存关键词
                # print(form.get('action'))
            else:
                print("无课可选")
                return False
        return True

    def select_les(self,**kwargs):
        for li in self.list: # 从list中获取地址，post发送数据到该地址
            self.url="http://epc.ustc.edu.cn/"+li
            t=threading.Thread(target=self.post_html(**kwargs))
            t.start()
            print("已选中"+" "+self.url)
        self.list.clear()

def main():
    datas={
    'submit_type':'book_submit'
    }
    iAi=select_lesson('http://epc.ustc.edu.cn/m_practice.asp?second_id=2001')
    while(True):
        if(iAi.judge_login()):
            if(iAi.capture_key()):
                 iAi.select_les(**datas)
                 break
        else:
            break
        time.sleep(20)



if __name__=="__main__":
    main()
