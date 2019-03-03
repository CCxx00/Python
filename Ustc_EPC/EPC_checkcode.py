from bs4 import BeautifulSoup
import requests
import re
import json
import os

class internet_Ai(object):
    def __init__(self,url):
        self.url=url
        self.list=[]
        self.Session=requests.session()
        os.makedirs('./image/', exist_ok=True)
        self.cookies=self.get_date('cookies.txt')
        self.headers=self.get_date('headers.txt')

    def get_date(self,textname):
        with open(textname, 'r') as f:
            return json.loads(f.read()) #打开文件

    def get_html(self):
        html=self.Session.get(url=self.url,headers=self.headers,cookies=self.cookies) #用get方法获取网页源代码
        # print(html.text)
        return BeautifulSoup(html.text,"html.parser") #使用BeautifulSoup分析

    def post_html(self,**kwargs):
        html=self.Session.post(url=self.url,data=kwargs,headers=self.headers,cookies=self.cookies) #用post方法获取网页源代码
        # print(html.text)
        return BeautifulSoup(html.text,"html.parser") #使用BeautifulSoup分析

    def capture_pic(self,classname):
        for img in self.post_html().find_all('div',attrs={'class':classname}): #寻找class为classname的div中的内容
            print(img)

class internet_Ai_EPC(internet_Ai):
    def capture_pic(self):
        for img in self.get_html().find_all('img',{'src':re.compile("checkcode.asp?")}): #寻找所有src中带有checkcode.asp?的img
            print("http://epc.ustc.edu.cn/"+str(img)[10:-3].replace(' ','%'))
            with open('./image/checkcode.bmp','wb') as f:
                f.write(requests.get("http://epc.ustc.edu.cn/"+str(img)[10:-3]).content) #保存目标地址的图片到image

def main():
    iAi=internet_Ai_EPC('http://epc.ustc.edu.cn/n_left.asp')
    iAi.capture_pic()

if __name__=="__main__":
    main()
