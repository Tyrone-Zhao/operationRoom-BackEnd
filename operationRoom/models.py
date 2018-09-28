from pymysql import connect, cursors
from pymysql.err import OperationalError
import os
import time
import configparser as cparser
import os

# __file__ refers to the file settings.py
APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_CONFIG_PATH = os.path.join(APP_ROOT, 'db_config.ini')

# ======== 封装读取 db_config.ini 文件设置 ========= #

# 框架
# def db_config(configPath='/db_config.ini'):
#     base_dir = str(os.path.dirname(os.path.dirname(__file__)))
#     base_dir = base_dir.replace('\\', '/')
#     file_path = base_dir + configPath
#     print(file_path)

#     cf = cparser.ConfigParser()
#     cf.read(file_path)

#     host = cf.get('mysqlconf', 'host')
#     port = cf.get('mysqlconf', 'port')
#     db = cf.get('mysqlconf', 'db_name')
#     user = cf.get('mysqlconf', 'user')
#     password = cf.get('mysqlconf', 'password')

#     return host, port, db, user, password


# 模块
def db_config(configPath="db_config.ini"):
    cf = cparser.ConfigParser()
    cf.read(configPath)

    host = cf.get('mysqlconf', 'host')
    port = cf.get('mysqlconf', 'port')
    db = cf.get('mysqlconf', 'db_name')
    user = cf.get('mysqlconf', 'user')
    password = cf.get('mysqlconf', 'password')

    return host, port, db, user, password

# ======== 封装 MySQL 基本操作 ========= #


class DB():

    def __init__(self, configPath=DB_CONFIG_PATH):
        try:
            config_datas = db_config(configPath)
            print(config_datas)
            # 连接数据库
            self.conn = connect(
                host=config_datas[0],
                user=config_datas[3],
                password=config_datas[4],
                db=config_datas[2],
                charset='utf8mb4',
                cursorclass=cursors.DictCursor
            )
        except OperationalError as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    # 清除表数据
    def clear(self, table_name):
        real_sql2 = 'truncate table ' + table_name + ';'
        real_sql = 'delete from ' + table_name + ';'
        print(real_sql)
        with self.conn.cursor() as cursor:
            cursor.execute('SET FOREIGN_KEY_CHECKS = 0;')
            cursor.execute(real_sql)
            cursor.execute(real_sql2)
        self.conn.commit()

    # 直接执行select_sql语句
    def select_sql(self, real_sql):
        print(real_sql)
        with self.conn.cursor() as cursor:
            cursor.execute(real_sql)
        self.conn.commit()
        return cursor.fetchall(), cursor.rowcount, real_sql

    # 直接执行insert_sql语句
    def insert_sql(self, real_sql):
        print(real_sql)
        with self.conn.cursor() as cursor:
            cursor.execute(real_sql)
        self.conn.commit()

    # 插入表数据
    def insert(self, table_name, table_data):
        for key in table_data:
            table_data[key] = "'" + str(table_data[key]) + "'"
        key = ','.join(table_data.keys())
        value = ','.join(table_data.values())
        real_sql = 'INSERT INTO ' + table_name + \
            '(' + key + ') VALUES (' + value + ')'
        print(real_sql)

        with self.conn.cursor() as cursor:
            cursor.execute(real_sql)
        self.conn.commit()

    # 查询表数据
    def select(self, table_name, column, value, like='', whats=[],
               order=''):
        text = ' WHERE '
        num = len(column)
        # 拼接列和数据
        if num == 0 and like == '':
            text = ''
        elif num == 1 and like == '':
            text += column[0] + "='" + str(value[0]) + "'"
        elif num > 1 and like == '':
            for i in range(len(column)):
                text += column[i] + "='" + str(value[i]) + "' AND "
                num -= 1
                if num == 1:
                    text += column[i + 1] + "='" + str(value[i + 1]) + "'"
                    break
        elif num == 1 and like != '':
            text += column[0] + " like '" + like + "'"
        elif num > 1 and like != '':
            text += column[i] + "='" + str(value[i]) + "' AND "
            num -= 1
            if num == 1:
                text += column[i + 1] + " like '" + like + "'"
        else:
            print('ColumnValue Error')

        what = ''
        num_what = len(whats)
        if num_what == 0:
            what = '*'
        elif num_what == 1:
            what = whats[0]
        elif num_what > 1:
            for i in range(len(whats)):
                what += whats[i]
                what += ','
                num_what -= 1
                if num_what == 1:
                    what += whats[i + 1]
                    break

        real_sql = 'SELECT ' + what + ' FROM ' + table_name + text + order
        print(real_sql)

        with self.conn.cursor() as cursor:
            cursor.execute(real_sql)
        self.conn.commit()
        return cursor.fetchall(), cursor.rowcount, real_sql

    # 关闭数据库连接
    def close(self):
        self.conn.close()


if __name__ == "__main__":
    db = DB()
