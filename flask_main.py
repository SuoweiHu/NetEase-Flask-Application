# import time
# from os import abort
# import sys
# sys.path.append("../")

# from crawler_n_db import NetEase_Crawler, NetEase_Mongodb
#     # NetEase_Crawler, # 获取/解析页面
#     # NetEase_Mongodb  # 数据库

# from flask import Flask, request, render_template, flash, url_for, redirect, session
#     # Flask,    # Flask web应用实例
#     # request,  # 获得HTTP请求信息(Query)
#     # render_template, # 渲染页面模版
#     # url_for,  # 构造URL
#     # flash,    # 消息闪现
#     # # Blueprint # 蓝图(用于组织视图)


# app = Flask(__name__) 
# app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# # # session configuraiton -- filesystem interface
# # SESSION_TYPE = 'filesystem'
# # app.config.from_object(__name__)
# # session(app)

# db = None
# dr_state = False
# db_state = False
# account='13735502141'
# password='husuowei200029'

# # 主页面(初始化界面)
# @app.route('/', methods=['GET', "POST"]) 
# @app.route('/index', methods=['GET', "POST"]) 
# def index():
#     session["crawler"] = "Hello" 

#     # db_state_string = "已连接" if db_state else "未连接"
#     # dr_state_string = "已初始化实例" if dr_state else "未初始化"
#     return render_template("index.html", database_state="未知", driver_state="未知")
#     # return redirect(url_for('initialize'))


# # 初始化请求处理 
# def initialize_pkg(request_dict, db_state=None, dr_state=None):
#     """
#     request_dict["init_option"] can be either:
#         database-init: connet to the database 
#         database-clear: connect/ clear existing docs/ close connection
#         webdriver-init: boot webdriver
#     return 
#         True: if operation is a success 
#         False: otherwise
#     """
#     if(request_dict["init_option"] == "database-init"):
#         db = NetEase_Mongodb.Database_Facade()
#         db.start(clear = False)
#         db_state = True
#         # return "You have successfully initialized database. "
#         return (True, dr_state)

#     elif(request_dict["init_option"] == "database-init-clear"):
#         db = NetEase_Mongodb.Database_Facade()
#         db.start(clear = True)
#         db_state = True
#         # return "You have successfullly initialized database and deleted all pre-existing collections."
#         return (True, dr_state)

#     elif(request_dict["init_option"] == "webdriver-init"):
#         crawler = NetEase_Crawler.Crawler_Facade()
#         crawler.start(headless = False, default_login=False)
#         # crawler.login(account=account, password=password)
#         dr_state = True
#         # return "You have successfullly initialized webdriver for the selenium. "
#         return (db_state, True)

#     elif(request_dict["init_option"] == "webdriver-init-headless"):
#         crawler = NetEase_Crawler.Crawler_Facade()
#         crawler.start(headless = True, default_login=False)
#         crawler.login(account=account, password=password)
#         dr_state = True
#         # return "You have successfullly initialized webdriver for the selenium. (With headless option)"
#         return (db_state, True)

#     else:
#         return False
# @app.route('/init', methods=["GET"])
# def initialize():
#     print(session["crawler"])
#     if(request.method == "GET"):
#         request_dict = dict(request.args)
#         if(len(request_dict) == 0): 
#             return redirect(url_for('index'))
#         elif('init_option' in request_dict.keys()):
#             (db_state, dr_state) = initialize_pkg(request_dict)
#             return redirect(url_for('index'))
#         elif('login' in request_dict.keys()):
#             return render_template("login.html")
#         else:
#             abort(404)
#     else:
#         abort(404)
#     #     db_state_string = "Connected" if db_state else "Not Connected"
#     #     dr_state_string = "Instentiated" if dr_state else "Disabled"
#     #     return render_template("index.html", database_state=db_state_string, driver_state=dr_state_string)


# # 登录请求处理
# @app.route('/login', methods=["POST"])
# def login():

#     # 如果HTTP方法为GET,那么就是用form方法获得请求参数
#     if(request.method == "POST"):
#         query_dict = dict(request.form)
#         if(request.form.get("option") == "username+password"):
#             username = request.form.get("username")
#             password = request.form.get("password")
#             crawler.login(account=account, password=password)

#             print(f"\t*Logging in with following credential")
#             print(f"\t*Username: {username} {password}")

#             return 

#         elif(request.form.get("option") == "cookie"):
#             cookie = request.form.get("cookie")
#             # crawler.login(cookie=)

#             print(f"\t*Logging in with following credential")
#             print(f"\t*Cookie: {cookie}")

#             raise("Cookie login (with request session) has not yet been implmented")
#             return 
            

#         return str(query_dict)
    
#     # 不对其他方法作响应
#     else:
#         abort(404)
 

# # 爬取请求处理
# @app.route('/craw/<string:craw_type>', methods=["GET"])
# def craw():
#     # crawler.
#     return

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=9512, debug=True)
    