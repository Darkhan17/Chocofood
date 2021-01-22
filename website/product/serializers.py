"""importing models"""
from .models import Prices,Products,Shops,Categories,OldPrices

from rest_framework import serializers


class OldPricesSerializer(serializers.ModelSerializer):
    """Old prices Serializer class"""
    class Meta:
        """Meta class"""
        model = OldPrices
        fields = ('price','time')


class PricesSerializer(serializers.ModelSerializer):
    """Price Serializer class"""
    shop_name = serializers.CharField(source='shop.shop_name')
    class Meta:
        """Meta class"""
        model = Prices
        fields = ('shop_name','price')


class PricesShopSerializer(serializers.ModelSerializer):
    """Price Serializer class"""
    title = serializers.CharField(source='product_id.title')
    old_prices = OldPricesSerializer(source="oldprices_set",many=True)
    class Meta:
        """Meta class"""
        model = Prices
        fields = ('title','price','old_prices')


class ProductsSerializer(serializers.ModelSerializer):
    """Product Serializer class"""
    prices = PricesSerializer(source='prices_set',many=True)
    class Meta:
        """Meta class"""
        model = Products
        fields = ('title','prices')


class ShopsSerializer(serializers.ModelSerializer):
    """Shops Serializer class"""
    products = PricesShopSerializer(source='prices_set',many=True)
    class Meta:
        """Meta class"""
        model = Shops
        fields = ('shop_name','products')


class CategorySerializer(serializers.ModelSerializer):
    """Category Serializer class"""
    class Meta:
        """Meta class"""
        model = Categories
        fields = ('name')



class MinMaxSerializer(serializers.ModelSerializer):
    """Max,min price Serializer class"""
    shop_name = serializers.CharField(source='shop.shop_name')
    title = serializers.CharField(source='product_id.title')
    category = serializers.CharField(source='product_id.category')
    class Meta:
        """Meta class"""
        model = Prices
        fields = ('category','title', 'price', 'shop_name')

    #def get_category_from_products(self,product):
     #   """return category of a product from products table"""
     #   return product.name.category
