from mayflysql.core.field import Field, FieldType, FieldKey
from mayflysql.engine import Engine


e = Engine()                    # 实例化数据库引擎对象
e.create_database('test_db')    # 创建数据库 test_db
e.select_db('test_db')          # 选择数据库 test_db

e.create_table(
    name='t_test',
    f_id=Field(
        data_type=FieldType.INT,
        keys=[
            FieldKey.PRIMARY,
         FieldKey.INCREMENT]),
    f_name=Field(data_type=FieldType.VARCHAR, keys=FieldKey.NOT_NULL),
    f_age=Field(data_type=FieldType.INT, keys=FieldKey.NOT_NULL)
)

# 向数据表 t_test 中插入数据
e.insert(table_name='t_test', f_name='whu_001', f_age=20)
e.insert(table_name='t_test', f_name='whu_002', f_age=10)
e.insert(table_name='t_test', f_name='whu_003', f_age=30)
e.insert(table_name='t_test', f_name='whu_004', f_age=40)
e.insert(table_name='t_test', f_name='goat', f_age=50)
e.insert(table_name='t_test', f_name='echo', f_age=50)

# 保存数据库内容到本地默认的 db.data 文件中
e.commit()

Engine().run()
