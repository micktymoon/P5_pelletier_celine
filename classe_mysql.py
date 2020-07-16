import mysql.connector


class MysqlConnector:
    """ Class that allows you to connect to MySQL and the database and execute SQL requests"""

    def __init__(self, host, user, password):
        self.connexion = mysql.connector.connect(host=host,
                                                 user=user,
                                                 password=password)

    def execute(self, req, info=(), **kwargs):
        """
        execute('sql')
        execute('sql %s', ('toto'))
        execute('sql1;sql2;', multi=1)
        """
        cursor = self.connexion.cursor()
        cursor.execute(req, info, **kwargs)
        id_create = cursor.lastrowid
        self.connexion.commit()
        cursor.close()
        if id_create:
            return id_create

    def select(self, req, info=()):
        cursor = self.connexion.cursor()
        cursor.execute(req, info)
        select = cursor.fetchall()
        cursor.close()
        return select

    def use_db(self):
        cursor = self.connexion.cursor()
        try:
            cursor.execute("USE purBeurre")
            return True
        except mysql.connector.Error:
            return False
        finally:
            cursor.close()


# connector = Mysql("localhost", "toto","tèto")
# if not connector.use('purbeur'):
#     connector.execute('create DB .....')
