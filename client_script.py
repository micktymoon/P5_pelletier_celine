#!/usr/bin/python3
# -*-coding: utf8 -*-

from database.classe_mysqlconnector import MysqlConnector
from database.classe_database import CategoryManager, ProductManager, \
    ProductCategoryManager, ProductStoreManager, SubstituteManager
from database.classe_api import ApiManageSearch
from user_interface.classe_ui import UserInterfaceManager


def main():
    """
    Run the program.
    """
    connector = MysqlConnector("localhost", "root", "cP93*mR78.")
    connector.use_db()
    api = ApiManageSearch()
    cm = CategoryManager(connector)
    pm = ProductManager(connector)
    sm = SubstituteManager(connector)
    pcm = ProductCategoryManager(connector)
    psm = ProductStoreManager(connector)
    subm = SubstituteManager(connector)
    uim = UserInterfaceManager(cm, pm, sm, pcm, psm, subm, api)
    uim.main_menu()


if __name__ == "__main__":
    main()
