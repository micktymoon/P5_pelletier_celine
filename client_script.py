#!/usr/bin/python3
# -*-coding: utf8 -*-
from classe_mysqlconnector import MysqlConnector
from classe_database import CategoryManager, ProductManager, \
    ProductCategoryManager, ProductStoreManager, SubstituteManager
from classe_api import ApiManageSearch
from classe_ui import UserInterfaceManager


def main():
    connector = MysqlConnector("localhost", "root", "cP93*mR78.")
    connector.use_db()
    api = ApiManageSearch()
    cm = CategoryManager(connector)
    pm = ProductManager(connector)
    pcm = ProductCategoryManager(connector)
    psm = ProductStoreManager(connector)
    subm = SubstituteManager(connector)
    uim = UserInterfaceManager(cm, pm, pcm, psm, subm, api)
    uim.main_menu()


if __name__ == "__main__":
    main()
