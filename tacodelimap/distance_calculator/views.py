from django.http import HttpResponse
from django.shortcuts import render
from geopy.distance import geodesic
from get_vendors.models import Vendor
from zipcode.models import ZipCode
from . models import Vendor_ZipCode
import pgeocode

# For every Vendor object, calculate the distance from the user's location to the Vendor's location.
#   - If the Vendor's location is not available, then the distance is set to 0.
#   - If the Vendor's location is available, then the distance is calculated using the geodesic function.
#   - The geodesic function returns the distance in miles.
#   - The distance is stored in the Vendor object.

def calculate_distance():
    # Get the Vendor objects
    vendor_list = Vendor.objects.all()

    # Get the user's location
    zipcode = ZipCode.objects.all()[0]

    dist = pgeocode.GeoDistance('US')

    # Calculate the distance from the user's location to the Vendor's location
    for vendor in vendor_list:
        vz = Vendor_ZipCode(vendor=vendor, zip_code=zipcode)
        if vendor.zip_code is None:
            vendor.zip_code = 0
        else:
            vendor.distance = dist.query_postal_code(zipcode.zip_code, vendor.zip_code)
            print(vendor.distance)

        vz.distance = vendor.distance
        vz.save()

def index(request):
    latest_distance_list = Vendor_ZipCode.objects.order_by('-distance')
    context = {'latest_distance_list': latest_distance_list}
    return render(request, 'distance_calculator/index.html', context)

def detail(request, vendor_zipcode_id):
    return HttpResponse("You're looking at vendor_zipcode %s." % vendor_zipcode_id)