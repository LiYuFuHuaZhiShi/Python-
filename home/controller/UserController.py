# 导入Flask类
import os
from datetime import timedelta

from flask import Flask, url_for, redirect, make_response, session
from flask import render_template
from flask import request
from home.dao.DBUtil import *

class UserController():

    # 实例化，可视为固定格式
    app = Flask(__name__)



