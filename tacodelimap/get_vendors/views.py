from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader

import requests
from bs4 import BeautifulSoup
import googlemaps
import pandas as pd

from .models import Vendor

import numpy as np
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

def index(request):
    latest_vendor_list = Vendor.objects.order_by('name')
    template = loader.get_template('get_vendors/index.html')
    context = {
        'latest_vendor_list': latest_vendor_list,
    }
    return HttpResponse(template.render(context, request))


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

def get_vendor_address(vendor):
    geolocator = Nominatim(user_agent="tacodeli")
    try:
        location = geolocator.geocode(vendor)
    except:
        location = None
    if location is None:
        return np.nan
    return location.address

def create_vendor(df):
    for index, row in df.iterrows():
        vendor_name = row["Vendors"]
        address = get_vendor_address(vendor_name)
        vendor = Vendor(name=vendor_name, address=address)
        vendor.save()

def detail(request, vendor_id):
    return HttpResponse("You're looking at vendor %s." % vendor_id)

def distance(request, vendor_id):
    response = "You're looking at the distance to vendor %s."
    return HttpResponse(response % vendor_id)

def hours(request, vendor_id):
    return HttpResponse("You're looking at the hours of %s." % vendor_id)