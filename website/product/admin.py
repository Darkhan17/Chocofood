from django.contrib import admin
#from .models import Notebooks
from .models import Products, Prices, Categories,Shops,OldPrices

#admin.site.register(Notebooks)
# Register your models here.
admin.site.register(Products)
admin.site.register(Prices)
admin.site.register(Categories)
admin.site.register(Shops)
admin.site.register(OldPrices)