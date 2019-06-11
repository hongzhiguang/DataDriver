#!/usr/bin/python
# -*- encoding: utf-8 -*-

import pymysql
from Config import *

class QueryData(object):
    """
    通过此类来读取测试数据，并插入测试结果
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

    def select_db(self,db):
        self.conn.select_db(db)

    def get_one(self, table, n=1, nVal=None):
        # 获取执行sql语句执行结果任意一行中的任意值
        # n:第n行，nVal：第nVal列
        query_sql = "select * from %s" % table
        cursor = self.__exec(query_sql)
        for i in range(1, self.count + 1):
            tmp = cursor.fetchone()
            if i == n:
                if nVal:
                    return tmp[nVal - 1]
                else:
                    return tmp
            else:
                continue

    def count_num(self):
        # 获取查询的有效行数
        query_sql = "select * from %s" % table
        self.__exec(query_sql)
        return self.count

    def insert_res(self,table,res,condition):
        insert_cmd = 'update %s set test_result=%s where bookname=%s;' % (table, repr(res), repr(condition))
        self.__exec(insert_cmd)

    def __exec(self, sql):
        # 创建一个可执行sql语句的对象
        try:
            self.count = self.cur.execute(sql)
            return self.cur
        except pymysql.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
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
    db_data = QueryData(host=host,user=user,password=password,port=port,charset=charset)
    db_data.select_db(database)
    # 获取行数
    row_num = db_data.count_num()
    data = []
    # 遍历每一行
    for i in range(1,row_num+1):
        # 获取第n行第n列的数据
        test_data = db_data.get_one(table, i, test_data_col_no)
        expect_data = db_data.get_one(table, i, expect_data_col_no)
        data.append((test_data,expect_data))
    print(data)
    # db_data.insert_res(table,"成功","暗时间")
    db_data.close()



