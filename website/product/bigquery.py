from google.cloud import bigquery
import os

#from product import parser
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/khamitov.darkhan/PycharmProjects/choco-master/website/product/choco-302209-d68902f62cd6.json"

# Construct a BigQuery client object.
client = bigquery.Client(project="choco-302209")
table_id='chocofood_111.products'
# TODO(developer): Set table_id to the ID of table to append to.

rows_to_insert = rows_to_insert = [
    {u"shop": u"Mechta", u"category": "Iphones", "title":"Iphone 10", "price":"20000"},
]
errors = client.insert_rows_json(table_id, rows_to_insert)  # Make an API request.
if errors == []:
    print("New rows have been added.")
else:
    print("Encountered errors while inserting rows: {}".format(errors))


