from django.shortcuts import get_object_or_404 ,render

from django.http import HttpResponse, Http404

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
    context = {'latest_vendor_list': latest_vendor_list}
    return render(request, 'get_vendors/index.html', context)

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

def validate_address(address):
    if address is None:
        return False
    if "Austin" in address:
        return True
    return False

def get_vendor_address(vendor):
    geolocator = Nominatim(user_agent="tacodeli")
    try:
        location = geolocator.geocode(vendor)
    except:
        location = None
    if location is None:
        return np.nan
    else: 
        if validate_address(location.address):
            return location.address
        else:
            return np.nan

def create_vendor(df):
    for index, row in df.iterrows():
        vendor_name = row["Vendors"]
        address = get_vendor_address(vendor_name)
        vendor = Vendor(name=vendor_name, address=address)
        vendor.save()

def detail(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    return render(request, 'get_vendors/detail.html', {'vendor': vendor})

def distance(request, vendor_id):
    response = "You're looking at the distance to vendor %s."
    return HttpResponse(response % vendor_id)

def hours(request, vendor_id):
    return HttpResponse("You're looking at the hours of %s." % vendor_id)

