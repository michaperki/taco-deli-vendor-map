from django.shortcuts import render

from django.http import HttpResponse

import requests
from bs4 import BeautifulSoup
import googlemaps
import pandas as pd

def index(request):
    response = HttpResponse("Hello, world. You're at the taco deli vendor map index.") 
    return response

def get_list_of_vendors():
    # Get the data from the website
    url = 'https://www.tacodeli.com/locations/tacodeli-vendors/'
    headers={'User-Agent': 'Mozilla/5.0'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    # Get the data from the table
    list = soup.find("div", {"class": "su-column-inner"})
    vendors = list.text.splitlines()
    df = pd.DataFrame(vendors, columns=["Vendors"])
    df = df[df["Vendors"].str.match("^[a-zA-Z]")]
    df = df.reset_index(drop=True)
    return df