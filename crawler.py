from bs4 import BeautifulSoup
import re
import requests

def extract_title(content):
    soup = BeautifulSoup(content, "lxml")
    tag = soup.find("title", text=True)
    
    if not tag:
        return None
    
    return tag.string.strip()

def extract_links(content):
    #print content
    soup = BeautifulSoup(content, "lxml")
    links = set()
    
    for tag in soup.find_all("a", href=True):
        if tag["href"].startswith("/url?q=http"):
            tag = tag["href"].replace("/url?q=","")
            tag = re.sub(r'&sa.*', '', tag)
            links.add(tag)
    
    return links

parameters = [
    {'desmatamento', 'amazônia'},
    {'desmatamento', 'cerrado'},
    {'desmatamento', 'ipam'},
    {'floresta', 'amazônia'},
    {'floresta', 'cerrado'},
    {'floresta', 'ipam'}
]

payload = {'q': ['desmatamento', 'cerrado'], 'tbm':'nws', 'tbs': 'qdr:d'}

search = requests.get("https://www.google.com.br/search", params=payload)
links = extract_links(search.text)

for link in links:
    page = requests.get(link)
    title = extract_title(page.text)
    #some_list = ['desmatamento', 'floresta', 'ameaças', 'amazônia', 'cerrado', 'fogo', 'deforestation', 'forest', 'fire', 'IPAM']
    if title:
        #if any(s in title.encode('utf-8') for s in some_list):
            print(title)
            print link
