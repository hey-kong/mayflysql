from mayflysql.core import SerializedInterface
from mayflysql.core.table import Table


# 数据库对象
class Database(SerializedInterface):
    def __init__(self, name):
        self.__name = name  # 数据库名字
        self.__table_names = []  # 所有数据表名
        self.__table_objs = {}  # 数据库表名与表对象映射

    # 创建数据表
    def create_table(self, table_name, **options):
        # 如果数据表名字已存在，抛出数据表已存在异常
        if table_name in self.__table_objs:
            raise Exception('table exists')

        # 追加数据表名字
        self.__table_names.append(table_name)

        # 新建一个数据表对象，并且与数据表名字关联绑定
        self.__table_objs[table_name] = Table(**options)

    # 删除数据表
    def drop_tables(self, table_name):
        # 如果要删除的数据表不存在，则抛出数据表不存在异常
        if table_name not in self.__table_names:
            raise Exception('table not exist')

        # 从 __table_names 中移除
        self.__table_names.remove(table_name)

        # 从 __table_objs 中移除
        self.__table_objs.pop(table_name, True)

    # 获取数据表对象
    def get_table_obj(self, name):
        # 如果指定的数据表名不存在，则返回 None 空对象
        return self.__table_objs.get(name, None)

    # 获取数据库名字
    def get_name(self):
        return self.__name

    # 序列化方法
    def serialized(self):
        # 初始化返回数据
        data = {'name': self.__name, 'tables': []}

        # 遍历所有 Table 对象并调用对应的序列化方法
        for tb_name, tb_data in self.__table_objs.items():
            data['tables'].append(
                [tb_name, tb_data.serialized()]
            )

        # 返回 Json 字符串
        return SerializedInterface.json.dumps(data)

    # 添加数据表
    def add_table(self, table_name, table):
        # 如果数据表名字不存在，则开始添加绑定
        if table_name not in self.__table_objs:
            # 追加数据表名字到 __table_names 中
            self.__table_names.append(table_name)

            # 版定数据表名字与数据表对象
            self.__table_objs[table_name] = table

    # 反序列化对象
    @staticmethod
    def deserialized(obj):
        # 解析 Json 字符串为 dict 字典
        data = SerializedInterface.json.loads(obj)

        # 使用解析出来的数据库名字实例化一个 Database 对象
        obj_tmp = Database(data['name'])

        # 遍历所有 Table Json 字符串，依次调用 Table 对象的反序列化方法，再添加到刚刚实例化出来的 Database 对象中
        for table_name, table_obj in data['tables']:
            obj_tmp.add_table(table_name, Table.deserialized(table_obj))

        # 返回 Database 对象
        return obj_tmp

    # 获取数据表名字
    def get_table(self, index=None):
        length = len(self.__table_names)

        if isinstance(index, int) and -index < length > index:
            return self.__table_names[index]
        return self.__table_names
