from bs4 import BeautifulSoup
from bs4.element import  Comment
import requests
import re
import urllib.request


def get_urls_from_page(page):
    adres = '([a-zA-Z]+.)*[a-zA-Z]+'
    automat = re.compile('http://' + adres)

    with urllib.request.urlopen(page, timeout=2) as f:
        tekst = f.read().decode('utf-8')

    return [ url.group() for url in automat.finditer(tekst) ]


#ta funkcja jest skopiowana ze stack overflow
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def get_content_from_page(page):
    response = requests.get(page)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.find_all(string=True)
    visible_text = filter(tag_visible,text)
    result = ".".join([elem.strip('\n') for elem in visible_text if elem!="\n" and elem!=""])
    return result

    
def crawl(start_page, distance, action):
    urls_to_do = [start_page]
    next_urls = []
    urls_done = set()

    while distance>=0:
        for url in urls_to_do:
            if url not in urls_done:
                try:
                    yield (url, action(get_content_from_page(url)))
                except:
                    yield (url, "something was wrong with this url")

                urls_done.add(url)
                try:
                    next_urls.extend(get_urls_from_page(url))
                except:
                    yield (url, "unable to scrape urls from this page")
                urls_to_do.remove(url)
            else:
                urls_to_do.remove(url)

            #print("how many urls left:", len(urls_to_do))
            if len(urls_to_do) == 0:
                distance = distance-1
                urls_to_do = next_urls
                next_urls = []
            

for url,wynik in crawl("http://www.ii.uni.wroc.pl",1,lambda tekst: "Python" in tekst):
    print(f"{url}: {wynik}")
