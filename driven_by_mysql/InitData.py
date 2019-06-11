#!/usr/bin/python
# -*- encoding: utf-8 -*-

import pymysql
import os
from Config import *
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s",
    datefmt ='%a, %Y-%m-%d %H:%M:%S',
    filename="report.txt",
    filemode = "a+"
)

class InitData(object):
    """
    通过此类向数据库插入测试的数据

    """

    def __init__(self,**kwargs):
        self.host = kwargs["host"]
        self.user = kwargs["user"]
        self.password = kwargs["password"]
        self.port = kwargs["port"]
        self.charset = kwargs["charset"]
        # 创建数据库链接
        self.__connect()
        # 创建一个可执行sql语句的对象
        self.cur = self.conn.cursor()
        self.count = 0

    def __connect(self):
        # 创建一个连接的实例对象
        try:
            self.conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port,
                charset=self.charset
            )
        except pymysql.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    def create_database(self, databaseName):
        create_cmd = "CREATE DATABASE IF NOT EXISTS %s DEFAULT CHARSET utf8 COLLATE utf8_general_ci;" % databaseName
        self.__exec(create_cmd)

    def create_table(self,tableName,cmd):
        drop_table_if_exist_sql = "drop table if exists %s;" % tableName
        self.__exec(drop_table_if_exist_sql)
        self.__exec(cmd)

    def insert_data(self,table,data):
        for i in data:
            bookname_value, author_value = i
            insert_cmd = 'insert into %s(bookname,author) values(%s,%s);' % (table,repr(bookname_value),repr(author_value))
            self.__exec(insert_cmd)

    def select_db(self,db):
        self.conn.select_db(db)

    def delete_db(self,db):
        del_cmd = "drop database %s" % db
        self.__exec(del_cmd)

    def __exec(self, sql):
        # 创建一个可执行sql语句的对象
        try:
            self.count = self.cur.execute(sql)
            return self.cur
        except pymysql.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
            logging.error("Mysql Error %d: %s" % (e.args[0], e.args[1]))
            return False

    def __del__(self):
        try:
            self.cur.close()
            self.conn.commit()
            self.conn.close()
        except:
            pass

    def close(self):
        self.__del__()

if __name__ == "__main__":
    init = InitData(host=host,user=user,password=password,port=port,charset=charset)
    # init.create_database(database)
    init.select_db(database)
    # init.create_table(table,create_table)
    init.insert_data(table,insert_data)
    init.close()