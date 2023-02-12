from django.db import models

# Create your models here.

class ZipCode(models.Model):
    zip_code = models.CharField(max_length=200)

    def __str__(self):
        return self.zip_code

    class Meta:
        ordering = ['zip_code']