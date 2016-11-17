from bs4 import BeautifulSoup
import requests
import random
import queue
import sys
import os

MAX_PAGENUM = 1000

def is_interested(url):
    #source = ['blog','vr','news','fashion','baby','edu','kaoshi','jiaju','eladies','dj','games','app','tech','zhongce','book','finance','sports']
    source = ['news']
    return hasattr(url,'startswith') and any(map(lambda x:url.startswith(x),map(lambda title:'http://'+title,source)))

def ishan(text):
    return any('\u4e00' <= char <= '\u9fff' for char in text)

def islegal_title(title):
    return all(map(lambda ch:(ishan(ch) or ch.isprintable()) and ch != '�' and ch != '/',title))

def has_title(soup):
    return soup.title != None

def get_title(soup):
    title = soup.title.text
    return title.split('|')[0]

def print_title(soup):
    title = get_title(soup)
    print(title)

def get_text(soup):
    articleContent_div = soup.find('div',{'id':'articleContent'})
    paragraphs = articleContent_div.findAll('p')
    text = ''
    for paragraph in paragraphs:
        text += paragraph.text
    return text

def isnews(soup):
    articleContent_div = soup.find('div',{'id':'articleContent'})
    return False if articleContent_div is None else True

def write_text(soup):
    if isnews(soup):
        title = get_title(soup)
        fd = open('news/'+title,'w+')
        fd.write(get_text(soup))
        print_title(soup)
        fd.close()

def requests_get(url):
    USER_AGENTS = (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100 101 Firefox/22.0',
        'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0',
        ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko) '
         'Chrome/19.0.1084.46 Safari/536.5'),
        ('Mozilla/5.0 (Windows; Windows NT 6.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46'
         'Safari/536.5')
    )
    r = None
    try:
        r = requests.get(
            url,
            headers={'User-Agent': random.choice(USER_AGENTS)}
        )
    except ConnectionError:
        #r.status_code = "Cinnection refused!"
        print('Connection refused!')
    except requests.exceptions.ConnectionError:
        #r.status_code = "Cinnection refused!"
        print('Connection refused!')
    return r


req = requests_get('http://www.sina.com.cn')
req.encoding = 'utf-8'


titles = set()
queue = queue.Queue()
queue.put(req.text)
while not queue.empty() or len(titles) >= MAX_PAGENUM:
    html = queue.get()
    bsObj = BeautifulSoup(html,'lxml')
    for link in bsObj.find_all('a'):
        url = link.get('href')
        if is_interested(url):
            r = requests_get(url)
            if r == None or r.status_code != 200:
                continue
            r.encoding = 'utf-8'
            soup = BeautifulSoup(r.text,'lxml')
            if not has_title(soup):
                continue
            title = get_title(soup)
            if islegal_title(title) and title not in titles:
                queue.put(r.text)
                write_text(soup)
                titles.add(title)
