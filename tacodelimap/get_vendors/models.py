from django.db import models


class Vendor(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200, null=True, blank=True)
    # city = models.CharField(max_length=200)
    # state = models.CharField(max_length=200)
    # zip_code = models.CharField(max_length=200)
    # phone_number = models.CharField(max_length=200)
    # website = models.CharField(max_length=200)
    # latitude = models.FloatField()
    # longitude = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']