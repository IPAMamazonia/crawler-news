#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        if tag["href"].startswith("/url?q=http"): # google
        #if tag["href"].startswith("http") and 'yahoo' not in tag["href"]: #yahoo
            tag = tag["href"].replace("/url?q=","") # google
            tag = re.sub(r'&sa.*', '', tag) # google
            links.add(tag)   
    
    return links

seen_urls = set()

filters = ['"desmatamento na amazônia" OR "desmatamento no cerrado" OR "fogo no cerrado" OR "deforestation in the amazon"']
    
payload = {'q': filters, 'tbm':'nws', 'tbs': 'qdr:d'} # google
#payload = {'p': filters, 'flt':'age:1d'} # yahoo

search = requests.get("https://www.google.com.br/search", params=payload) # google
#search = requests.get("https://br.news.search.yahoo.com/search", params=payload) # yahoo
links = extract_links(search.text)

for link in links:
    #print link
    if link not in seen_urls:
        seen_urls.add(link)
        page = requests.get(link)
        title = extract_title(page.text)
        if title:
            print(title)
            print link
