from django.contrib import admin
from .models import Transaction,Person,Asset
# Register your models here.
admin.site.register(Person)
admin.site.register(Asset)
admin.site.register(Transaction)
