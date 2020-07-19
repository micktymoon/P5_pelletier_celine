#!/usr/bin/python3
# -*-coding: utf8 -*-


class DatabaseManager:
    """ """
    def __init__(self, connector):
        self.connector = connector

    def create_db(self):
        req = "CREATE DATABASE purBeurre"
        self.connector.execute(req)

    def erase_db(self):
        req = "DROP DATABASE purBeurre"
        self.connector.execute(req)

    def create_table(self):
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
            PRIMARY KEY (id)
            )
            ENGINE=InnoDB DEFAULT CHARSET=utf8;
        CREATE TABLE ProductCategory (
            id_cat INT UNSIGNED NOT NULL,
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

    def __init__(self, connector):
        self.connector = connector

    def delete(self, id_delete):
        req = "DELETE FROM Categories WHERE id = %s"
        self.connector.execute(req, (id_delete,))

    def insert(self, category):
        req = "INSERT INTO Categories (name_cat) VALUES (%s)"
        id_ = self.connector.execute(req, (category["name"],))
        category["id"] = id_

    def update(self, id_cat_update, name_cat_update):
        infos = (name_cat_update, id_cat_update)
        req = "UPDATE Categories SET name_cat= %s WHERE id = %s"
        self.connector.execute(req, infos)

    def select(self):
        req = "SELECT * FROM Categories"
        response = self.connector.select(req)
        list_cat = []
        for cat in response:
            category = {"id": cat[0], "name": cat[1]}
            list_cat.append(category)
        return list_cat

    def get(self, id_cat):
        req = "SELECT name_cat FROM Categories WHERE id = %s"
        response = self.connector.select(req, (id_cat,))
        category = {"id": id_cat, "name": response[0][0]}
        return category


class StoreManager:

    def __init__(self, connector):
        self.connector = connector

    def delete(self, id_delete):
        req = "DELETE FROM Store WHERE id = %s"
        self.connector.execute(req, (id_delete,))

    def insert(self, store):
        req = "INSERT INTO Store (name_store) VALUES (%s)"
        id_ = self.connector.execute(req, (store["name"],))
        store['id'] = id_

    def update(self, id_store_update, name_store_update):
        infos = (name_store_update, id_store_update)
        req = "UPDATE Store SET name_cat= %s WHERE id = %s"
        self.connector.execute(req, infos)

    def select(self):
        req = "SELECT * FROM Store"
        return self.connector.select(req)
        # for x in select:
        #     print("id {} : {}".format(x[0], x[1]))

    def get(self, id_store):
        req = "SELECT name_store FROM Store WHERE id = %s"
        return self.connector.select(req, (id_store,))


class ProductManager:

    def __init__(self, connector):

        self.connector = connector

    def delete(self, id_delete):
        req = "DELETE FROM Product WHERE id = %s"
        self.connector.execute(req, (id_delete,))

    def insert(self, product):
        req = "INSERT INTO Product " \
              "(name_product, brand, category, nutri_score, store, ingredient) " \
              "VALUES (%s, %s, %s, %s, %s, %s)"
        id_= self.connector.execute(req, (product["name"],
                                     product["brand"],
                                     product["category"],
                                     product["nutri_score"],
                                     product["store"],
                                     product["ingredients"]))
        product["id"] = id_

    def update(self, product):
        req = "UPDATE Product SET name_product=%s, brand=%s, category=%s, nutri_score=%s, store=%s, ingredient=%s" \
              "WHERE id=%s"
        self.connector.execute(req, (product["name"],
                                     product["brand"],
                                     product["category"],
                                     product["nutri_score"],
                                     product["store"],
                                     product["ingredient"],
                                     product["id"]))

    def select(self):
        req = "SELECT * FROM Product"
        select = self.connector.select(req)
        list_product = []
        for product in select:
            product_return = {"id": product[0],
                              "name": product[1],
                              "brand": product[2],
                              "category": product[3],
                              "nutriscore": product[4],
                              "store": product[5],
                              "ingredient": product[6]}
            list_product.append(product_return)
        return list_product

    def get(self, id_product):
        req = "SELECT name_product, brand, category, nutri_score, store, ingredient FROM Product " \
              "WHERE Product.id = %s"
        select = self.connector.select(req, (id_product,))
        product = {"id": id_product,
                   "name": select[0][0],
                   "brand": select[0][1],
                   "category": select[0][2],
                   "nutriscore": select[0][3],
                   "store": select[0][4],
                   "ingredient": select[0][5]}
        return product


class ProductCategoryManager:
    """"""
    def __init__(self, connector):
        self.connector = connector

    def insert_product_category(self, id_cat, id_product):
        req = "INSERT INTO ProductCategory (id_cat, id_product_cat)" \
              "VALUES (%s, %s)"
        self.connector.execute(req, (id_cat, id_product))


