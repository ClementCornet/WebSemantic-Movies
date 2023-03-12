import requests
from bs4 import BeautifulSoup

url_top250_imdb = "https://www.imdb.com/chart/top/"

def get_top250_ids():
    page = requests.get(url_top250_imdb).text

    soup = BeautifulSoup(page,features="lxml")
    ids = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith("/title/tt"):
            id = href.split('/')[2]
            ids.append(id)

    ids = list(set(ids))
    if len(ids) != 250:
        raise ValueError("Did not return 250 values")
    
    return ids