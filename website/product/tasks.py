from celery import shared_task
from .models import Products,Prices,Categories,OldPrices,Shops
from product.parser import parser
from google.cloud import bigquery
import os
from datetime import date
from product.ML import tenserflow

@shared_task
def create_product():
    categories = Categories.objects.all()
    database_categories = [category.category_name for category in categories]
    all_products=[]
    for category in database_categories:
        all_products.extend(parser.parse_shops(category))
    for products in all_products:
        for product in products:
            shop = product['shop']
            category = product['category']
            for item in product['items']:
                product_name = item['title']
                product_price = parser.to_int(item['price'])
                try:
                    good = Products.objects.get(title=product_name)
                except Products.DoesNotExist:
                    good_category = Categories.objects.get(category_name=category)
                    good = Products(title=product_name,category=good_category)
                    good.save()
                try:
                    new_price = Prices.objects.get(product_id = good)
                except Prices.DoesNotExist:
                    new_price = Prices(product_id=good,price=product_price)
                    new_price.shop = Shops.objects.get(shop_name=shop)
                    new_price.save()
                    data = {'shop': shop, 'category': category, 'title': product_name, 'price': product_price}
                if (new_price.price!=product_price and new_price.price!=None):
                    old = OldPrices.objects.create(price_id=new_price, price=new_price.price, time=date.today())
                    new_price.price = product_price
                new_price.save()


@shared_task
def import_to_bq():

    # from product import parser
    os.environ[
        "GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/khamitov.darkhan/PycharmProjects/choco-master/website/product/choco-302209-f3b4817ab3e5.json"

    # Construct a BigQuery client object.
    client = bigquery.Client(project="choco-302209")
    table_id = 'chocofood_111.products'
    products = Products.objects.all()
    items=[]
    for product in products:
        flag = False
        product_name = product.title
        product_category = product.category.category_name
        price_objects = Prices.objects.filter(product_id=product)

        for price_object in price_objects:
            product_price = price_object.price
            product_shop = price_object.shop.shop_name
            query = """ SELECT *, LAST_VALUE(price) OVER (ORDER BY date) 
                            FROM chocofood_111.products where title = {0}
                             and shop ={1} limit 1"""
            query_job = client.query(query.format("'" + product_name + "'","'"+product_shop+"'"))# Make an API request.
            for row in query_job:
                if (row['price']==str(product_price)):
                    flag=True
            if (flag):
                continue
            else:
                product_date = str(date.today())
                items.append({'shop':product_shop,'category':product_category,'title':product_name,
                      'price':product_price, 'date': product_date})
    if (len(items)>0):
        errors = client.insert_rows_json(table_id, items)  # Make an API request.




@shared_task
def check_on_dublicates():
    categories = Categories.objects.all()
    for x in categories:
        products = Products.objects.filter(category=x)
        for product in products:
            print([item.title for item in products])
            same_product_name = tenserflow.run(product.title, [item.title for item in products])
            print(same_product_name)
            break
            #for name in same_product_name:
            #    item = Products.objects.get(title=name)
            #    price = Prices.objects.get(product_id = item)
            #    price.product_id = product.id
            #products.exclude(title=)
