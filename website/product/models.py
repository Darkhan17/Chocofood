from django.db import models



class Categories(models.Model):
    category_name = models.CharField(max_length=100)

    def getData(self):
        return Categories.objects.all()

    def __str__(self):
        return self.category_name


class Shops(models.Model):
    shop_name = models.CharField(max_length=100)

    def __str__(self):
        return self.shop_name



class Products(models.Model):
    title = models.CharField(max_length=1000)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)

    def __str__(self):
        return self.title



class Prices(models.Model):
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shops,on_delete=models.CASCADE)
    price = models.IntegerField(null=True)

    def __str__(self):
        return self.product_id.title


class OldPrices(models.Model):
    price_id = models.ForeignKey(Prices, on_delete=models.CASCADE)
    price = models.IntegerField(null=True)
    time = models.DateTimeField()

    def __str__(self):
        return self.price_id.__str__()