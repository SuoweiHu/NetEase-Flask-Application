from os import abort
import sys

from flask.helpers import get_flashed_messages
sys.path.append("../")
from flask import Flask, request, render_template
from crawler_n_db import NetEase_Crawler, NetEase_Mongodb


app = Flask(__name__) # Flask web应用实例
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


# 主页面 index.html
@app.route('/') 
def index():
    return render_template("index.html")


# 登录页面 login.html
@app.route('/login', methods=['GET', "POST"])
def login():
    # 如果HTTP方法为GET,那么就是用args方法获得请求参数
    if(request.method == "GET"):
        return str(dict(request.form))

    # 如果HTTP方法为GET,那么就是用form方法获得请求参数
    elif(request.method == "POST"):
        query_dict = dict(request.form)
        if(request.form.get("option") == "username+password"):
            username = request.form.get("username")
            password = request.form.get("password")
            return f"Username: {username} {password}"
        elif(request.form.get("option") == "cookie"):
            cookie = request.form.get("cookie")
            return f"Cookie: {cookie}"

        return str(query_dict)
    
    # 不对其他方法作响应
    else:
        abort(404)
 

# 初始化页面 
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
        try: 
            NetEase_Mongodb.start(clear=False)
            return True
        except:
            print("Database initalization failure.")
            return False

    elif(request_dict["init_option"] == "database-init-clear"):
        try: 
            NetEase_Mongodb.start(clear=True)
            return True
        except:
            print("Database initalization failure.")
            return False

    elif(request_dict["init_option"] == "webdriver-init"):
        try:
            NetEase_Crawler.start(clear=True)
            return True
        except:
            print("Driver initalization failure.")
            return False

    else:
        return False
@app.route('/init', methods=["POST","GET"])
def initialize():
    if(request.method == "GET"):
        request_dict = dict(request.args)
        initialize_pkg(request_dict)
        return
    elif(request.method == "POST"):
        request_dict = dict(request.form)
        initialize_pkg(request_dict)
        return
    else:
        abort(404)


# 等待页面 wait.html
@app.route('/wait')
def wait():
    return "<h1> Waiting for crawler to finish... </h1>"


if __name__ == "__main__":
    __driver__ = None
    app.run(host="0.0.0.0", port=9512, debug=True)
    