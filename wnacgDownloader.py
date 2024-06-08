import os
import re
import time
import requests

from bs4 import BeautifulSoup

#适用的本子站：https://www.wnacg.com/

startUrlId = 17172927
endUrlId = 17172949

#startUrl = 'https://www.wnacg.com/photos-view-id-17172914.html'
startUrl = 'https://www.wnacg.com/photos-view-id-'+str(startUrlId)+'.html'
#起始url

#endUrl = 'https://www.wnacg.com/photos-view-id-17172949.html'
endUrl = 'https://www.wnacg.com/photos-view-id-'+str(endUrlId)+'.html'
#终止url，注意，这个应当是本子的第一页，不然最后一张不下载

#startUrl = input("startUrl:")
#endUrl = input("endUrl:")
#如果你希望同时启动多个程序的话

#tryIDM = True
tryIDM = False
#是否导出为idm文件

dirName = "性愛＆迷宮!! 5"
os.makedirs('./'+dirName+'/', exist_ok=True)
#漫画名用作文件夹名

sleepTime=0.1
#下载间歇

timeout=10
#连接超时

proxies = {
'http': 'http://127.0.0.1:10279',
'https': 'http://127.0.0.1:10279',
}
#配置代理

os.system("cls")
#os.system("clear")
#清屏

def imgDownloader(url,dirName,title,proxies,timeout):
    print(title)
    print(url)
    imgUrl = requests.get(url, proxies=proxies,timeout=timeout)
    
    img=open("./"+dirName+"/"+title+".jpg", "wb+")
    img.write(imgUrl.content)
    img.close()
    
    print("fin")
#下载器部分

def useIDM(url,title):
    print(title)
    print(url)
    
    urlList=open("./idm.ef2", "a")
    urlList.write("<\n"+url+"\nUser-Agent: netdisk;7.2.6.2;PC\n>\n")
    urlList.close()
    
    print("fin")
    

def getUrl(url,endUrl,dirName,proxies,timeout):
    website = requests.get(url, proxies=proxies,timeout=timeout) 
    soup = BeautifulSoup(website.text,features="html.parser")
    #获取网页
    
    title = soup.find('h1').get_text().replace(' ', '').replace('\n', '').replace('\r', '')
    #获取标题，用作文件名，去除空格、换行符
    
    link = soup.find('img',src=re.compile(r"img4.qy0.ru"))
    
    url = "https:"+link['src']
    #获取图片的地址
    if tryIDM == True:
        useIDM(url,title)
    else:
        imgDownloader(url,dirName,title,proxies,timeout)
    
    time.sleep(sleepTime)
    
    nextUrl = soup.find('link',rel="prerender")
    nextUrl = "https://www.wnacg.com"+nextUrl['href']
    #获取下一页的地址
    print("nextUrl:")
    print(nextUrl)
    if endUrl==nextUrl:
        exit()
    else:
        getUrl(nextUrl,endUrl,dirName,proxies,timeout)

getUrl(startUrl,endUrl,dirName,proxies,timeout)