from bs4 import BeautifulSoup
import requests

link = "http://www.ii.uni.wroc.pl"

def get_urls(link, distance):
    result = []
    if distance == 0:
        return result

    response = requests.get(link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [e['href'] for e in soup.find_all(href=True)]
        print(links)

#get_urls(link,2)

x = requests.get("http://www.ii.uni.wroc.pl")
y = requests.get("http://www.red-team-design.com/google-font-api-and-typekit-solutions-vs-font-face")
print(x.status_code)
print(y.status_code)

soup = BeautifulSoup(x.text, 'html.parser')
#print(soup)
links = [e['href'] for e in soup.find_all(href=True) if 'https://' in e['href']]
print(links,"\n\n")
links = links + ["http://www.ii.uni.wroc.pl" + e['href'] for e in soup.find_all(href=True) if e['href'][0]=="/"]
print(links)
#print(soup.contents)