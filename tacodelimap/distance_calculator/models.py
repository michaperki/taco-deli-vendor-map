from django.db import models

# Create your models here.

class Vendor_ZipCode(models.Model):
    vendor = models.ForeignKey('get_vendors.Vendor', on_delete=models.CASCADE)
    zip_code = models.ForeignKey('zipcode.ZipCode', on_delete=models.CASCADE)
    distance = models.FloatField()

    def __str__(self):
        return self.vendor

    class Meta:
        ordering = ['vendor']