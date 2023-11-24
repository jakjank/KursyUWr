# Zalozylem, ze tresc strony, ktora jest argumentem funkcji action,
# to widoczny tekst na stronie

from bs4 import BeautifulSoup
from bs4.element import  Comment
import requests


def get_urls(page, distance):
    result = [page]
    if distance == 0:
        return result

    try:
        response = requests.get(page, timeout=1)
    except:
        print("Unable to get response from", page)
        return []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        hrefs = soup.find_all(href=True)
        links = []

        for elem in hrefs:
            try:
                if len(elem['href']) > 0:
                    if "http" == elem['href'][0:4]:
                        links.append(elem['href'])    #dodajemy linki bezwgledne
                    if elem['href'][0]=="/":
                        links.append(page + elem['href'])   #dodajemy linki wzgledne 
                    if elem['href'][0:2]=="..":
                        links.append(page + elem['href'][2:])  #znowu link wzgledny
            except:
                print(elem)
                pass

        for link in links:
            try:
                result = result + [e for e in get_urls(link, distance-1) if e not in result]
            except:
                print("Someting wrong with",link)
                try:
                    resp_status = requests.get(link).status_code
                    print("Response status code:", resp_status)
                except:
                    print("Unable to get response status code")

        return result

def crawl(start_page, distance, action):
    result = []
    all_urls = get_urls(start_page, distance)
    print(f"------------------------------------------------{len(all_urls)} znalezionych stron")
    for url in all_urls:
        try:
            response = requests.get(url, timeout=1)
        except:
            print("2Unable to get response from", url) 
            #nie otwiera z reguly (poza http://portal.uwr.edu.pl/) roznych linkow, wiec to chyba kwestia czasu odpowiedzi
            continue
        
        soup = BeautifulSoup(response.text, 'html.parser')
        text = ".".join(soup.find_all(string=True))
        result.append((url,action(text)))
        #print("dzialamy!")
    return result

#dla distance=2 jest to ok 15000 znalezionych stron i trwa to ho ho ho
for url,res in crawl("http://www.ii.uni.wroc.pl", 1, lambda tekst : [zdanie for zdanie in tekst.split(".") if "Python" in zdanie]):
    # if len(res) > 0:
    #     print(f"\n{url} :")
    #     for e in res:
    #         print(e)
    print(url)