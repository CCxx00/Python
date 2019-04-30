import requests
import json
import time

weekt={'Monday':'周一','Tuesday':'周二','Wednesday':'周三','Thursday':'周四','Friday':'周五','Saturday':'周六','Sunday':'周日'}

def fun():
    Session=requests.session()
    headers={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    html=Session.get('https://www.sojson.com/open/api/lunar/json.shtml',headers=headers) #用get方法获取网页源代码
    str1='【中丞集团 | 新闻早读】 '
    strnyr=str(html.json()['data']['year'])+'.'+str(html.json()['data']['month'])+'.'+str(html.json()['data']['day'])+' '
    strxq=weekt[html.json()['data']['week']]+' '
    strnl='农历'+html.json()['data']['cnmonth']+'月'+html.json()['data']['cnday']+'\n'
    str2='  点击：有声听读！\n  让世界每天在您耳边！'
    strz=str1+strnyr+strxq+strnl+str2
    src=r'C:\Users\admin\Desktop\updata.txt'
    with open(src,'w') as f:
        f.write(strz) #保存目标地址的图片到image

def set_pause_time(h,m,s):
    pause_time=h*60*60+m*60+s-time.localtime()[3]*60*60-time.localtime()[4]*60-time.localtime()[5]
    if pause_time<0:
        pause_time=0
    print(pause_time/60)
    return pause_time

def main():
    time.sleep(set_pause_time(23,59,59)+60)
    while True:
        fun()
        time.sleep(set_pause_time(23,59,59)+60)

if __name__=='__main__':
    main()
