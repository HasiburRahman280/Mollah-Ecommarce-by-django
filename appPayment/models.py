from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class BillingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='billing_ads')
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    phone = models.CharField(max_length=16, blank=True, null=True)
    address= models.TextField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}"

    def is_fully_filled(self):
        fields_names =[f.name for f in self._meta.get_fields()]
        for fields_name in fields_names:
            value = getattr(self,fields_name)
            if value is None or value =='':
                return False
            else:
                return True
