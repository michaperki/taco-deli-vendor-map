from django.db import models

# Create your models here.

class Vendor_ZipCode(models.Model):
    vendor = models.ForeignKey('get_vendors.Vendor', on_delete=models.CASCADE)
    zip_code = models.ForeignKey('zipcode.ZipCode', on_delete=models.CASCADE)
    distance = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.vendor.name, self.vendor.zip_code, self.zip_code.zip_code, self.distance

    class Meta:
        ordering = ['vendor']