import time
from os import abort
import sys
sys.path.append("../")

cache = {}

from crawler_n_db import NetEase_Crawler, NetEase_Mongodb
    # NetEase_Crawler, # 获取/解析页面
    # NetEase_Mongodb  # 数据库

from flask import Flask, request, render_template, flash, url_for, redirect, session, g
    # Flask,    # Flask web应用实例
    # request,  # 获得HTTP请求信息(Query)
    # render_template, # 渲染页面模版
    # url_for,  # 构造URL
    # flash,    # 消息闪现
    # # Blueprint # 蓝图(用于组织视图)

from flask.cli import with_appcontext
from flask.json import jsonify

app = Flask(__name__) 
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# 主页面(初始化界面)
@app.route('/', methods=['GET','POST']) 
@app.route('/index', methods=['GET','POST']) 
def flask_startSession():
    return render_template("login.html")
    # session["dr_state"] = False
    # session["db_state"] = False
    # return redirect(url_for("index"))

# @app.route('/index') 
def index():
    db_state_string = "已连接" if session["db_state"] else "未连接"
    dr_state_string = "已初始化实例" if session["dr_state"] else "未初始化"
    return render_template("index.html", database_state=db_state_string, driver_state=dr_state_string)

# 初始化请求处理 
def initialize_pkg(request_dict):
    """
    request_dict["init_option"] can be either:
        database-init: connet to the database 
        database-clear: connect/ clear existing docs/ close connection
        webdriver-init: boot webdriver
    return 
        True: if operation is a success 
        False: otherwise
    """

    if(request_dict["init_option"] == "database-init"):
        __database__ = NetEase_Mongodb.Database_Facade()
        __database__.start(clear = False)
        # __database__ = NetEase_Mongodb.Database_Facade()
        # __database__.start(clear = False)
        session["db_state"] = True
        # return "You have successfully initialized database. "
        # return (db_state, dr_state)

    elif(request_dict["init_option"] == "database-init-clear"):
        __database__ = NetEase_Mongodb.Database_Facade()
        __database__.start(clear = True)
        session["db_state"] = True
        # return "You have successfullly initialized database and deleted all pre-existing collections."
        # return (db_state, dr_state)

    elif(request_dict["init_option"] == "webdriver-init"):
        __crawler__ = NetEase_Crawler.Crawler_Facade()
        __crawler__.start(headless = False, default_login=False)
        # crawler.login(account=account, password=password)
        session["dr_state"] = True
        # return "You have successfullly initialized webdriver for the selenium. "
        # return (db_state, True)

    elif(request_dict["init_option"] == "webdriver-init-headless"):
        __crawler__ = NetEase_Crawler.Crawler_Facade()
        __crawler__.start(headless = True, default_login=False)
        # crawler.login(account=account, password=password)
        session["dr_state"] = True
        # return "You have successfullly initialized webdriver for the selenium. (With headless option)"
        # return (db_state, True)

    else:
        return False
@app.route('/init', methods=["GET"])
def initialize():
    if(request.method == "GET"):
        request_dict = dict(request.args)
        if(len(request_dict) == 0): 
            return redirect(url_for('index'))
        elif('init_option' in request_dict.keys()):
            initialize_pkg(request_dict)
            time.sleep(2)
            print(session['db_state'], session['dr_state'])
            return redirect(url_for('index'))
        elif('login' in request_dict.keys()):
            return render_template("login.html")
        else:
            abort(404)
    else:
        abort(404)
    #     db_state_string = "Connected" if db_state else "Not Connected"
    #     dr_state_string = "Instentiated" if dr_state else "Disabled"
    #     return render_template("index.html", database_state=db_state_string, driver_state=dr_state_string)

# 登录请求处理
@app.route('/login')
@app.route('/login', methods=["POST"])
def login():
    # 如果HTTP方法为GET,那么就是用form方法获得请求参数
    if(request.method == "POST"):
        if(request.form.get("option") == "username+password"):
            username = request.form.get("username")
            password = request.form.get("password")
            target = request.form.get("target")

            print(f"\t*Logging in with following credential")
            print(f"\t*Username: {username} {password}")

            __crawler__ = NetEase_Crawler.Crawler_Facade()
            __crawler__.start(headless = True, default_login=False)
            __crawler__.login(account=username, password=password)
            r_dict_ = __crawler__.craw(target, recursive=True, save_json=True)
            __crawler__.close()

            __database__ = NetEase_Mongodb.Database_Facade()
            __database__.start(clear = False)
            __database__.insert(r_dict_, target) 
            __database__.close()
            return render_template("success.html")

        elif(request.form.get("option") == "cookie"):
            cookie = request.form.get("cookie")
            target = request.form.get("target")
            # crawler.login(cookie=)

            print(f"\t*Logging in with following credential")
            print(f"\t*Cookie: {cookie}")

            print("Cookie login (with request session) has not yet been implmented")
            raise("Cookie login (with request session) has not yet been implmented")
            return 

    
    # 不对其他方法作响应
    else:
        abort(404)
 
if __name__ == "__main__":
    __crwaler__ = None
    __database__ = None
    app.run(host="0.0.0.0", port=9512, debug=True)
    