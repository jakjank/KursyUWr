import bs4
import re
import urllib.request
import requests

# adres = '([a-zA-Z]+.)*[a-zA-Z]+'
# automat = re.compile('http://' + adres)
# print(automat)

# host = "http://www.ii.uni.wroc.pl"
# with urllib.request.urlopen(host) as f:
#     tekst = f.read().decode('utf8')
#print(tekst)

# print([url.group() for url in automat.finditer(tekst)])

def get_urls(url , distance):
    result = []
    if distance == 0:
        return result

    else:
        adres = '([a-zA-Z]+.)*[a-zA-Z]+'
        automat = re.compile('http://' + adres)

        host = url
        try:
            f = urllib.request.urlopen(host)
        except:
            print("smh wrong with",url)
            return result
        
        tekst = f.read().decode('utf8')

        new_urls = [url.group() for url in automat.finditer(tekst)]

        for elem in new_urls:
            if elem not in result:
                result.append(elem)
                result = result + get_urls(elem,distance-1)
            else:
                pass
                #print(elem)

        return result

def crawl(start_page,distance,action):
    result = []
    all_urls = get_urls(start_page,distance)
    for url in all_urls:
        try:
            x = urllib.request.urlopen(url)
            result.append((url,action(x.read().decode('utf8'))))
        except:
            print("smh2 wrong with", url)
    return result
        


for url,res in crawl("http://www.ii.uni.wroc.pl",2, lambda tekst : "Python" in tekst):
    print(f"{url}: {res}")



#print(get_urls("http://www.ii.uni.wroc.pl",2))
