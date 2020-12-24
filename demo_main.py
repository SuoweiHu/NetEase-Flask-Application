from file_utils   import  HTML, JSON

from crawler_n_db import NetEase_Crawler, NetEase_Mongodb
# NetEase_Crawler,  # 获取/解析页面
# NetEase_Mongodb   # 数据库

from flask import Flask, request, render_template, flash, url_for
# Flask,            # Flask web应用实例
# request,          # 获得HTTP请求信息(Query)
# render_template,  # 渲染页面模版
# url_for,          # 构造URL
# flash,            # 消息闪现
# # Blueprint       # 蓝图(用于组织视图)


class DEMO:

    def demo_db():
        db = NetEase_Mongodb.Database_Facade()
        db.start(clear=True)
        uid = 505508015
        res = JSON.read("src/user/export.json") 
        db.insert(res, uid) 
        db.close(clear=False)
        return

    def demo_craw():
        crawler = NetEase_Crawler.Crawler_Facade()
        crawler.start(headless = True)
        user_dict = crawler.craw(505508015, recursive=False, save_json=False)
        crawler.close()
        return user_dict

    def demo_main():
        # 用户ID
        uid = 505508015
        archived_userDict = JSON.read("src/user/export.json") 
        del archived_userDict['playlists']

        # 初始化连接/驱动 
        crawler = NetEase_Crawler.Crawler_Facade()
        crawler.start(headless = True, default_login=False)
        crawler.login(account='13735502141', password='husuowei200029')
        db = NetEase_Mongodb.Database_Facade()
        db.start(clear=True)

        # 获取用户数据字典并添加
        crawed_userDict = crawler.craw(uid, recursive=False, save_json=False)
        db.insert(crawed_userDict, uid) 

        # 关闭连接/驱动
        db.close(clear=False)
        crawler.close()

        # ===============================================================
        # res = JSON.read("src/user/export.json") 
        # pls = res["playlists"]["my"]
        # print(f"Crawed a totoal of {len(pls)} playlists")
        # print('=' * 40)
        # return

        # ===============================================================
        # db = NetEase_Mongodb.Database_Facade()
        # db.start(clear=True)
        # NetEase_Mongodb.start()               # 初始化浏览器测试平台
        # r = NetEase_Crawler.craw(505508015)   # 爬取用户界面，解析并返回字典结果
        # r = JSON.read("src/user/export.json") # 这里暂时用本地数据代替
        # NetEase_Mongodb.insert(r, 505508015)  # 把爬到的内容存进数据库
        # NetEase_Mongodb.close()               # 关闭数据库连接
        # NetEase_Crawler.close()               # 退出浏览器
        # return

def main():
    DEMO.demo_main()

if __name__ == "__main__":
    main()

