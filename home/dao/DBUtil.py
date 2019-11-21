# FileName : DBUtil.py

import pymysql

# username : root
# password : root


class DBUtil(object):
    ''' 定义一个 MySQL 操作类'''

    def __init__(self):
        '''初始化数据库信息并创建数据库连接'''
        # 下面的赋值其实可以省略，connect 时 直接使用形参即可
        self.db = pymysql.connect(
            host = 'localhost',
            user = 'root',password = 'root',
            database = 'coffee',
            charset='utf8')




    def insertDB(self,sql,para):
        ''' 插入数据库操作 '''

        self.cursor = self.db.cursor()

        try:
            # 执行sql
            self.cursor.execute(sql,para)
            # tt = self.cursor.execute(sql)  # 返回 插入数据 条数 可以根据 返回值 判定处理结果
            # print(tt)
            self.db.commit()
        except:
            # 发生错误时回滚
            self.db.rollback()
        finally:
            self.cursor.close()



    def deleteDB(self,sql):
        ''' 操作数据库数据删除 '''
        self.cursor = self.db.cursor()

        try:
            # 执行sql
            self.cursor.execute(sql)
            # tt = self.cursor.execute(sql) # 返回 删除数据 条数 可以根据 返回值 判定处理结果
            # print(tt)
            self.db.commit()
        except:
            # 发生错误时回滚
            self.db.rollback()
        finally:
            self.cursor.close()





    def updateDb(self,sql):
        ''' 更新数据库操作 '''

        self.cursor = self.db.cursor()

        try:
            # 执行sql
            self.cursor.execute(sql)
            # tt = self.cursor.execute(sql) # 返回 更新数据 条数 可以根据 返回值 判定处理结果
            # print(tt)
            self.db.commit()
        except:
            # 发生错误时回滚
            self.db.rollback()
        finally:
            self.cursor.close()





    def selectDb(self,sql):
        ''' 数据库查询 '''
        self.cursor = self.db.cursor()
        try:
            self.cursor.execute(sql) # 返回 查询数据 条数 可以根据 返回值 判定处理结果

            return self.cursor.fetchall() # 返回所有记录列表

        finally:
            self.cursor.close()


    def closeDb(self):
        ''' 数据库连接关闭 '''
        self.db.close()



if __name__ == '__main__':

    dbUtil= DBUtil()

    # dbUtil.insertDB('insert into test(name) values ("%s")'%('Xue'))
    # dbUtil.insertDB('insert into test(name) values ("%s")'%('Xue'))
    sql = "select * from user where user_name = '%s' and user_pwd = '%s' and user_level = '%s'" % ('user', '123', '1')
    result = dbUtil.selectDb(sql)
    for r in result:
        print(r[1])

    # dbUtil.updateDb('update test set name = "%s" where sid = "%d"' %('Kai',22))
    # dbUtil.selectDb('select * from test')
    # dbUtil.insertDB('insert into test(name) values ("%s")'%('Li'))
    # dbUtil.deleteDB('delete from test where sid > "%d"' %(25))
    # dbUtil.selectDb('select * from test')
    dbUtil.closeDb()