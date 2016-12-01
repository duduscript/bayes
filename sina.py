from bs4 import BeautifulSoup
import requests
import random
import queue
import sys
import os

def is_interested(url,sources):
    return isinstance(url,str) and any(map(lambda x:url.startswith('http://'+x),sources))

def get_type(url, sources):
    for source in sources:
        if source in url:
            return source
    return None

def islegal_title(title):
    ishan = lambda text:any('\u4e00' <= char <= '\u9fff' for char in text)
    return all(map(lambda ch:(ishan(ch) or ch.isprintable()) and ch != '�' and ch != '/',title))

def has_title(soup):
    return soup.title != None

def get_title(soup):
    title = soup.title.text
    if title != None:
        return title.split('|')[0]
    title = soup.find('h1',{'id':'artibodyTitle'})
    return title.text

def print_title(soup):
    print(get_title(soup))

def write_text(soup,path):
    def get_text(soup):
        div = soup.find('div',{'id':'artibody'})
        if div is None:
        	div = soup.find('div',{'id':'articleContent'})
        paragraphs = div.findAll('p')
        text = ''
        for paragraph in paragraphs:
            text += paragraph.text
        return text
    def isnews(soup):
        articleContent_div = soup.find('div',{'id':'articleContent'})
        artibody_div = soup.find('div',{'id':'artibody'})
        return articleContent_div != None or artibody_div != None
    if isnews(soup) and not os.path.exists(path):
        title = get_title(soup)
        fd = open(path,'w+')
        fd.write(get_text(soup))
        print_title(soup)
        fd.close()

def makedirs(sources):
    pwd,dirlist = os.getcwd(),os.listdir()
    for source in sources:
        if not (os.path.exists(pwd+'/'+source) and os.path.isdir(pwd+'/'+source)):
            os.makedirs(pwd+'/'+source)

def deal_with_url(url):
    if url != None and (url.startswith('/n') or url.startswith(' ')):
        return deal_with_url(url[1:])
    return url

def is_legal_url(url):
    return url != None and url.startswith('http://')

def is_in_sina(url):
	return url != None and 'sina' in url

def is_filter_sources(url,sources):
	return any(map(lambda x:x in url,filter_sources))

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
    except requests.exceptions.ChunkedEncodingError:
    	print('Connection refused!')
    return r

if __name__ == '__main__':
    #titles = init_titles()
    sources = ['edu','health','finance','tech','baby','sports','mil','ent','auto','games']
    filter_sources = ['mid','download','tag','app','weather','blog','db','fashion','slide','house','video','vip','vr','bbs','club','help','apk']
    makedirs(sources)
    init_url = 'http://www.sina.com.cn'
    urls = set()
    queue = queue.Queue()
    queue.put(init_url)
    while not queue.empty():
        source_url = queue.get()
        print(source_url)
        r = requests_get(source_url)
        if r != None and r.status_code == 200:
            r.encoding = 'utf-8'
            bsObj = BeautifulSoup(r.text,'lxml')
            for link in bsObj.find_all('a'):
                url = deal_with_url(link.get('href'))
                if url not in urls:
                    urls.add(url)
                    if is_legal_url(url) and is_in_sina(url) and is_interested(url,sources):
                        queue.put(url)
            if get_type(source_url,sources) != None \
            and has_title(bsObj) \
            and islegal_title(get_title(bsObj)) \
            and is_interested(source_url,sources):
                write_text(bsObj,'/'.join([os.getcwd(),get_type(source_url,sources),get_title(bsObj)]))
