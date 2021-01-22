from django.test import TestCase
from django.urls import reverse
from rest_framework import status
import pytest

from .models import Products,Prices
from rest_framework.test import APIClient
from rest_framework.reverse import reverse


class MaxMinPriceTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product = Products.objects.create(name = 'Iphone 10', category = 'Iphones')

        self.product2 = Products.objects.create(name = 'Iphone 12', category = 'Iphones')
        self.price = Prices.objects.create(name=self.product,
                                           technodom_price = 1000,
                                           sulpak_price=30,
                                           beliyveter_price=200,
                                           mechta_price=100)

        self.price2 = Prices.objects.create(name=self.product2,
                                            technodom_price = 10,
                                            sulpak_price=200,
                                            beliyveter_price=500,
                                            mechta_price=100)
    def test_product_can_be_created(self):
        product_result = Products.objects.last()
        assert product_result.name == 'Iphone 12'

    def test_price_can_be_created(self):
        price_result = Prices.objects.last()
        assert price_result.sulpak_price == 200

    def test_find_max(self):
        responce = self.client.get(reverse(viewname='max'))
        assert responce.json()!=None
        assert len(responce.json()) == 1
        assert responce.status_code == 200
        assert (responce.json()[0])['name_id']=='Iphone 10'

    def test_find_min(self):
        responce = self.client.get(reverse(viewname='min'))
        assert responce.json() != None
        assert len(responce.json()) == 1
        assert responce.status_code == 200
        assert (responce.json())[0]['name_id'] == 'Iphone 12'






