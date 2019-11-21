# 导入Flask类
import os
from datetime import timedelta

from flask import Flask, url_for, redirect, make_response, session
from flask import render_template
from flask import request

from home.controller.UserController import UserController
from home.dao.DBUtil import *

# 实例化，可视为固定格式
app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # 设置session的保存时间

# 设置路径
@app.route('/')
@app.route('/index.html')
def index():
    session['user'] = [()]   # 注册session
    session.permanent = True    # 设置session的过期状态为True
    sql = "select * from goods"
    session['goods'] = DBUtil().selectDb(sql)
    return render_template('index.html', msg = None)

# 用户登录
@app.route('/user/login',methods=['GET','POST'])
def login():
    # 获得form提交的user
    userName = request.form.get('userName')
    userPwd = request.form.get('userPwd')
    userLevel = request.form.get('userLevel')
    # 在数据库中找到user
    sql = "select * from user where user_name = '%s' and user_pwd = '%s' and user_level = '%s'"%(userName,userPwd,userLevel)
    user = list(DBUtil().selectDb(sql))   # 将找回的(())转换为[()]
    # 在控制台中提示
    print("user",user)
    '''
    user是一个列表（里面是元组）
    对查找结果进行判断
        返回非空（长度不为0）：能在数据库中找到user，登录成功
            登录成功就将用户存储到session里面
        返回为空（长度为0）：不能在数据库中找到user，登录失败
    '''
    if len(user) != 0:  # 找到user，登录成功
        session['user'] = user  # 使用session保存user
        print("session",session['user'])
        return render_template('index.html')
    else:   # 没找到user，返回null，并给msg赋值：登录失败
        session['user'] = [()]
        return render_template('index.html', msg ='登录失败，请重新登录！')

# 登出
@app.route('/user/logout')
def logout():
    # 跳转到本方法后将session['user']中的值注销掉
    session.clear()
    return redirect(url_for('index'))

# 用户注册
@app.route('/user/register',methods=['GET','POST'])
def register():
    # 获取form表单提交的数值
    userName = request.form.get('userName')
    userPwd = request.form.get('userPwd')
    userPhone = request.form.get('userPhone')
    userEmail = request.form.get('userEmail')
    userLevel = request.form.get('userLevel')
    # 封装到user列表里
    user = [userName, userPwd,userPhone,userEmail,userLevel]
    # 通过sql语句向后台添加user，可能数据库操作会报错，使用try-except将错误提出，保证程序正常运行
    try:
        sql = "insert into user (user_name,user_pwd,user_phone,user_email,user_level) values (%s,%s,%s,%s,%s)"
        DBUtil().insertDB(sql, user)
        # 添加成功后返回“添加成功”到控制台
        print('添加成功', userName)
    except Exception as e:      # 拦截所有的异常
        print('添加失败',userName)
        print(e)
    finally:
        user = [(0, userName, userPwd, userPhone, userEmail, userLevel)]
    # 由于注册到数据库中，直接将用户添加到session中
    session['user'] = user
    return render_template('index.html')

# 搜索商品
@app.route('/goods/selectGoods', methods=['GET', 'POST'])
def select_goods():
    # 传入待查找的名字
    nameKeyword = request.form['nameKeyword']
    print('nameKeyword', nameKeyword)
    sql_nameKeyword = "%" + str(nameKeyword) + "%"
    print(sql_nameKeyword)
    # 使用sql语句模糊查找
    sql = "select * from goods where goods_name like  '%s' " % sql_nameKeyword
    # 处理找到的列表,使用session，返回到index.html
    session['goods'] = DBUtil().selectDb(sql)
    print(session['goods'])
    return render_template('index.html', msg=None)

# 跳转到购物车
@app.route('/goods/shoppingcart',methods=['GET','POST'])
def shopcart_html():
    return render_template('shoppingcart.html')

# 启动开关
if __name__ == '__main__':
    # app.run(host, port, debug, options)
    # 默认值：host=127.0.0.1, port=5000, debug=false
    app.run()