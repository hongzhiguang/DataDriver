#!/usr/bin/python
# -*- encoding: utf-8 -*-

import ddt
import unittest
import time
import logging
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from Config import *
from ReadData import *


logging.basicConfig(
    level=logging.INFO,
    format="%%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s",
    datefmt ='%a, %Y-%m-%d %H:%M:%S',
    filename="report.txt",
    filemode = "a+"
)

db_data = QueryData(host=host,user=user,password=password,port=port,charset=charset)
db_data.select_db(database)
row_num = db_data.count_num()
data = []
for i in range(1,row_num+1):
    test_data = db_data.get_one(table, i, test_data_col_no)
    expect_data = db_data.get_one(table, i, expect_data_col_no)
    data.append((test_data,expect_data))


@ddt.ddt
class DrivenBySql(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(executable_path="c:\chromedriver")

    @ddt.data(*data)
    def test_by_sql(self,data):
        testData,expetData = tuple(data)
        print(testData,expetData)
        url = "https://www.baidu.com"
        self.driver.get(url)
        self.driver.implicitly_wait(10)
        try:
            self.driver.find_element_by_id("kw").send_keys(testData)
            self.driver.find_element_by_id("su").click()
            time.sleep(5)
            self.assertTrue(expetData in self.driver.page_source)
        except NoSuchElementException as e:
            logging.error("页面找不到！")
        except AssertionError as e:
            logging.info("断言失败！")
            db_data.insert_res(table,"断言失败",testData)
        except Exception as e:
            logging.error("其他错误！")
        else:
            db_data.insert_res(table,"成功",testData)

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
    db_data.close()