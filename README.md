This project is designed to compare prices in different stores (Sulpak, Technodom, Mechta, White Wind). It collects data from store sites every hour, and updates in case of changes. All collected data is saved, if desired, you can create a price change schedule.

#tracker

The whole project consists of one application - tracker.

#Data base

The Category model describes product categories and consists of only one name field (CharField).
Products are described by the Product model. Its fields are name (CharField), category (ForeignKey (Category)).
Stores are described by the Shop model, and consist of fields: name (CharField), url (URLField). Prices are listed in a separate table, which consists of the following fields: cost (IntegerField), date (DateTimeField), product (ForeiignKey (product)), shop (ForeignKey (shop)). For each store, a separate proxy model is created, because each store has its own way of collecting data, and at the same time we store them all in one table, it also makes it easier to add new stores to collect data. To make it even easier, there is a Url model with fields: url (URLField), shop (ForeignKey (Shop)), category (ForeignKey (Category)). This is done to simplify adding stores thanks to StackedInline, it also makes it easier to expand the list of pages to collect data from existing pages. (This also makes it easier to add a product manually, if such a need arises, you can immediately specify all prices from all stores in base)

#How does it work?

First you need to add a store from which the data will be downloaded. Let's create a porxy model that will inherit from Shop for the store and describe the way to collect data in the get_data () method. Having made the migration, we create a new store using the admin panel, add all the links and categories that they display there. It remains to add our new model to the shops list, which is found inside tasks.py update_data () of our tracker application. That's it, now the project using celery will collect new data from the links that you added along with your store. update_data () will run through all store models and run the get_data () method, it will collect all the data and call the super () method. update_data () from the super class Shop, which, in turn, will check if the price has changed and will add a new price if she has changed after all. To get the result, go to the link http: // localhost: 8000 / api / products /, you will see json with all the products. To see the value of a particular product, add its id /.

#How to start?

From the project root run

docker-compose build

Now you can run the project

docker-compose up
