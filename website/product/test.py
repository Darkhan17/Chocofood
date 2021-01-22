from google.cloud import bigquery
import os

# from product import parser
os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/khamitov.darkhan/PycharmProjects/choco-master/website/product/choco-302209-f3b4817ab3e5.json"

# Construct a BigQuery client object.
client = bigquery.Client(project="choco-302209")
table_id = 'chocofood_111.products'

query = """ SELECT *, LAST_VALUE(price) OVER (ORDER BY date) 
                           FROM chocofood_111.products where title = {0}
                            and shop ={1} limit 1"""
product_name = 'Iphone 10'
product_shop = 'Sulpak'
query_job = client.query(
            query.format("'" + product_name + "'", "'" + product_shop + "'"))  # Make an API request.


for row in query_job:
    print(type(row['price']))