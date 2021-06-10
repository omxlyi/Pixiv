from selenium import webdriver
import re
import time
from bs4 import BeautifulSoup
import requests
import os   
import random
import winsound



'''
1、输入作者uid    创建作者文件夹
2、进入作品页面1-？页，获取wid    创建作品文件夹（可选，主要看单个作品图片数量）
3、进入作品页面，获取url    保存图片'''

def downloadPic(uid,name,driver):
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


def GenerateFolder():
    #uid = input("请输入作者uid:")
    #name = input("请输入文件夹名称（推荐用作者名）:")
    uid = "18403608"
    name = "マシマサキ"
    root = "d:/Spider/pic/"+name+"/"
    if not os.path.exists(root):
        os.makedirs(root)
    print("Pixiv作者{}的文件夹创建成功！".format(name))
    return uid
        
def getHTML(url,driver):
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    #driver.execute_script("alert('To Buttom')")
    time.sleep(8)
    html = driver.page_source
    return html

#每一页、每个作品名称、url
def F(uid,driver):
    url = "https://www.pixiv.net/users/"+ uid +"/artworks"
    html = getHTML(url,driver)

    soup = BeautifulSoup(html,"html.parser")
    s = set()
    for i in soup.find_all(class_='_2m8qrc7'):
        try:
            s.add('https://www.pixiv.net'+i['href'])
        except:
            continue
    dict = {}
    for i in s:
        html = getHTML(i,driver)
        soup = BeautifulSoup(html,"html.parser")
        for j in soup.find_all(class_='hegAwd'):
            dict[j.string] = 'https://www.pixiv.net'+j['href']

    #print(dict.items())
    #print(len(dict))
    return dict

def getWorksList(uid,driver):
    url = "https://www.pixiv.net/users/"+ uid +"/artworks"
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    #driver.execute_script("alert('To Buttom')")
    time.sleep(8)
    html = driver.page_source

    pattern = r'/users/\d{7,8}/artworks.p=\d'
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
        html = getHTML(i,driver)
        s = set(re.findall(pattern,html))
        for j in s:
            wls.append("https://www.pixiv.net" + j)

    print(len(wls))
#    for i in wls:
#        print(i)
    
    #创建作品文件夹
    return wls

def F2(dict,driver,name):
    root = "d:/Spider/pic/"+name+"/"
    if not os.path.exists(root):
        os.makedirs(root)
    
    header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
          'referer':'https://www.pixiv.net/'}
    illegalChaSet = r"[\/\\\:\*\?\"\<\>\|\.]"
    for i in dict:
        tmpStr = re.sub(illegalChaSet,"_",i)
        path = root+tmpStr+"/"
        os.makedirs(path)
        url = dict.get(i)
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
    winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
    return


#删掉    
def getHtmlText(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(options = chrome_options)
    browser = webdriver.Chrome()
    browser.get(url)
#页面下拉
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(8)
    html = browser.page_source
    browser.close()
    return html

def showUrl(uid,driver):
    url = "https://www.pixiv.net/users/"+ uid +"/artworks"
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    driver.execute_script("alert('To Buttom')")


def main():

    Options = webdriver.ChromeOptions()
    Options.add_argument(r"--user-data-dir=D:\Spider\User Data")
    #Options.add_argument('--headless')    #不打开浏览器
    Options.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = webdriver.Chrome(options=Options)

    uid = input("请输入作者uid:")
    name = input("请输入文件夹名称（推荐用作者名）:")
    
    wls = getWorksList(uid,driver)
    pls = getPurl(wls,driver)
    SavePic(pls,name)

    #downloadPic(uid,name,driver)
    
    return

main()


def getPageUrlList(url,html):
    pattern = '/users/'+ uid + r'/artworks[?p=]{3}\d'
    s = set(re.findall(pattern,html))
    ls = []
    ls.append(url)
    for i in s:
        ls.append("https://www.pixiv.net" + i)
    return ls

def getPicUrlList(list):
    Tmp = []
    pattern = r'/artworks/\d{8}'
    for i in list:
        html = getHtmlText(i)
        s = set(re.findall(pattern,html))
        for j in s:
            Tmp.append("https://www.pixiv.net" + j)
    return Tmp




#pattern = r'/artworks/\d{8}'    #套图url

#pattern = '/users/'+ uid + r'/artworks[?p=]{3}\d'

#pattern = r'https:.*?img-original.*?p\d.\w{3}'    #原图
#pattern = r'>1/\d{1,3}'    #套图数量








            



#regex = re.compile(pattern)
#ls = regex.findall(html)



#BeautifulSoup
#soup = BeautifulSoup(html,'html.parser')
#print(soup.prettify())











#header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
#          'referer':'https://www.pixiv.net/'}
#root = "d:/Spider/pic/ASK/"
#if not os.path.exists(root):
#    os.makedirs(root)

#for item in urls:
#    try:
#        r = requests.get(item,headers=header)
#        r.raise_for_status()
#        if(r.status_code==200):
#            print(item.split('/')[-1]+"获取成功")
#        path = root+item.split('/')[-1]
#        with open(path,'wb') as f:
#            f.write(r.content)
#            f.close()
#        time.sleep(random.random())
#    except:
#        continue
        
#winsound.PlaySound("SystemExit", winsound.SND_ALIAS)


#获得以前浏览器信息
#from selenium import webdriver
#Options = webdriver.ChromeOptions()
#Options.add_argument(r"--user-data-dir=D:\Spider\User Data")
#Options.add_experimental_option('excludeSwitches', ['enable-automation'])
#driver = webdriver.Chrome(options=Options)
#driver.get("https://www.pixiv.net/users/1960050/artworks")
