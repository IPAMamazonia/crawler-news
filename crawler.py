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
        if tag["href"].startswith("/url?q=http"):
            tag = tag["href"].replace("/url?q=","")
            tag = re.sub(r'&sa.*', '', tag)
            links.add(tag)
    
    return links

filters = [
    {'desmatamento', 'amazônia'},
    {'desmatamento', 'cerrado'},
    {'desmatamento', 'ipam'},
    {'desmatamento', 'floresta'},
    {'floresta', 'amazônia'},
    {'floresta', 'cerrado'},
    {'floresta', 'ipam'},
    {'garimpo', 'amazônia'},
    {'garimpo', 'cerrado'},
    {'fogo', 'amazônia'},
    {'fogo', 'cerrado'},
    {'fogo', 'unidade de conservação'},
    {'fogo', 'terra indígena'},
    {'fogo', 'floresta'},
    {'fogo', 'área protegida'},
    {'invação', 'unidade de conservação'},
    {'invação', 'terra indígena'},
    {'perda', 'carbono', 'floresta'},
    {'emissão', 'CO2', 'floresta'},
    {'emissão', 'CO2', 'desmatamento'},
    {'estoque', 'carbono', 'floresta'},
    {'estoque', 'carbono', 'regeneração'},
    {'map', 'biomas'},
    {'agricultura', 'familiar', 'amazônia'},
    {'agricultura', 'familiar', 'cerrado'},
    {'agricultura', 'familiar', 'mato grosso'},
    {'agricultura', 'familiar', 'acre'},
    {'agricultura', 'familiar', 'rondônia'},
    {'agricultura', 'familiar', 'amazonas'},
    {'agricultura', 'familiar', 'para'},
    {'agricultura', 'familiar', 'roraima'},
    {'agricultura', 'familiar', 'amapá'},
    {'agricultura', 'familiar', 'acre'},
    {'extrativismo', 'amazônia'},
    {'extrativismo', 'cerrado'},
    {'extração', 'madeira', 'ilegal', 'amazônia'},
    {'extração', 'madeira', 'ilegal', 'cerrado'},
    {'conflitos', 'amazônia'},
    {'conflitos', 'cerrado'},
    {'pesquisa', 'ipam'},
    {'pesquisadores', 'ipam'},
    {'estudo', 'ipam'},
    {'ipam', 'desenvolve', 'sistema'},
    {'ipam', 'plataforma'},
    {'ipam', 'alerta indígena'},
    {'amazônia', 'seca'},
    {'cerrado', 'seca'},
    {'amazônia', 'seca', 'fogo'},
    {'cerrado', 'seca', 'fogo'},
    {'amazônia', 'soja', 'desmatamento'},
    {'cerrado', 'soja', 'desmatamento'},
]

seen_urls = set()
for filter in filters:
    
    payload = {'q': filter, 'tbm':'nws', 'tbs': 'qdr:d'}

    search = requests.get("https://www.google.com.br/search", params=payload)
    links = extract_links(search.text)
    
    print search.url

    for link in links:
        print link
        if link not in seen_urls:
            seen_urls.add(link)
            page = requests.get(link)
            title = extract_title(page.text)
            if title:
                print(title)
                print link
