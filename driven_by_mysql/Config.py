#encoding=utf-8

# 数据库登陆信息
host="127.0.0.1"
user="root"
password="123456"
port=3306
charset="utf8"


# 创建数据库
database = "testdb"

# 创建表
table = "testdata"

create_table = """
    
    create table testdata(
        id int not null auto_increment comment '主键',
        bookname varchar(40) unique not null comment '书名',
        author varchar(30) not null comment '作者',
        test_result varchar(30) default null,
        primary key(id)
    )engine=innodb character set utf8 comment '测试数据表';
"""

# 插入数据
insert_data = [('人工智能改变未来', '野村直之'),
                                  ('能力陷阱', '埃米尼亚'),
                                  ('暗时间', '刘未鹏'),
                                  ("别让拖延症毁掉你","李世强")
               ]

test_data_col_no = 2
expect_data_col_no = 3
test_result_col_no = 4