#!/usr/bin/python3
# -*-coding: utf8 -*-
from function_updating_db import insert_product_db


class DatabaseManager:
    """
        Class which manages the database.

    Attributes:
        connector : Class MysqlConnector
            The database connector.

    Methods:

        create_db()
            Create the database "purBeurre".

        erase_db()
            Delete the database "purBeurre".

        create_table()
            Create the table that compose our database.
    """

    def __init__(self, connector):
        """
        DatebaseManager class constructor.

        Parameters:
            connector : Class MysqlConnector
                The database connector.
        """
        self.connector = connector

    def create_db(self):
        """Create the database "purBeurre".

        Execute the SQL request which allows to create the database.
        """
        req = "CREATE DATABASE purBeurre"
        self.connector.execute(req)

    def erase_db(self):
        """Delete the database "purBeurre".

        Execute the SQL request which allows you to delete the database.
        """
        req = "DROP DATABASE purBeurre"
        self.connector.execute(req)

    def create_table(self):
        """Create the table that compose our database.

        Execute the SQL requests which will create all the tables that the
         database needs.
        """
        req = """
        CREATE TABLE Categories (
            id INT UNSIGNED NOT NULL AUTO_INCREMENT,
            name_cat VARCHAR(255) NOT NULL,
            PRIMARY KEY (id)
            )
            ENGINE=InnoDB DEFAULT CHARSET=utf8;
        CREATE TABLE Store (
            id INT UNSIGNED NOT NULL AUTO_INCREMENT,
            name_store VARCHAR(255) NOT NULL,
            PRIMARY KEY (id)
            )
            ENGINE=InnoDB DEFAULT CHARSET=utf8;
        CREATE TABLE Product (
            id INT UNSIGNED NOT NULL AUTO_INCREMENT,
            name_product VARCHAR(255) NOT NULL,
            brand VARCHAR(255),
            category TEXT,
            nutri_score VARCHAR(2),
            store TEXT,
            ingredient TEXT,
            url TEXT,
            PRIMARY KEY (id)
            )
            ENGINE=InnoDB DEFAULT CHARSET=utf8;
        CREATE TABLE ProductCategory (
            id_product INT UNSIGNED NOT NULL,
            id_product_cat INT UNSIGNED NOT NULL
            )
            ENGINE=InnoDB DEFAULT CHARSET=utf8;
        CREATE TABLE Substitute (
            id_product INT UNSIGNED NOT NULL,
            id_product_substitute INT UNSIGNED NOT NULL
            )
            ENGINE=InnoDB DEFAULT CHARSET=utf8;
        CREATE TABLE ProductStore (
            id_product INT UNSIGNED NOT NULL,
            id_product_store INT UNSIGNED NOT NULL
            )
            ENGINE=InnoDB DEFAULT CHARSET=utf8;
        ALTER TABLE ProductCategory ADD CONSTRAINT fk_idproduct
        FOREIGN KEY (id_product) REFERENCES Product(id);
        ALTER TABLE ProductCategory ADD CONSTRAINT fk_id_product_cat
        FOREIGN KEY (id_product_cat) REFERENCES Categories(id);
        ALTER TABLE Substitute ADD CONSTRAINT fk_id_product
        FOREIGN KEY (id_product) REFERENCES Product(id);
        ALTER TABLE Substitute ADD CONSTRAINT fk_id_product_substitute
        FOREIGN KEY (id_product_substitute) REFERENCES Product(id);
        ALTER TABLE ProductStore ADD CONSTRAINT fk_idproduct
        FOREIGN KEY (id_product) REFERENCES Product(id);
        ALTER TABLE ProductStore ADD CONSTRAINT fk_id_product_store
        FOREIGN KEY (id_product_store) REFERENCES Store(id);"""
        self.connector.execute(req, multi=1)


class CategoryManager:
    """
    Class which manages the Categories table of the database.

    Attributes:
        connector : Class MysqlConnector
            The database connector.

    Methods:

        delete(id_delete)
            Delete a category from the table.

        insert(category)
            Insert a category into the table.

        update(category)
            Updates a category of the table.

        select()
            Get all the categories of the table in a list and
             return this list.

        get()
            Get a category from the table and returns it.
    """

    def __init__(self, connector):
        """
        CategoryManager class constructor.

        Parameters:
            connector : Class MysqlConnector
                The database connector.
        """
        self.connector = connector

    def delete(self, id_delete):
        """
        Delete a category from the table.

        Execute the SQL request which allows you to delete a category
         from the table.

        Parameters:
            id_delete: int
                The ID number of the category we want to delete
                 from the table.
        """
        req = "DELETE FROM Categories WHERE id = %s"
        self.connector.execute(req, (id_delete,))

    def insert(self, category):
        """
        Insert a category into the table.

        Execute the SQL request which allows to insert a category
         in the table.

        Parameters:
            category: dict
                The category we want to insert in the table.
        """
        req = "INSERT INTO Categories (name_cat) VALUES (%s)"
        id_ = self.connector.execute(req, (category["name"],))
        category["id"] = id_

    def update(self, category):
        """
        Updates a category of the table.

        Execute the SQL request which allows updating a category in the table.

        Parameters:
            category: dict
                The category we want to update in the table.
        """
        infos = (category["name"], category["id"])
        req = "UPDATE Categories SET name_cat= %s WHERE id = %s"
        self.connector.execute(req, infos)

    def select(self, name=None):
        """
        Get all the categories of the table in a list and
         return this list.

        Execute the SQL request which retrieves all the categories from
         the table, transforms each category into a dictionary comprising
         the ID and the name, and returns a list of all these categories.

        Returns:
            list
                A list of all the categories of the table.
        """
        if name is None:
            req = "SELECT * FROM Categories"
            response = self.connector.select(req)
            list_cat = []
            for cat in response:
                category = {"id": cat[0], "name": cat[1]}
                list_cat.append(category)
            return list_cat
        if name is not None:
            try:
                req = "SELECT id, name_cat FROM Categories " \
                      "WHERE name_cat=%s;"
                response = self.connector.select(req, (name,))
                category = {"id": response[0][0], "name": response[0][1]}
                return category
            except IndexError:
                return None

    def get(self, id_cat):
        """
        Get a category from the table and returns it.

        Execute the SQL query which retrieves the desired category,
         transforms it into a dictionary comprising an ID and a name,
         and returns this category.

        Parameters:
            id_cat : int
                The ID number of the category we want to get from the table.

        Returns:
             dict
                A dictionary that represents a category with the Id
                 and the name.
        """
        req = "SELECT name_cat FROM Categories WHERE id = %s"
        response = self.connector.select(req, (id_cat,))
        category = {"id": id_cat, "name": response[0][0]}
        return category


class StoreManager:
    """
    Class which manages the Store table of the database.

    Attributes:
       connector : Class MysqlConnector
           The database connector.

    Methods:

       delete(id_delete)
           Delete a store from the table.

       insert(store)
           Insert a store into the table.

       update(store)
           Updates a store of the table.

       select()
           Get all the stores of the table in a list and
            return this list.

       get()
           Get a store from the table and returns it.
    """

    def __init__(self, connector):
        """
        StoreManager class constructor.

        Parameters:
            connector : Class MysqlConnector
                The database connector.
        """
        self.connector = connector

    def delete(self, id_delete):
        """
        Delete a store from the table.

        Execute the SQL request which allows you to delete a store
         from the table.

        Parameters:
            id_delete: int
                The ID number of the store we want to delete
                 from the table.
        """
        req = "DELETE FROM Store WHERE id = %s"
        self.connector.execute(req, (id_delete,))

    def insert(self, store):
        """
        Insert a store into the table.

        Execute the SQL request which allows to insert a store
         in the table.

        Parameters:
            store: dict
                The store we want to insert in the table.
        """
        req = "INSERT INTO Store (name_store) VALUES (%s)"
        id_ = self.connector.execute(req, (store["name"],))
        store['id'] = id_

    def update(self, store):
        """
        Updates a store of the table.

        Execute the SQL request which allows updating a store in the table.

        Parameters:
            store: dict
                The store we want to update in the table.
        """
        infos = (store["name"], store["id"])
        req = "UPDATE Store SET name_cat= %s WHERE id = %s"
        self.connector.execute(req, infos)

    def select(self, name=None):
        """
        Get all the stores of the table in a list and
         return this list.

        Execute the SQL request which retrieves all the stores from
         the table, transforms each store into a dictionary comprising
         the ID and the name, and returns a list of all these stores.

        Returns:
            list
                A list of all the stores of the table.
        """
        if name is None:
            req = "SELECT * FROM Store"
            response = self.connector.select(req)
            list_store = []
            for store in response:
                sto = {"id": store[0], "name": store[1]}
                list_store.append(sto)
            return list_store

        if name is not None:
            try:
                req = "SELECT id, name_store FROM Store " \
                      "WHERE name_store=%s;"
                response = self.connector.select(req, (name,))
                store = {"id": response[0][0], "name": response[0][1]}
                return store
            except IndexError:
                return None

    def get(self, id_store):
        """
        Get a store from the table and returns it.

        Execute the SQL query which retrieves the desired store,
         transforms it into a dictionary comprising the ID and the name,
         and returns this store.

        Parameters:
            id_store : int
                The ID number of the store we want to get from the table.

        Returns:
             dict
                A dictionary that represents a store with the Id and the name.
        """
        req = "SELECT name_store FROM Store WHERE id = %s"
        response = self.connector.select(req, (id_store,))
        store = {"id": id_store, "name": response[0][0]}
        return store


class ProductManager:
    """
    Class which manages the Product table of the database.

    Attributes:
       connector : Class MysqlConnector
           The database connector.

    Methods:

       delete(id_delete)
           Delete a product from the table.

       insert(product)
           Insert a product into the table.

       update(product)
           Updates a product of the table.

       select()
           Get all the products of the table in a list and
            return this list.

       get()
           Get a product from the table and returns it.
    """

    def __init__(self, connector):
        """
        ProductManager class constructor.

        Parameters:
           connector : Class MysqlConnector
               The database connector.
        """
        self.connector = connector

    def delete(self, id_delete):
        """
        Delete a product from the table.

        Execute the SQL request which allows you to delete a product
         from the table.

        Parameters:
            id_delete: int
                The ID number of the product we want to delete
                 from the table.
        """
        req = "DELETE FROM Product WHERE id = %s"
        self.connector.execute(req, (id_delete,))

    def insert(self, pcm, psm, product=None, list_prod=None):
        """
        Insert a product into the table.

        Execute the SQL request which allows to insert a product
         in the table.

        Parameters:
            product: dict
                The product we want to insert in the table.
        """
        if product is not None:
            check = self.select(pcm, psm, name=product["name"])
            if check is None:
                req = "INSERT INTO Product " \
                      "(name_product, brand, nutri_score, " \
                      "ingredient, url) VALUES (%s, %s, %s, %s, %s)"
                id_ = self.connector.execute(req, (product["name"],
                                                   product["brand"],
                                                   product["nutriscore"],
                                                   product["ingredients"],
                                                   product["url"]))
                product["id"] = id_
                return product
            else:
                print("Ce produit existe déjà dans la base de donnée.")
                print("Produit n°{}, nom: {}".format(check["id"], check["name"]))
                return check
        if list_prod is not None:
            for product in list_prod:
                check = self.select(pcm, psm, name=product["name"])
                if check is None:
                    req = "INSERT INTO Product " \
                          "(name_product, brand, category, nutri_score, " \
                          "store, ingredient, url) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    id_ = self.connector.execute(req, (product["name"],
                                                       product["brand"],
                                                       product["category"],
                                                       product["nutri_score"],
                                                       product["store"],
                                                       product["ingredients"],
                                                       product["url"]))
                    product["id"] = id_
                    return product
                else:
                    print("Ce produit existe déjà dans la base de donnée.")
                    print("Produit n°{}, nom: {}".format(check["id"], check["name"]))
                    return check

    def update(self, product):
        """
        Updates a product of the table.

        Execute the SQL request which allows updating a product in the table.

        Parameters:
            product: dict
                The product we want to update in the table.
        """
        req = "UPDATE Product SET name_product=%s, brand=%s, category=%s, " \
              "nutri_score=%s, store=%s, ingredient=%s, url=%s" \
              "WHERE id=%s"
        self.connector.execute(req, (product["name"],
                                     product["brand"],
                                     product["category"],
                                     product["nutri_score"],
                                     product["store"],
                                     product["ingredient"],
                                     product["url"],
                                     product["id"]))

    def select(self, pcm, psm, name=None):
        """
        Get all the products of the table in a list and
        return this list.

        Execute the SQL request which retrieves all the products from
         the table, transforms each product into a dictionary comprising
         the ID, the name, the brand, the categories, the nutri-score,
         the stores and the ingredients.
         And returns a list of all these products.

        Returns:
            list
                A list of all the products of the table.
       """
        if name is None:
            req = "SELECT * FROM Product"
            select = self.connector.select(req)
            list_product = []
            for product in select:
                product_return = {"id": product[0],
                                  "name": product[1],
                                  "brand": product[2],
                                  "nutriscore": product[4],
                                  "ingredient": product[6],
                                  "url": product[7]}
                product_return["category"] = pcm.select_association_with_id_prod(product_return["id"])
                product_return["store"] = psm.select_association(product_return["id"])
                list_product.append(product_return)
            return list_product
        if name is not None:
            try:
                req = "SELECT id, name_product, brand, category, " \
                      "nutri_score, store, ingredient, url " \
                      "FROM Product " \
                      "WHERE name_product=%s;"
                response = self.connector.select(req, (name,))
                product = {"id": response[0][0],
                           "name": response[0][1],
                           "brand": response[0][2],
                           "nutriscore": response[0][4],
                           "ingredient": response[0][6],
                           "url": response[0][7]}
                product["category"] = pcm.select_association_with_id_prod(product["id"])
                product["store"] = psm.select_association(product["id"])
                return product
            except IndexError:
                return None

    def get(self, id_product):
        """
        Get a product from the table and returns it.

        Execute the SQL query which retrieves the desired product,
         transforms it into a dictionary comprising the ID, the name,
         the brand, the categories, the nutri-score, the stores and the
         ingredients. And returns this product.

        Parameters:
            id_product : int
                The ID number of the product we want to get from the table.

        Returns:
             dict
                A dictionary that represents a product with the Id and the
                 name.
        """
        req = "SELECT name_product, brand, category, nutri_score, store, " \
              "ingredient, url FROM Product " \
              "WHERE Product.id = %s"
        select = self.connector.select(req, (id_product,))
        product = {"id": id_product,
                   "name": select[0][0],
                   "brand": select[0][1],
                   "category": select[0][2],
                   "nutriscore": select[0][3],
                   "store": select[0][4],
                   "ingredient": select[0][5],
                   "url": select[0][6]}
        return product


class ProductCategoryManager:
    """
    Class which manages the ProductCategory table of the database.

    Attributes:
       connector : Class MysqlConnector
           The database connector.

    Methods:

        insert_association(id_cat, id_product)
            Insert the association of a product with a category.

        select_association(id_product)
            Get the association of a product with a category.
    """
    def __init__(self, connector):
        """
        ProductCategoryManager class constructor.

        Parameters:
          connector : Class MysqlConnector
              The database connector.
        """
        self.connector = connector

    def insert_association(self, id_cat, id_product):
        """
        Insert an association of a product with a category into the table.

        Execute the SQL request which allows to insert an association of
         a product with a category in the table.

        Parameters:
            id_cat : int
                The ID number of the category we want to insert into
                 the table.

            id_product : int
                The ID number of the product we want to insert into
                 the table.
        """
        req = "INSERT INTO ProductCategory (id_product, id_product_cat)" \
              "VALUES (%s, %s)"
        self.connector.execute(req, (id_product, id_cat))

    def select_association_with_id_prod(self, id_product):
        """
        Get the associations of a product with its categories and return them.

        Execute the SQL request which retrieves the associations of a product
         with its categories. And returns a list of its associations.

        Returns:
            list
                A list of the associations of a product with its categories.
        """
        req = "SELECT Categories.name_cat  " \
              "FROM Product " \
              "INNER JOIN ProductCategory " \
              "ON ProductCategory.id_product = Product.id " \
              "INNER JOIN Categories " \
              "ON Categories.id = ProductCategory.id_product_cat  " \
              "WHERE Product.id = %s"
        response = self.connector.select(req, (id_product,))
        list_cat = []
        for cat in response:
            list_cat.append(cat[0])
        return list_cat

    def select_association_with_cat(self, category_name):
        req = "SELECT Product.id,Product.name_product,Product.nutri_score " \
              "FROM Product " \
              "INNER JOIN ProductCategory " \
              "ON ProductCategory.id_product = Product.id " \
              "INNER JOIN Categories " \
              "ON Categories.id = ProductCategory.id_product_cat " \
              "WHERE Categories.name_cat = %s"

        response = self.connector.select(req, (category_name,))
        list_prod = []
        for prod in response:
            product = {"id": prod[0], "name": prod[1], "nutriscore": prod[2]}
            list_prod.append(product)
        return list_prod


class ProductStoreManager:
    """
    Class which manages the ProductStore table of the database.

    Attributes:
       connector : Class MysqlConnector
           The database connector.

    Methods:

        insert_association(id_cat, id_product)
            Insert the association of a product with a category.

        select_association(id_product)
            Get the association of a product with a category.
    """
    def __init__(self, connector):
        """
        ProductStoreManager class constructor.

        Parameters:
          connector : Class MysqlConnector
              The database connector.
        """
        self.connector = connector

    def insert_association(self, id_store, id_product):
        """
        Insert an association of a product with a store into the table.

        Execute the SQL request which allows to insert an association of
         a product with a store in the table.

        Parameters:
            id_store : int
                The ID number of the store we want to insert into
                 the table.

            id_product : int
                The ID number of the product we want to insert into
                 the table.
        """
        req = "INSERT INTO ProductStore (id_product, id_product_store)" \
              "VALUES (%s, %s)"
        self.connector.execute(req, (id_product, id_store))

    def select_association(self, id_product):
        """
        Get the associations of a product with its stores and return them.

        Execute the SQL request which retrieves the associations of a product
         with its stores. And returns a list of its associations.

        Returns:
            list
                A list of the associations of a product with its stores.
        """
        req = "SELECT Store.name_store  " \
              "FROM Product " \
              "INNER JOIN ProductStore " \
              "ON ProductStore.id_product = Product.id " \
              "INNER JOIN Store " \
              "ON Store.id = ProductStore.id_product_store  " \
              "WHERE Product.id = %s"
        response = self.connector.select(req, (id_product,))
        list_store = []
        for store in response:
            list_store.append(store[0])
        return list_store


class SubstituteManager:
    """
        Class which manages the Substitute table of the database.

        Attributes:
           connector : Class MysqlConnector
               The database connector.

        Methods:

            insert_association(id_sub, id_product)
                Insert the association of a product with a substitute.

            select_association(id_product)
                Get the association of a product with a substitute.
        """

    def __init__(self, connector):
        """
        SubstituteManager class constructor.

        Parameters:
          connector : Class MysqlConnector
              The database connector.
        """
        self.connector = connector

    def insert_association(self, id_product, id_sub):
        """
        Insert an association of a product with a substitute into the table.

        Execute the SQL request which allows to insert an association of
         a product with a substitute in the table.

        Parameters:
            id_product : int
                The ID number of the product we want to insert into
                 the table.

            id_sub : int
                The ID number of the substitute we want to insert into
                 the table.
        """
        req = "INSERT INTO Substitute (id_product, id_product_substitute)" \
              "VALUES (%s, %s)"
        self.connector.execute(req, (id_product, id_sub))

    def select_association(self, id_product, psm, pcm, pm):
        """
        Get the associations of a product with its substitute and return them.

        Execute the SQL request which retrieves the associations of a product
         with its substitutes. And returns a list of its associations.

        Returns:
            list
                A list of the associations of a product with its substitutes.
        """
        req = "SELECT Product.id, Product.name_product, Product.nutri_score, Product.url  " \
              "FROM Product " \
              "INNER JOIN Substitute " \
              "ON Product.id = Substitute.id_product_substitute " \
              "WHERE Substitute.id_product=%s"
        response = self.connector.select(req, (id_product,))
        list_sub = []
        for sub in response:
            substitute = {"id": sub[0], "name": sub[1], "nutriscore": sub[2], "url": sub[3]}
            substitute["store"] = psm.select_association(substitute["id"])
            substitute["category"] = pcm.select_association_with_id_prod(substitute["id"])
            list_sub.append(substitute)
        return list_sub

    def select_substituted_product(self):
        req = "SELECT id_product, Product.name_product " \
              "FROM Substitute " \
              "INNER JOIN Product ON Product.id=Substitute.id_product"
        response = self.connector.select(req)
        list_prod = []
        for prod in response:
            product = {"id": prod[0], "name": prod[1]}
            list_prod.append(product)
        return list_prod

    def associate_substitute_to_product(self, pm, cm, sm, pcm, psm, api, product):
        """
        Associate a substitue to a product in the database.

        Get a list of all the database products.
        Get a list of all the product categories.
        Retrieves the products having one of the categories of the product
         in parameter.
        If the list contains products, check if their nutriscore is lower than
         that of the product in parameter.
        If it's lower, associate the product as a substitute for the product
         that we have put in parameter and return True.
        If the list is empty returns False.

        Parameters:
            pm : class ProductManager
                The manager of the Product table in the database.
            pcm : class ProductCategoryManager
                The manager of the ProductCategory table in the database.
            subm : class SubstituteManager
                The manager of the Substitute table in the database.
            product : dict
                The product to whiwh we want to associate a store.

        Returns:
            boolean
                True if there is a list of substitutes and false if the list of
                 substitutes is empty.
        """
        list_product_bdd = pm.select(pcm, psm)
        list_cat_product = pcm.select_association_with_id_prod(product["id"])
        list_substitute_possible = []

        for prod in list_product_bdd:
            prod["category"] = pcm.select_association_with_id_prod(prod["id"])
            match = False
            for cat in prod["category"]:
                if cat in list_cat_product:
                    if prod["nutriscore"] < product["nutriscore"]:
                        match = True
            if match:
                list_substitute_possible.append(prod)
        if list_substitute_possible:
            return list_substitute_possible
        if not list_substitute_possible:
            research = api.search_product(product["name"])
            match = False
            for prod in research:
                pdt = None
                if prod["nutriscore"] < product["nutriscore"]:
                    match = True
                    pdt = insert_product_db(pm, cm, sm, pcm, psm, prod)
                if match:
                    list_substitute_possible.append(pdt)
            return list_substitute_possible
