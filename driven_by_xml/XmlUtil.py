#!/usr/bin/python
# -*- encoding: utf-8 -*-


try:
    import xml.etree.cElementTree as ET
except:
    import xml.etree.ElementTree as ET


class ParseXmlByET(object):

    def __init__(self,filePath):
        # 读取xml  --__init__()
        self.filePath = filePath
        self.tree = ET.ElementTree(file=self.filePath)

    def get_root(self):
        # 抓根节点元素
        return self.tree.getroot()

    def get_elem_tag_attrib_text(self,tag):
        # 读取某标签元素所有的属性和text
        elem_data = []
        for child in self.tree.iter(tag=tag):
            elem_data.append((child.tag,child.attrib,child.text))
        return elem_data

    def findNodeByName(self, parentNode, nodeName):
        # 通过节点的名字，获取节点对象
        nodes = parentNode.findall(nodeName)
        return nodes

    def get_child_all(self,tag):
        # 读取某元素下的子元素
        elem_data = []
        root = self.tree.getroot()
        try:
            for elem in root.iter(tag):
                book_name = elem.find("name").text
                book_author = elem.find("author").text
                elem_data.append((book_name,book_author))
        except AttributeError as e:
            return False
        except Exception as e:
            return False
        else:
            return elem_data


if __name__ == "__main__":
    book_xml = ParseXmlByET(r"TestData.xml")
    print(book_xml.get_elem_tag_attrib_text("name"))
    print(book_xml.get_child_all("book"))
