"Importing modules working wirh database"
from django.db.models import Max,Min
from django.db.models import Q

from product.utils import CacheMixins
from product.serializers import PricesSerializer,ProductsSerializer,ShopsSerializer,Categories,MinMaxSerializer
from .models import Prices,Products,Shops
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

@api_view(['GET'])
def maxOfCategory(request,category): # pylint: disable=too-many-ancestors
    """find the product with the maximum price"""
    maximum = Prices.objects.filter(product_id__category_id__category_name=category).aggregate(Max('price'))
    products = Prices.objects.filter(price = maximum['price__max'] ,product_id__category=1 )
    serializer = MinMaxSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def minOfCategory(request,category): # pylint: disable=too-many-ancestors
    """find the product with the maximum price"""
    minimum = Prices.objects.filter(product_id__category_id__category_name=category).aggregate(Min('price'))
    products = Prices.objects.filter(price = minimum['price__min'] ,product_id__category=1 )
    serializer = MinMaxSerializer(products, many=True)
    return Response(serializer.data)


class ProductView(CacheMixins): # pylint: disable=too-many-ancestors
    """View for Product"""
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer


class PriceView(CacheMixins): # pylint: disable=too-many-ancestors
    """View for Prices"""
    queryset = Prices.objects.all()
    serializer_class = PricesSerializer

class ShopsView(CacheMixins): # pylint: disable=too-many-ancestors
    """View for Shops"""
    queryset = Shops.objects.all()
    serializer_class = ShopsSerializer


class ShopsProducts(CacheMixins): # pylint: disable=too-many-ancestors
    """View for Shops"""
    queryset = Shops.objects.all()
    serializer_class = ShopsSerializer





#def ProductfromShop (request,requestCategory,product_id):
 #   queryset = Products.objects.get(id=product_id)
  #  serializer = ProductsSerializer(queryset)
 #   return (status.HTTP_200_OK,serializer.data)


