import mysql.connector


class MysqlConnector:

    def __init__(self, host, user, password):
        self.connexion = mysql.connector.connect(host=host,
                                                 user=user,
                                                 password=password)

    def execute(self, req):
        cursor = self.connexion.cursor()
        cursor.execute(req)
        self.connexion.commit()
        cursor.close()

    def execute_multi(self, req):
        cursor = self.connexion.cursor()
        cursor.execute(req, multi=1)
        self.connexion.commit()
        cursor.close()

    def execute_info(self, req, info):
        cursor = self.connexion.cursor()
        cursor.execute(req, info)
        self.connexion.commit()
        cursor.close()

    def select(self, req):
        cursor = self.connexion.cursor()
        cursor.execute(req)
        select = cursor.fetchall()
        for x in select:
            print("Catégorie {} : {}".format(x[0], x[1]))
        cursor.close()
        return select

    def use_db(self):
        cursor = self.connexion.cursor()
        cursor.execute("USE purBeurre")
        cursor.close()


# connector = Mysql("localhost", "toto","tèto")
# if not connector.use('purbeur'):
#     connector.execute('create DB .....')
