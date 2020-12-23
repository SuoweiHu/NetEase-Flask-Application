from crawler_n_db import NetEase_Crawler, NetEase_Mongodb
from file_utils   import  HTML, JSON
import flask_app

def main():
    NetEase_Crawler.start() # 初始化数据库
    NetEase_Mongodb.start() # 初始化浏览器测试平台
    # r = NetEase_Crawler.craw(505508015)  # 爬取用户界面，解析并返回字典结果
    r = JSON.read("src/user/export.json")  # 这里暂时用本地数据代替
    NetEase_Mongodb.insert(r, 505508015)   # 把爬到的内容存进数据库
    NetEase_Mongodb.close() # 关闭数据库连接
    NetEase_Crawler.close() # 退出浏览器
    return

if __name__ == "__main__":
    main()

