#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(__file__))

import ddt
import time,traceback
import unittest
import logging
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from ExcelUtil import *
from ProjVar import *


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt ='%Y/%m/%d %H:%M:%S',
    filename="report.txt",
    filemode = "a+"
)

test_excel = ParseExcel("data.xlsx")
test_data_list = test_excel.get_col_value(test_data_col_no)
expect_data_list = test_excel.get_col_value(test_expect_data_col_no)
data_list = list(zip(test_data_list,expect_data_list))


current_test_row = 2

@ddt.ddt
class DrivenByExcel(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(executable_path="c:\chromedriver")

    @ddt.data(*data_list)
    def test_by_excel(self,data):
        global current_test_row
        testData,expectData = tuple(data)
        url = "https://www.baidu.com"
        self.driver.get(url)
        self.driver.implicitly_wait(10)
        try:
            self.driver.find_element_by_id("kw").send_keys(testData)
            self.driver.find_element_by_id("su").click()
            time.sleep(3)
            self.assertTrue(expectData in self.driver.page_source)
        except NoSuchElementException as e:
            logging.error(u"查找的页面元素不存在，异常堆栈信息："+ str(traceback.format_exc()))
            test_excel.write_cell(current_test_row,test_result_col_no,"执行错误")
        except AssertionError as e:
            logging.info(u"搜索“%s”，期望“%s”，失败" %(testData, expectData))
            test_excel.write_cell(current_test_row,test_result_col_no,"断言失败")
        except Exception as e:
            logging.error(u"未知错误，错误信息：" + str(traceback.format_exc()))
            test_excel.write_cell(current_test_row,test_result_col_no,"执行错误")
        else:
            logging.info(u"搜索“%s”，期望“%s”通过" %(testData, expectData))
            test_excel.write_cell(current_test_row,test_result_col_no,"成功")
        test_excel.write_exec_time(current_test_row, test_time_col_no)
        current_test_row += 1

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
