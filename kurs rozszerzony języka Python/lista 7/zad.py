from bs4 import BeautifulSoup
from bs4.element import  Comment
import requests
import re
import urllib.request
import threading
import queue

done_urls = set()

def get_urls_from_page(page):
    adres = '([a-zA-Z]+.)*[a-zA-Z]+'
    automat = re.compile('http://' + adres)

    with urllib.request.urlopen(page) as f:
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

def urls_and_content(page):
    try:
        urls = get_urls_from_page(page)
        content = get_content_from_page(page)
    except:
        print("something went wrong with", page)
        return ([],"")
    return (urls,content)


#skopiowany z wykladu i zmodyfikowany
def worker(shared_queue, results):
    while True:
        item = shared_queue.get()
        f, action, url, distance = item

        if distance == -1:
            break
        if url in done_urls:
            continue
        wynik = f(url)
        results[url] = action(wynik[1])
        print("--------------------------------------")
        print(results)
        print(len(results))
        print("--------------------------------------")
        done_urls.add(url)
        for new_url in wynik[0]:
            shared_queue.put((urls_and_content,action,new_url,distance-1))
        shared_queue.task_done()
        # print(threading.active_count())

    
def crawl(start_page, distance, action):
    shared_queue = queue.Queue()
    urls_done = set()
    shared_queue.put((urls_and_content, action, start_page, distance))
    #dane do workera to funkcja, funkcja do przetwarzania zawartosci strony, link do strony, i glebokosc

    results = {}

    #przygotownanie paru zadan zeby watki sie nie skonczyly na starcie
    for url in get_urls_from_page(start_page):
        shared_queue.put((urls_and_content, action, url, distance))

    watki = [threading.Thread(target=worker,
                                args=(shared_queue, results))
            for _ in range(5)]

    [w.start() for w in watki]
    return results
            
result_dict = crawl("http://www.ii.uni.wroc.pl",0,lambda tekst: "Python" in tekst)
print(result_dict)
