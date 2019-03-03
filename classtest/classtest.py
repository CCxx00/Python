from bs4 import BeautifulSoup
# from urllib.request import urlopen
from requests import session
import time
import re
import json

class internetAi(object):
    def __init__(self,url):
        self.url=url
        self.cookies=self.getText('cookies.txt')
        self.headers=self.getText('headers.txt')

    def getText(self,textname):
        with open(textname, 'r') as f:
            return json.loads(f.read()) #打开文件

    def postDatas(self):
        Session=session()
        html=Session.post(url=self.url,headers=self.headers,cookies=self.cookies) #获取网页源代码
        # print(BeautifulSoup(html.text).find('img',attrs={'alt':'cover'}))
        return BeautifulSoup(html.text) #使用BeautifulSoup分析

    def capturePic(self,classname):
        for img in self.postDatas().find_all('div',attrs={'class':classname}): #.find_all('img'):
            print(img)

def main():
    iAi=internetAi('https://www.zhihu.com/')
    # iAi.postDatas()
    iAi.capturePic('RichContent-cover-inner')

if __name__=="__main__":
    main()
