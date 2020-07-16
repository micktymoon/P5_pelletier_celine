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
        DROP TABLE IF EXISTS Categories;
        DROP TABLE IF EXISTS Product;
        DROP TABLE IF EXISTS Substitute;
        CREATE TABLE Categories (
            id INT UNSIGNED NOT NULL AUTO_INCREMENT,
            name_cat VARCHAR(255) NOT NULL,
            PRIMARY KEY (id)
            )
            ENGINE=InnoDB DEFAULT CHARSET=utf8;
        CREATE TABLE Product (
            id INT UNSIGNED NOT NULL AUTO_INCREMENT,
            name_product VARCHAR(255) NOT NULL,
            brand VARCHAR(255),
            category_id INT UNSIGNED,
            nutri_score VARCHAR(2),
            store TEXT,
            ingredient TEXT,
            PRIMARY KEY (id)
            )
            ENGINE=InnoDB DEFAULT CHARSET=utf8;
        CREATE TABLE Substitute (
            id_product INT UNSIGNED NOT NULL,
            id_product_substitute INT UNSIGNED NOT NULL
            )
            ENGINE=InnoDB DEFAULT CHARSET=utf8;
        ALTER TABLE Substitute ADD CONSTRAINT fk_id_product 
        FOREIGN KEY (id_product) REFERENCES Product(id);
        ALTER TABLE Substitute ADD CONSTRAINT fk_id_product_id_product_substitute 
        FOREIGN KEY (id_product_substitute) REFERENCES Product(id);"""
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
        category['id'] = id_

    def update(self, id_cat_update, name_cat_update):
        infos = (name_cat_update, id_cat_update)
        req = "UPDATE Categories SET name_cat= %s WHERE id = %s"
        self.connector.execute(req, infos)

    def select(self):
        req = "SELECT * FROM Categories"
        return self.connector.select(req)
        # for x in select:
        #     print("id {} : {}".format(x[0], x[1]))

    def get(self, id_cat):
        req = "SELECT name_cat FROM Categories WHERE id = %s"
        return self.connector.select(req, (id_cat,))


class ProductManager:

    def __init__(self, connector):

        self.connector = connector

    def delete(self, id_delete):
        req = "DELETE FROM Product WHERE id = %s"
        self.connector.execute(req, (id_delete,))

    def insert(self, product):
        req = "INSERT INTO Product " \
              "(name_product, brand, category_id, nutri_score, store, ingredient) " \
              "VALUES (%s, %s, %s, %s, %s, %s)"
        self.connector.execute(req, (product["name"],
                                     product["brand"],
                                     product["category_id"],
                                     product["nutri_score"],
                                     product["store"],
                                     product["ingredient"]))

    def update(self, product):
        req = "UPDATE Product SET name_product=%s, brand=%s, category_id=%s, nutri_score=%s, store=%s, ingredient=%s" \
              "WHERE id=%s"
        self.connector.execute(req, (product["name"],
                                     product["brand"],
                                     product["category_id"],
                                     product["nutri_score"],
                                     product["store"],
                                     product["ingredient"],
                                     product["id"]))

    def select(self):
        req = "SELECT * FROM Product"
        select = self.connector.select(req)
        return select
        # for product in select:
        #     print("id : {} "
        #           "name : {} "
        #           "brand : {} "
        #           "category_id : {} "
        #           "nutriscore : {} "
        #           "store : {} "
        #           "ingredients : {}".format(product[0], product[1], product[2], product[3], product[4], product[5], product[6]))

    def get(self, id_product):
        req = "SELECT name_product, brand, Categories.name_cat, nutri_score, store, ingredient FROM Product " \
              "INNER JOIN Categories ON Categories.id = Product.category_id " \
              "WHERE Product.id = %s"
        select = self.connector.select(req, (id_product,))
        return select
        # for product in select:
        #     print("name : {} \n"
        #           "brand : {} \n"
        #           "category : {} \n"
        #           "nutriscore : {} \n"
        #           "store : {} \n"
        #           "ingredients : {}".format(product[0], product[1], product[2], product[3], product[4], product[5]))

# pm = ProductManager()
# produit = pm.get('17')
# print(produit)
# produit['brand'] = 'sodebo'
# pm.update(produit)