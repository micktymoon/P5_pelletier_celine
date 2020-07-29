import mysql.connector


class MysqlConnector:
    """
    Class that allows you to connect to MySQL and execute SQL requests.

    Attributes:
        host : str
            The host we use to connect to MySQL.
        user : str
            The user we use to connect to MySQL.
        password : str
            The password of the user we use to connect to MySQL.

    Methods:

        execute(req, info=(), **kwargs)
            Execute a SQL request and return an id if an id is created
             with the request.

        select(req, info=())
            Execute a SQL request, fetch all the results of the request
             and return them.

        use_db()
            Try to use the database, if the database exists it returns
             True else it returns False.
    """

    def __init__(self, host, user, password):
        """
        MysqlConnector class constructor.

        Parameters:
            host : str
                The host we use to connect to MySQL.
            user : str
                The user we use to connect to MySQL.
            password : str
                The password of the user we use to connect to MySQL.
        """
        self.connexion = mysql.connector.connect(host=host,
                                                 user=user,
                                                 password=password)

    def execute(self, req, info=(), **kwargs):
        """
        Execute a SQL request and return an id if an id is created
         with the request.

        Create the cursor we need for the execution.
        Try to execute the SQL request, if there are no kwargs it commit
         the changement and if an id is created with the request it returns
         the id that was created.
        And finally close the cursor.

        Parameters:
            req : str
                The request that we want to execute.
            info : tuple, optional
                The informations we need to execute the request.
                (default is empty)
            **kwargs : multi=1, optional
                The argument we need if we want to execute many requests.
        """
        cursor = self.connexion.cursor()
        try:
            cursor.execute(req, info, **kwargs)
            id_create = cursor.lastrowid
            if not kwargs:
                self.connexion.commit()
            if id_create:
                return id_create
        finally:
            cursor.close()

    def select(self, req, info=()):
        """
        Execute a SQL request, get all the results of the request
         and return them.

        Create the cursor we need for the execution.
        Execute the SQL request, fetch all the result of the request,
         close the cursor and return the results who were recovered
         with the request.

        Parameters:
            req : str
                The request that we want to execute.
            info : tuple, optional
                The informations we need to execute the request.
                (default is empty)

        Returns:
            list
                A list of the results who have been fetching with the request.
        """
        cursor = self.connexion.cursor()
        cursor.execute(req, info)
        result = cursor.fetchall()
        cursor.close()
        return result

    def use_db(self):
        """
        Try to use the database, if the database exists it returns
             True else it returns False.

        Create the cursor we need for the execution.
        Try to use the database 'purBeurre', if it works it returns True
        and if it doesn't works it returns False.
        And finally close the cursor.

        Returns:
            boolean
                True if the request works and False if it doesn't works.

        """
        cursor = self.connexion.cursor()
        try:
            cursor.execute("USE purBeurre")
            return True
        except mysql.connector.Error:
            return False
        finally:
            cursor.close()
