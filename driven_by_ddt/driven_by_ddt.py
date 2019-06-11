import ddt
import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt ='%Y/%m/%d %H:%M:%S',
    filename="report.txt",
    filemode = "a+"
)

@ddt.ddt
class DrivenByDdt(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(executable_path="c:\chromedriver")

    @ddt.data(["还珠格格","小燕子"],["西游记","猪八戒"])
    @ddt.unpack
    def test_driverbyddt(self,testData,expectData):
        url = "https://www.baidu.com/"
        self.driver.get(url)
        self.driver.implicitly_wait(10)
        try:
            self.driver.find_element_by_id("kw").send_keys(testData)
            self.driver.find_element_by_id("su").click()
            time.sleep(3)
            self.assertTrue(expectData in self.driver.page_source)
        except NoSuchElementException as e:
            logging.error(e)
        except AssertionError as e:
            logging.info(u"搜索“%s”，期望“%s”，失败" %(testData, expectData))
        except Exception as e:
            logging.error(e)
        else:
            logging.info(u"搜索“%s”，期望“%s”通过" % (testData, expectData))

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":

    unittest.main()

