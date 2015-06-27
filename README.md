Simple catalog CRUD app with Flask 
=============
### About
1. This is a simple Flask based web application that allows CRUD application on a catalog. The catalog contains multiple categories and each category can have multiple products associated with it. 
2. Users can browse various categories and products and read tru the product details (Item name, description, price).
3. Authentication: Add, Edit and delete operations can only be performed by users who are looged into the system using. Users can autenticate themselves via two oauth  - google or facebook. 
4. Autherization: After logining in, only users who are seup as category owners can add,edit or delete product items from their categories.
5. The application also has two JSON endpoints that return data in JSON format   (a) JSON endpoint for all categories in the catalog :localhost:5000/catalog/categories/JSON  (b) JSON endpoint for all products within a category : localhost:5000/catalog/<int:category_id>/products/JSON

### Steps to run this application: 

1. Download or clone the `vagrant` directory.
2. Initialize the Vagrant vm via `vagrant up`.
3. Connect to the virtual machine: `vagrant ssh`.
4. Obtain your own Google or FB API keys by registering a new application
5. Update config file with required Client id and secret.
6. (optional) For sample data setup, navigate to /vagrant/catalog/catalogapp/models directory and run `python db_sampledata.py`. This creates 3 sports categories with a couple of items each in catalog.db
7. Navigate to the catalog directory: `cd /vagrant/catalog`
8. Start the server: `python run.py`. [Note: you can run this in debug mode by '`python run.py --debug`
9. Navigate to it in your browser  at `localhost:5000`.  
10. Browse, Add, Edit or Delete items in catalog

