import imdb
import requests

API_KEY = "5c8ca1a6"

def get_one_film(id):
    url = f"http://www.omdbapi.com/?i={id}&apikey={API_KEY}"
    response = requests.get(url).text
    return response

ids = imdb.get_top250_ids()

#d = dict(get_one_film(ids[0]))

import json
d = json.loads(get_one_film(ids[0]))



#print(d["Title"])
#print(d.keys())
#print(d)