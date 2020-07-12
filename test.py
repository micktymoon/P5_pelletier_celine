from classe_mysql import MysqlConnector
from classeBDD import DatabaseManager, CategoryManager

connector = MysqlConnector("localhost", "root", "cP93*mR78.")
connector.use_db()

pizza = CategoryManager(connector, "Pizzas")
pizza.insert()
pizza.select()
"je suis nul avec git"
