from django.db import models
from django.contrib.auth.models import User
import datetime
from decimal import Decimal
# Create your models here.

class Transaction(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	user_handle = models.CharField(max_length = 50)
	name = models.CharField(max_length = 100)
	asset_id = models.CharField(max_length = 50)
	asset_name = models.CharField(max_length = 100)
	price = models.DecimalField(max_digits=8,decimal_places=2,default=Decimal('0.00'))
	units = models.DecimalField(max_digits=8,decimal_places=2,default=Decimal('0.00'))
	trans_type = models.IntegerField(default = 1) # buy-1 , sell-2
	date_time = models.DateTimeField(auto_now_add=True, blank=True)






