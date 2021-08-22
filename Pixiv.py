from selenium import webdriver
import re
import time
from bs4 import BeautifulSoup
import requests
import os   
import random
import winsound
import sqlite3



'''
1、输入作者uid    创建作者文件夹
2、进入作品页面1-？页，获取wid    创建作品文件夹（可选，主要看单个作品图片数量）
3、进入作品页面，获取url    保存图片'''


def getHtml(url,driver):
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    #driver.execute_script("alert('To Buttom')")
    time.sleep(8)
    return driver.page_source

def downloadComic(uid,name,driver):
    url = "https://www.pixiv.net/users/"+ uid +"/artworks"
    html = getHtml(url,driver)
    soup = BeautifulSoup(html,"html.parser")

    s = set()
    for i in soup.find_all(class_='_2m8qrc7'):
        try:
            s.add('https://www.pixiv.net'+i['href'])
        except:
            continue

    d = dict()
    for i in s:
        html = getHtml(i,driver)
        soup = BeautifulSoup(html,"html.parser")
        for j in soup.find_all(class_='hegAwd'):
            d[j.string] = 'https://www.pixiv.net'+j['href']

    root = "d:/Spider/pic/"+name+"/"
    if not os.path.exists(root):
        os.makedirs(root)

    illegalChaSet = r"[\/\\\:\*\?\"\<\>\|\.]"
    header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
          'referer':'https://www.pixiv.net/'}
    for i in d:
        tmpStr = re.sub(illegalChaSet,"_",i)
        path = root + tmpStr + "/"
        if not os.path.exists(path):
            os.makedirs(path)
        url = d.get(i)
        try:
            driver.get(url)
            try:
                button = driver.find_element_by_class_name('cwSjFV')
                button.click()
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            except:
                time.sleep(0.01)
            time.sleep(8)
            html = driver.page_source
            pattern = r'https://i.pximg.net/img-original.*?p\d{1,3}.\w{3}'
            tmp = re.findall(pattern,html)
            for j in tmp:
                try:
                    r = requests.get(j,headers=header)
                    r.raise_for_status()
                    fname = path+j.split('/')[-1]
                    with open(fname,'wb') as f:
                        f.write(r.content)
                        f.close()
                    time.sleep(random.random())
                except:
                    continue
            print(i+":下载成功！")
        except:
            continue
    return




def getWorksList(uid,driver):
    url = "https://www.pixiv.net/users/"+ uid +"/artworks"
    #driver.get(url)
    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    #driver.execute_script("alert('To Buttom')")
    #time.sleep(8)
    #html = driver.page_source
    html = getHtml(url,driver)
    

    pattern = r'/users/\d{6,8}/artworks.p=\d'
    pls = re.findall(pattern,html)
    pls.append(url[21:])
    s = set(pls)
    tmp = []

    for i in s:
        tmp.append(i)

    for i in tmp:
        print(i)

    purl = []
    for i in range(len(tmp)):
        purl.append("https://www.pixiv.net"+tmp[i])
    
    wls = []
    pattern = r'/artworks/\d{8}'
    for i in purl:
        html = getHtml(i,driver)
        s = set(re.findall(pattern,html))
        for j in s:
            wls.append("https://www.pixiv.net" + j)

    print(len(wls))
#    for i in wls:
#        print(i)
    
    #创建作品文件夹
    return wls



def getPurl(wls,driver):
    ls = []
    for i in wls:
        try:
            driver.get(i)
            try:
                button = driver.find_element_by_class_name('cwSjFV')
                button.click()
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            except:
                time.sleep(1)
            time.sleep(8)
            html = driver.page_source
            pattern = r'https://i.pximg.net/img-original.*?p\d{1,3}.\w{3}'
            tmp = re.findall(pattern,html)
#        for j in tmp:
#            print(j)
            for j in tmp:
                ls.append(j)
        except:
            continue

    print(len(ls))
#    for i in ls:
#        print(i)
    return ls

def SavePic(pls,name):
    #name = input("请输入文件夹名称（推荐用作者名）:")
    #name = "マシマサキ"
    root = "d:/Spider/pic/"+name+"/"
    header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
          'referer':'https://www.pixiv.net/'}
    if not os.path.exists(root):
        os.makedirs(root)

    for i in pls:
        try:
            r = requests.get(i,headers=header)
            r.raise_for_status()
            if(r.status_code==200):
                print(i.split('/')[-1]+"获取成功")
            path = root+i.split('/')[-1]
            with open(path,'wb') as f:
                f.write(r.content)
                f.close()
            time.sleep(random.random())
        except:
            continue
    return


def printWorksList(uid,driver,n=1):

    ls = []
    for i in range(1,n+1):
        url = 'https://www.pixiv.net/users/'+uid+'/artworks?p='+str(i)
        html = getHtml(url,driver)
        soup = BeautifulSoup(html,'html.parser')
        print('\n第{0}页:'.format(i))
        for j in soup(class_='hegAwd'):
            ls.append(j['href'].split('/')[-1])
            print(j['href'].split('/')[-1]+':'+j.string)
    print('\ntotal:{0}\n'.format(len(ls)))
    return ls

def printWorkInfo(aid,driver):

    url = 'https://www.pixiv.net/artworks/'+str(aid)
    html = getHtml(url,driver)
    soup = BeautifulSoup(html,'html.parser')
    info = [soup.find(class_='iFrcHJ').getText(),
            soup.find(class_='feoVvS').string,
            soup.find_all('dd')[0].string,
            soup.find_all('dd')[1].string,
            soup.find_all('dd')[2].string,
            soup.find(class_='cuUtZw').string]
    print(info)

def getInfo(aid):
    url = 'https://www.pixiv.net/artworks/'+str(aid)
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}
    r = requests.get(url,headers=headers)
    likeCount = r'likeCount":(.*?),'
    bookmarkCount = r'bookmarkCount":(.*?),'
    viewCount = r'viewCount":(.*?),'
    illustTitle = r'illustTitle":"(.*?)"'
    l = []
    l.append(re.findall(likeCount,r.text)[0])
    l.append(re.findall(bookmarkCount,r.text)[0])
    l.append(re.findall(viewCount,r.text)[0])
    l.append(re.findall(illustTitle,r.text)[0])
    print(l)
    return

def saveToDB(aid,con):
    
    url = 'https://www.pixiv.net/artworks/'+str(aid)
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}
    r = requests.get(url,headers=headers)
    likeCount = r'likeCount":(.*?),'
    bookmarkCount = r'bookmarkCount":(.*?),'
    viewCount = r'viewCount":(.*?),'
    illustTitle = r'illustTitle":"(.*?)"'
    lc = int(re.findall(likeCount,r.text)[0])
    bmc = int(re.findall(bookmarkCount,r.text)[0])
    vc = int(re.findall(viewCount,r.text)[0])
    title = re.findall(illustTitle,r.text)[0]

    t = (title,lc,bmc,vc)
    cur = con.cursor()
    cur.execute("insert into pixiv values (?,?,?,?)",t)
    con.commit()
    print(t)


def downloadPicture(uid,driver,name):
    wls = getWorksList(uid,driver)
    pls = getPurl(wls,driver)
    SavePic(pls,name)
    return 0

def getDriver():
    op = webdriver.ChromeOptions()
    op.add_argument(r"--user-data-dir=D:\Spider\User Data")
    #Options.add_argument('--headless')    #不打开浏览器
    #Options.add_experimental_option('excludeSwitches', ['enable-automation'])
    return webdriver.Chrome(options=op)

def main():

    driver = getDriver()

#DB
    #con = sqlite3.connect('d:/example.db')
    
    uid = input("请输入作者uid:")
    name = input("请输入文件夹名称（推荐用作者名）:")

    #cur.execute('''create table pixiv (title, like, bookmark, view)''')
    #ls = printWorksList(uid,driver)
    #for i in ls:
    #    saveToDB(i,con)

    #con.close()

    #print('作品信息:')
    #for i in ls:
    #    getInfo(i)

    downloadPicture(uid,driver,name)    #图片

    #downloadComic(uid,name,driver)    #漫画
    
    winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
    return

main()






#pattern = r'/artworks/\d{8}'    #套图url

#pattern = '/users/'+ uid + r'/artworks[?p=]{3}\d'

#pattern = r'https:.*?img-original.*?p\d.\w{3}'    #原图
#pattern = r'>1/\d{1,3}'    #套图数量



#soup.find(class_='iFrcHJ').getText()   #作者名
#soup.find(class_='feoVvS').string      #标题
#soup.find_all('dd')[0].string          #赞
#soup.find_all('dd')[1].string          #收藏
#soup.find_all('dd')[2].string          #浏览量
#soup.find(class_='cuUtZw').string      #上传日期


            



#regex = re.compile(pattern)
#ls = regex.findall(html)



#BeautifulSoup
#soup = BeautifulSoup(html,'html.parser')
#print(soup.prettify())



