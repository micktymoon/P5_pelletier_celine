#!/usr/bin/python3
# -*-coding: utf8 -*-

import mysql.connector.errors
from database.function_updating_db import insert_product_db


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
        DatabaseManager class constructor.

        Parameters:
            connector : Class MysqlConnector
                The database connector.
        """
        self.connector = connector

    def create_db(self):
        """
        Create the database "purBeurre".

        Execute the SQL request which allows to create the database.
        """
        req = "CREATE DATABASE purBeurre"
        self.connector.execute(req)

    def erase_db(self):
        """
        Delete the database "purBeurre".

        Execute the SQL request which allows you to delete the database.
        """
        req = "DROP DATABASE purBeurre"
        self.connector.execute(req)

    def create_table(self):
        """
        Create the table that compose our database.

        Execute the SQL requests which will create all the tables that the
         database needs.
        """
        req = """
        CREATE TABLE Category (
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
            nutri_score VARCHAR(2),
            ingredient TEXT,
            url TEXT,
            PRIMARY KEY (id)
            )
            ENGINE=InnoDB DEFAULT CHARSET=utf8;
        CREATE TABLE ProductCategory (
            id_product INT UNSIGNED NOT NULL,
            id_product_cat INT UNSIGNED NOT NULL,
            PRIMARY KEY (id_product, id_product_cat),
            FOREIGN KEY (id_product) REFERENCES Product(id),
            FOREIGN KEY (id_product_cat) REFERENCES Category(id)
            )
            ENGINE=InnoDB DEFAULT CHARSET=utf8;
        CREATE TABLE Substitute (
            id_product INT UNSIGNED NOT NULL,
            id_product_substitute INT UNSIGNED NOT NULL,
            PRIMARY KEY (id_product, id_product_substitute),
            FOREIGN KEY (id_product) REFERENCES Product(id),
            FOREIGN KEY (id_product_substitute) REFERENCES Product(id)
            )
            ENGINE=InnoDB DEFAULT CHARSET=utf8;
        CREATE TABLE ProductStore (
            id_product INT UNSIGNED NOT NULL,
            id_product_store INT UNSIGNED NOT NULL,
            PRIMARY KEY (id_product, id_product_store),
            FOREIGN KEY (id_product) REFERENCES Product(id),
            FOREIGN KEY (id_product_store) REFERENCES Store(id)
            )
            ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
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

        select(name)
            Get all the categories from the table, or just a given category,
             and return them.

        get(id_cat)
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
        req = "DELETE FROM Category WHERE id = %s"
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
        req = "INSERT INTO Category (name_cat) VALUES (%s)"
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
        req = "UPDATE Category SET name_cat= %s WHERE id = %s"
        self.connector.execute(req, infos)

    def select(self, name=None):
        """
        Get all the categories from the table, or just a given category,
         and return them.

        If there is no category given in the "name" parameter:
        Execute the SQL query which retrieves all the categories from
         the table, transforms each category into a dictionary comprising
         the ID and the name, and returns a list of all these categories.
        If there is a category given in the "name" parameter:
        Execute the SQL query which retrieves the category, given as a
         parameter, of the table, transforms it into a dictionary comprising
         an ID and a name, and returns it.

        Parameters:
            name: str
                The name of the category we want to retrieve.

        Returns:
            If name is None: list
                A list of all the categories of the table.
            If name is not None: dict
                The category that we put in parameter.
        """
        if name is None:
            req = "SELECT * FROM Category"
            response = self.connector.select(req)
            list_cat = []
            for cat in response:
                category = {"id": cat[0], "name": cat[1]}
                list_cat.append(category)
            return list_cat
        if name is not None:
            try:
                req = "SELECT id, name_cat FROM Category " \
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
        req = "SELECT name_cat FROM Category WHERE id = %s"
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

       select(name)
           Get all the stores of the table in a list and
            return this list.

       get(id_store)
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
        Get all the stores from the table, or just a given store,
         and return them.

        If there is no store given in the "name" parameter:
        Execute the SQL query which retrieves all the stores from
         the table, transforms each store into a dictionary comprising
         the ID and the name, and returns a list of all these stores.
        If there is a store given in the "name" parameter:
        Execute the SQL query which retrieves the store, given as a
         parameter, of the table, transforms it into a dictionary comprising
         an ID and a name, and returns it.

        Parameters:
            name: str
                The name of the store we want to retrieve.

        Returns:
            If name is None: list
                A list of all the stores of the table or just the given store.
            If name is not None: dict
                The store that we set as a parameter.

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

       insert(pcm, psm, product, list_prod)
           Insert a product into the table.

       update(product)
           Updates a product of the table.

       select(name)
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
        Insert a product or a product list into the table.

        If there is a product indicated in the "product" parameter:
        Executes the SQL query which inserts the product, given as a
         parameter, into the table. Assigns an ID and returns it.
        If there is a product list indicated in the "list_prod" parameter:
        Execute the SQL query which inserts a product in the table, for each
         product of the list given in parameter.
        Assigns them an ID and returns them.

        Parameters:
            pcm : class ProductCategoryManager
                The manager of the ProductCategory table in the database.

            psm : class ProductStoreManager
                The manager of the ProductStore table in the database.

            product: dict
                The product we want to insert into the table.

            list_prod: list
                The list of products that we want to insert into the table.

        Returns:
            dict
                The product that we have inserted in the table.
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
                print("Produit n°{}, nom: {}".format(check["id"],
                                                     check["name"]))
                return check
        if list_prod is not None:
            for product in list_prod:
                check = self.select(pcm, psm, name=product["name"])
                if check is None:
                    req = "INSERT INTO Product " \
                          "(name_product, brand, nutri_score, ingredient," \
                          " url) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    id_ = self.connector.execute(req, (product["name"],
                                                       product["brand"],
                                                       product["nutri_score"],
                                                       product["ingredients"],
                                                       product["url"]))
                    product["id"] = id_
                    return product
                else:
                    print("Ce produit existe déjà dans la base de donnée.")
                    print("Produit n°{}, nom: {}".format(check["id"],
                                                         check["name"]))
                    return check

    def update(self, product):
        """
        Updates a product of the table.

        Execute the SQL request which allows updating a product in the table.

        Parameters:
            product: dict
                The product we want to update in the table.
        """
        req = "UPDATE Product SET name_product=%s, brand=%s, " \
              "nutri_score=%s, ingredient=%s, url=%s" \
              "WHERE id=%s"
        self.connector.execute(req, (product["name"],
                                     product["brand"],
                                     product["nutri_score"],
                                     product["ingredient"],
                                     product["url"],
                                     product["id"]))

    def select(self, pcm, psm, name=None):
        """
        Get all the products, or just a product given as a parameter,
         of the table in a list and return them.

        If name is None:
        Execute the SQL request which retrieves all the products from
         the table, transforms each product into a dictionary comprising
         the ID, the name, the brand, the categories, the nutri-score,
         the stores and the ingredients.
         And returns a list of all these products.
        If name is not None:
        Execute the SQL request which retrieves the products given in
         parameter from the table, transforms this product into a dictionary
         comprising the ID, the name, the brand, the categories,
         the nutri-score, the stores and the ingredients.
        And returns it.

        Parameters:
            pcm : class ProductCategoryManager
                The manager of the ProductCategory table in the database.

            psm : class ProductStoreManager
                The manager of the ProductStore table in the database.

            name : str
                The name of the product that we want to recover.

        Returns:
            If name ise None :list
                A list of all the products of the table.
            If name is not None: dict
                The product that we put in parameter.
       """
        if name is None:
            req = "SELECT * FROM Product"
            select = self.connector.select(req)
            list_product = []
            for product in select:
                product_return = {"id": product[0],
                                  "name": product[1],
                                  "brand": product[2],
                                  "nutriscore": product[3],
                                  "ingredient": product[4],
                                  "url": product[5]}
                product_return["category"] = \
                    pcm.select_asso_with_id_prod(product_return["id"])
                product_return["store"] = \
                    psm.select_association(product_return["id"])
                list_product.append(product_return)
            return list_product
        if name is not None:
            try:
                req = "SELECT id, name_product, brand, " \
                      "nutri_score, ingredient, url " \
                      "FROM Product " \
                      "WHERE name_product=%s;"
                response = self.connector.select(req, (name,))
                prdct = {"id": response[0][0],
                         "name": response[0][1],
                         "brand": response[0][2],
                         "nutriscore": response[0][3],
                         "ingredient": response[0][4],
                         "url": response[0][5]}
                prdct["category"] = pcm.select_asso_with_id_prod(prdct["id"])
                prdct["store"] = psm.select_association(prdct["id"])
                return prdct
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
                A dictionary that represents a product.
        """
        req = "SELECT name_product, brand, nutri_score, " \
              "ingredient, url FROM Product " \
              "WHERE Product.id = %s"
        select = self.connector.select(req, (id_product,))
        product = {"id": id_product,
                   "name": select[0][0],
                   "brand": select[0][1],
                   "nutriscore": select[0][2],
                   "ingredient": select[0][3],
                   "url": select[0][4]}
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

        select_association_with_id_prod(id_product)
            Get the association of a product with categories.

        select_association_whit_cat(category_name)
            Get the association of a category to products.
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
        try:
            req = "INSERT INTO ProductCategory (id_product, id_product_cat)" \
                  "VALUES (%s, %s)"
            self.connector.execute(req, (id_product, id_cat))
        except mysql.connector.Error:
            print("Cette catégorie est déjà associée à ce produit.")
            pass

    def select_asso_with_id_prod(self, id_product):
        """
        Get the associations of a product with its categories and return them.

        Execute the SQL request which retrieves the associations of a product
         with its categories. And returns a list of its associations.

        Returns:
            list
               A list of categories associated with the product.
        """
        req = "SELECT Category.name_cat  " \
              "FROM Product " \
              "INNER JOIN ProductCategory " \
              "ON ProductCategory.id_product = Product.id " \
              "INNER JOIN Category " \
              "ON Category.id = ProductCategory.id_product_cat  " \
              "WHERE Product.id = %s"
        response = self.connector.select(req, (id_product,))
        list_cat = []
        for cat in response:
            list_cat.append(cat[0])
        return list_cat

    def select_asso_with_cat(self, category_name):
        """
        Get the association of a category to products.

        Execute the SQL query which retrieves the products associated with
         the given category. And returns a list of these products.

        Parameters:
            category_name: str
                The name of the category from which we want to retrieve
                 the products associated with it.

        Returns:
            list
                The list of products associated with the given category.
        """
        req = "SELECT Product.id,Product.name_product,Product.nutri_score " \
              "FROM Product " \
              "INNER JOIN ProductCategory " \
              "ON ProductCategory.id_product = Product.id " \
              "INNER JOIN Category " \
              "ON Category.id = ProductCategory.id_product_cat " \
              "WHERE Category.name_cat = %s"

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
        insert_association(id_store, id_product)
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
        try:
            req = "INSERT INTO ProductStore (id_product, id_product_store)" \
                  "VALUES (%s, %s)"
            self.connector.execute(req, (id_product, id_store))
        except mysql.connector.Error:
            print("Ce magasin est déjà associé à ce produit.")
            pass

    def select_association(self, id_product):
        """
        Get the associations of a product with its stores and return them.

        Execute the SQL request which retrieves the associations of a product
         with its stores. And returns a list of its associations.

        Parameters:
            id_product : int
                The ID of the product whose stores we want to retrieve.

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

        select_association(id_product, psm, pcm)
            Get the association of a product with a substitute.

        select_substituted_product()

        associate_substitute_to_product(pm, cm, sm, pcm, psm, api, product)
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
        try:
            req = "INSERT INTO Substitute (id_product, id_product_substitute)" \
                  "VALUES (%s, %s)"
            self.connector.execute(req, (id_product, id_sub))
        except mysql.connector.Error:
            print("Ce substitut est déjà enregistré.")
            pass

    def select_association(self, id_product, pcm, psm):
        """
        Get the associations of a product with its substitute and return them.

        Execute the SQL request which retrieves the associations of a product
         with its substitutes. And returns a list of its associations.

        Parameters:
            id_product: int
                The ID number of the product which we want to recover
                 its substitutes.

            pcm : class ProductCategoryManager
                The manager of the ProductCategory table in the database.

            psm : class ProductStoreManager
                The manager of the ProductStore table in the database.

        Returns:
            list
                The list of substitutes for the product.
        """
        req = "SELECT Product.id, Product.name_product, " \
              "Product.nutri_score, Product.url  " \
              "FROM Product " \
              "INNER JOIN Substitute " \
              "ON Product.id = Substitute.id_product_substitute " \
              "WHERE Substitute.id_product=%s"
        response = self.connector.select(req, (id_product,))
        list_sub = []
        for sub in response:
            substi = {"id": sub[0],
                      "name": sub[1],
                      "nutriscore": sub[2],
                      "url": sub[3]}
            substi["store"] = psm.select_association(substi["id"])
            substi["category"] = pcm.select_asso_with_id_prod(substi["id"])
            list_sub.append(substi)
        return list_sub

    def select_substituted_product(self):
        """
        Get a list of products with a substitute.

        Execute the SQL query which retrieves the list of products with
         a substitute. And return this list.

        Returns
            list
                The list of products with a substitute.
        """
        req = "SELECT DISTINCT id_product, Product.name_product " \
              "FROM Substitute " \
              "INNER JOIN Product ON Product.id=Substitute.id_product"
        response = self.connector.select(req)
        list_prod = []
        for prod in response:
            product = {"id": prod[0], "name": prod[1]}
            list_prod.append(product)
        return list_prod

    def associate_sub_to_prod(self, pm, cm, sm, pcm, psm, api, product):
        """
        Associate a substitue to a product in the database.

        Get a list of all the database products.
        Get a list of all the product categories.
        Retrieves a list of products from the database, having one of the
         categories and a nutri-score lower than that of the product you want
         to substitute.
        If the list of products is full:
        Return it.
        If the list of products is empty:
        Searches the OpenFoodFact API for substitutes and returns a list of
         its substitutes.

        Parameters:
            pm : class ProductManager
                The manager of the Product table in the database.

            cm : class CategoryManager
                The manager of the Categories table in the database.

            sm : class StoreManager
                The Manager of the Categories table in the database.

            pcm : class ProductCategoryManager
                The manager of the ProductCategory table in the database.

            psm : class ProductStoreManager
                The manager of the ProductStore table in the database.

            api : Class ApiManagerSearch
                The manager of the OpenFoodFact API research manager.

            product : dict
                The product to which we want to associate a store.

        Returns:
            list
                The list of possible substitutes for the product.
        """
        list_product_bdd = pm.select(pcm, psm)
        list_cat_product = pcm.select_asso_with_id_prod(product["id"])
        list_substitute_possible = []

        for prod in list_product_bdd:
            prod["category"] = pcm.select_asso_with_id_prod(prod["id"])
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
