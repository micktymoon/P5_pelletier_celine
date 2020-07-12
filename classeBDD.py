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
        self.connector.execute_multi(req)


class CategoryManager:

    def __init__(self, connector, category):
        self.connector = connector
        self.name_category = category

    def delete(self):
        req = "DELETE FROM Categories WHERE name_cat = %s"
        self.connector.execute_info(req, (self.name_category,))

    def insert(self):
        req = "INSERT INTO Categories (name_cat) VALUES (%s)"
        self.connector.execute_info(req, (self.name_category,))

    def update(self, id_cat_update, name_cat_update):
        infos = (name_cat_update, id_cat_update)
        req = "UPDATE Categories SET name_cat= %s WHERE id = %s"
        self.connector.execute_info(req, infos)

    def select(self):
        req = "SELECT * FROM Categories"
        self.connector.select(req)

    def get(self, id_cat):
        req = "SELECT name_cat FROM Categories WHERE id = %s"
        print(self.connector.select(req, (id_cat,)))


class ProductManager:

    def __init__(self):
        self.id = int
        self.name_product = str
        self.brand = str
        self.category_id = int
        self.nutri_score = int
        self.store = str
        self.ingredient = str

    def delete(self, mysql_cmd, conn, cursor, id_product_delete):
        req = "DELETE FROM Product WHERE id = %s"
        mysql_cmd.exec_infos(cursor, req, (id_product_delete,))
        mysql_cmd.commit(conn)
        mysql_cmd.cursor_close(cursor)

    def insert(self, mysql_cmd, conn, cursor, product):
        req = "INSERT INTO Product (name_product, brand, category_id, nutri_score, store, ingredient) " \
              "VALUES (%s, %s, %s, %s, %s, %s)"
        mysql_cmd.exec_infos(cursor, req, product)
        mysql_cmd.commit(conn)
        mysql_cmd.cursor_close(cursor)

    def update(self, mysql_cmd, conn, cursor, id_product_update, product):
        infos = (product[0], product[1], product[2], product[3], product[4],product[5], id_product_update)
        req = "UPDATE Categories " \
              "SET name_product= %s, brand= %s, category_id= %s, nutri_score= %s, store= %s, ingredient= %s " \
              "WHERE id = %s"
        mysql_cmd.exec_infos(cursor, req, infos)
        mysql_cmd.commit(conn)
        mysql_cmd.cursor_close(cursor)

    def select(self, mysql_cmd, cursor):
        req = "SELECT * FROM Product"
        mysql_cmd.exec(cursor, req)
        product_list = mysql_cmd.fetchall(cursor)
        for product in product_list:
            print(" product {} : {}".format(product[0], product[1]))
        mysql_cmd.cursor_close(cursor)

    def get(self, mysql_cmd, cursor, id_product):
        req = "SELECT name_product, brand, Categories.name_cat, nutri_score, store, ingredient FROM Product " \
              "INNER JOIN Categories ON Categories.id = Product.category_id " \
              "WHERE id = %s"
        mysql_cmd.exec_infos(cursor, req, (id_product,))
        product = mysql_cmd.fetchall(cursor)
        print("name : {} "
              "brand : {}"
              "category : {}"
              "nutriscore : {}"
              "store : {}"
              "ingredients : {}".format(product[0], product[1], product[2], product[3], product[4], product[5]))
        mysql_cmd.cursor_close(cursor)
