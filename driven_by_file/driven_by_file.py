#!/usr/bin/python
# -*- encoding: utf-8 -*-
import ddt
import unittest
import logging
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import traceback

logging.basicConfig(
    level=logging.INFO,
    format = "%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s",
    datefmt = '%a, %d %b %Y %H:%M:%S',
    filename="report.log",
    filemode="a+"
)

with open("data.txt", "r") as fp:
    testContent = fp.readlines()

test_list = []
for line in testContent:
    testData = line.strip().split("||")[0]
    expectData = line.strip().split("||")[1]
    test_list.append([testData,expectData])

print(test_list)

@ddt.ddt
class DrivenByFile(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(executable_path="c:\chromedriver")

    @ddt.data(*test_list)
    # @ddt.unpack
    def test_file(self,data):
        testData, expectData = tuple(data)
        url = "https://www.baidu.com"
        self.driver.get(url)
        self.driver.implicitly_wait(10)
        try:
            self.driver.find_element_by_id("kw").send_keys(testData)
            self.driver.find_element_by_id("su").click()
            time.sleep(3)
            self.assertTrue(expectData in self.driver.page_source)
        except NoSuchElementException as e:
            logging.error("页面没有找到！")
        except AssertionError as e:
            logging.info("期望结果没找到！")
        except Exception as e:
            logging.error("其他异常！" )
        else:
            logging.info("期望结果找到了！")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()

