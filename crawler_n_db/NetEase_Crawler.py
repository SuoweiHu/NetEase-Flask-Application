# @ Author: Suowei Hu
# @ Date: 2020.12.16
# @ Comment: demo
from os import abort
import sys
sys.path.append("../")

from file_utils import JSON,HTML                         # 文件导入导出
import sys                                               # 加载编码格式，命令行入参
# import os                                                # 为了删除文件
import time                                              # 设置强制延迟
import requests                                          # 网页请求
import json                                              # 导出数据字段为JSON文件
from bs4 import BeautifulSoup                            # 网页解析
from selenium import webdriver                           # Chrome浏览器驱动
from selenium.webdriver.common.keys import Keys          # 键盘输入/快捷键输入
from selenium.webdriver.chrome.options import Options    # 浏览器设置（设置无洁面浏览器，不加载图片）
# from requests_testadapter import Resp                    # 读取本地HTML文件
# from selenium.webdriver.phantomjs.options import Options # PhantomJS自动化无界面浏览器


class Crawler_Utils:
    LOGIN_INFO={
        'act' : 'account',
        'pad' : 'password'}

    URL_DICT={                                          
        "login": "https://music.163.com/",              # Example URLS
        "user" : "https://music.163.com/#/user/home",   # https://music.163.com/#/user/home?id=505508015
        "playlist" : "https://music.163.com/#/playlist",# https://music.163.com/#/playlist?id=5375119825
        "song" : "https://music.163.com/#/song"}        # https://music.163.com/#/song?id=1350330823

    DEP_PATH={
        "webdriver" : 
        {
            "chrome"    : "chromedriver/87_0_4280_88",  # Chrome Version 87.0.4280.88 (Official Build) (x86_64)
            "phantomjs" : "phantomjs/bin/phantomjs"     # Phatomjs Version: ?
        }}

    FILE_PATH={
        "user"      : "src/user/",
        "playlist"  : "src/playlist/",
        "song"      : "src/song/"}
    

class Driver_Facade:
    def __init__(self):
        return

    def start(self, headless = False):
        chrome_options = Options()
        chrome_dvrPath = Crawler_Utils.DEP_PATH['webdriver']['chrome']

        if(headless):
            # chrome_options.add_argument('--no-sandbox')                       #解决DevToolsActivePort文件不存在的报错
            chrome_options.add_argument('window-size=1920x3000')                #指定浏览器分辨率 (无界面模式下默认不是全屏，所以需要设置一下分辨率)
            chrome_options.add_argument('--disable-gpu')                        #谷歌文档提到需要加上这个属性来规避bug
            chrome_options.add_argument('--hide-scroll_till_bottombars')                    #隐藏滚动条, 应对一些特殊页面
            chrome_options.add_argument('blink-settings=imagesEnabled=false')   #不加载图片, 提升速度
            chrome_options.add_argument('--headless')                           #浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
            # chrome_options.binary_location = r“PATH"                          #手动指定使用的浏览器位置
            # driver = webdriver.Chrome(executable_path = chrome_dvrPath, options = chrome_options)
            self.driver = webdriver.Chrome(options = chrome_options)

            headless_mode = '1' if headless else '0'
            print(f"\t* WebDriver:")
            print(f"\t* Started chrome webdriver, version 87_0_4280_88")
            print(f"\t* Headless state: {headless_mode}")
            print()

            return 
            
        else:
            # driver = webdriver.Chrome(executable_path = chrome_dvrPath, options = chrome_options)
            self.driver = webdriver.Chrome(options = chrome_options)
            return

    def close(self):
        self.driver.close()
        self.driver.quit()
        self.driver = None

        print(f"\t* WebDriver:")
        print(f"\t* Stopped chrome webdriver, version 87_0_4280_88")
        print(f"\t* (self.driver = None)")
        print()

        return

class Parser:
    def __init__(self, crawler_facade):
        self.crawler = crawler_facade
        return 

    def parse_songPage(self, page_source,id=0):
        # ========================================
        # 歌曲的解析为第一个尝试所以可能不会这么规范
        # 如果要找模版写HTML解析请看用户和歌单的页面的解析
        # ========================================

        soup = BeautifulSoup(page_source, "lxml")
        for br in soup.find_all("br"):
            br.replace_with("\n")
        sid = id
        singer  = soup.find_all('a',class_='s-fc7')[1].text
        album   = soup.find_all('a',class_='s-fc7')[2].text
        info_   = soup.find_all('div',class_='cnt')[0]
        name    = info_.find_all('div')[0].text
        lyrics    = (info_.find_all('div')[4]).text
        lyrics_line = lyrics.strip().split('\n')
        lyrics_line = lyrics_line[:-2]
        if(lyrics_line==["播放","","","收藏","","分享"]): lyrics_line=[]

        result_dict = {
            "id" : sid,
            "name" : name.replace("\n",""),
            "singer" : singer,
            "album" : album,
            "lyrics" : lyrics_line
        }    
        # print(result_dict)

        return result_dict

    def parse_playlistPage(self, page_source,id=0,recursive=False,recur_limit=5):
        soup = BeautifulSoup(page_source, 'lxml')
        table_element = soup.find('table', class_="m-table")
        tableBody_element = table_element.find('tbody')
        tableRow_elements = tableBody_element.find_all('tr')
        user_element = soup.find('div',class_="user f-cb")

        # 字典存储结果
        result_dict = {"meta" : {"count" : 0, "start" : 1, "end":1}, "playlist":{}}
        
        # 获取用户信息（创建歌单的用户）
        icon_element = user_element.find('a')
        link = icon_element["href"]
        icon = user_element.img["src"]
        name_element = user_element.find('span')
        name = name_element.a.text
        time_element = user_element.find_all('span')[1]
        time = time_element.text

        creator_info = {
            'name' : name,
            'time' : time[:10],
            'link' : link,
            'icon' : icon
        }
        result_dict["creator"] = creator_info

        # 循环行获取曲目信息保存
        for row in tableRow_elements:
            rowCells_elements = row.find_all('td')  # 使用TD标签分割
            cell_1 = rowCells_elements[0]           # Song ordering
            cell_2 = rowCells_elements[1]           # Song name / link / id
            cell_3 = rowCells_elements[2]           # Time Span
            cell_4 = rowCells_elements[3]           # Author / Singer / Artist 
            cell_5 = rowCells_elements[4]           # Album

            ordering    = cell_1('span')[1].text    # -
            song_name   = cell_2.a.b["title"]       # -
            song_name = "".join(song_name.split())
            song_href   = cell_2.a["href"]          # -
            time        = cell_3.span.text
            singer      = cell_4.div["title"]       # -
            singer = "".join(singer.split())
            singer_href = ""
            # if (cell_4.a is None):
            #     singer_href = ""
            # else:
            #     singer_href = cell_4.a["href"]
            album       = cell_5.a["title"]         # -
            album = "".join(album.split())
            album_href  = cell_5.a["href"]          # -

            # print("=" * 10)
            # print("ordering: \n\t" + str(ordering))
            # print("song_name: \n\t" + str(song_name))
            # print("song_href: \n\t" + str(song_href))
            # print("time: \n\t" + str(time))
            # print("singer: \n\t" + str(singer))
            # print("singer_href: \n\t" + str(singer_href))
            # print("album: \n\t" + str(album))
            # print("album_href: \n\t" + str(album_href))

            if(recursive and recur_limit>0 and song_href!=""):
                song_id   = song_href[9:]
                sond_text = self.crawler.craw_songPage(song_id)
                song_dict = self.parse_songPage(sond_text)
                recur_limit-=1
            else:
                song_dict = "Recursive Disabled"

            temp_dict = {
                "name" : song_name,
                "href" : song_href,
                "time" : time,
                "singer" : {"name" : singer, "href" : singer_href},
                "album"  : {"name" : album, "href" : album_href},
                'detail' : song_dict
            }
            result_dict["playlist"][ordering] = temp_dict

        # 整理返回结果
        result_dict["meta"]["count"] = len(result_dict["playlist"])
        keys_order = list(result_dict["playlist"].keys())
        result_dict["meta"]["start"] = keys_order[0]
        result_dict["meta"]["end"]   = keys_order[-1]

        # 返回结果
        # print(result_dict)
        return result_dict

    def parse_userPage(self, page_source,id=0,recursive=False,recur_limit=5):
        # page_source.replace("::marker","")
        soup = BeautifulSoup(page_source, 'lxml')

        # （先处理个人信息栏）
        # 将元素分割成小的Wrapper
        infoWrapper_element = soup.find('dd')
        div_1 = infoWrapper_element.findChildren('div',recursive=False)[0]
        div_2 = infoWrapper_element.findChildren('div',recursive=False)[1]
        div_3 = infoWrapper_element.findChildren('div',recursive=False)[2]
        div_4 = infoWrapper_element.findChildren('div',recursive=False)[3]
        # 提取字段
        name = div_1.h2.span.text
        intr = div_2.text
        loct = div_3('span')[0].text
        age  = div_3('span')[1].span.text
        med  = div_4.text
        # print('name: \t' + name)
        # print('intr: \t' + intr)
        # print('loct: \t' + loct)
        # print('age: \t' + age)
        # print('med: \t' + med)

        # （处理歌单信息）
        # 将元素分割成小的容器
        my_playlist_container = soup.find_all('ul', class_ = "m-cvrlst f-cb")[0]        # 我创建的歌单
        added_playlist_container = soup.find_all('ul', class_ = "m-cvrlst f-cb")[1]     # 我收藏的歌单

        # （处理我的歌单）
        covers_container = my_playlist_container.find_all('div', class_ = "u-cover u-cover-1")
        my_playlists = []
        # 提取每个播放列表的字段
        for cover in covers_container:
            title = cover.a['title']
            title = "".join(title.split())
            href  = cover.a['href']
            image = cover.img['src']
            # print('='*10)
            # print('title: \n\t' + title)
            # print('href: \n\t' + href)
            # print('image: \n\t' + image)
            if(recursive and recur_limit>0):
                playlist_id   = href[13:]
                playlist_text = self.crawler.craw_playlistPage(playlist_id)
                playlist_dict = self.parse_playlistPage(playlist_text)
                recur_limit-=1
            else:
                playlist_dict = "Recursive Disabled"
            temp_playlist = {'title':title,'cover':image,'href':href, 'detail':playlist_dict}
            my_playlists.append(temp_playlist)

        # （处理我的歌单）
        covers_container = added_playlist_container.find_all('div', class_ = "u-cover u-cover-1")
        added_playlists = []
        # 提取每个播放列表的字段
        for cover in covers_container:
            title = cover.a['title']
            title = "".join(title.split())
            href  = cover.a['href']
            image = cover.img['src']
            # print('='*10)
            # print('title: \n\t' + title)
            # print('href: \n\t' + href)
            # print('image: \n\t' + image)
            if(recursive and recur_limit>0):
                playlist_id   = href[13:]
                playlist_text = self.crawler.craw_playlistPage(playlist_id)
                playlist_dict = self.parse_playlistPage(playlist_text)
                recur_limit-=1
            else:
                playlist_dict = "Recursive Disabled"
            temp_playlist = {'title':title,'cover':image,'href':href, 'detail':playlist_dict}
            added_playlists.append(temp_playlist)

        # （整合信息）
        result_dict = {
        'name'          : name,
        'introduction'  : intr,
        'location'      : loct,
        'age'           : '年龄：'+age,
        'media'         : med,
        'playlists'     : {
            'my' : my_playlists,
            'added' : added_playlists
            }
        }
        # print("="*10)
        # print(result_dict)
        # print("="*10)

        # 返回信息
        return result_dict


class Crawler_Facade:  
    def __init__(self):
        self.login_state = False
        self.parser = Parser(self)
        return

    def login(self, account = Crawler_Utils.LOGIN_INFO['act'], password=Crawler_Utils.LOGIN_INFO['pad']):
        __driver__ = self.driverFacade.driver
        base_url = Crawler_Utils.URL_DICT["login"]
        __driver__.get(base_url)
        __driver__.implicitly_wait(5)
        time.sleep(2)
        __driver__.find_element_by_xpath('/html/body/div[1]/div[1]/div/div[1]/a').click()                               # 单击登录按钮
        # __driver__.implicitly_wait(5)
        time.sleep(2)
        __driver__.find_element_by_xpath("/html/body/div[6]/div[2]/div/div[2]/div/div[3]").click()                      # 单击其他登录方式
        __driver__.find_element_by_id('j-official-terms').click()       # 单击用户条款
        # __driver__.switch_to.frame("g_iframe")                        # 进入内联标签
        __driver__.find_element_by_xpath('/html/body/div[6]/div[2]/div/div[1]/div[1]/div[1]/div[2]/a').click()          # 单击手机登录
        input_account = __driver__.find_element_by_xpath('/html/body/div[6]/div[2]/div/div[1]/div[1]/div/div/input')    # 单击用户名框
        input_password = __driver__.find_element_by_xpath('/html/body/div[6]/div[2]/div/div[1]/div[2]/input')           # 单击密码框
        input_account.send_keys(account)     # 输入用户名
        input_password.send_keys(password)   # 输入密码
        __driver__.find_element_by_xpath("/html/body/div[6]/div[2]/div/div[1]/div[5]/a").click()                        # 单击登陆
        # __driver__.page_source                                        # 获得登陆后网页源码 
        # __driver__.close()                 # 关闭登录页面 (经过测试关闭之后SessionID就会失效)

        self.login_state = True

        return
        
    def start(self, headless=True, default_login = True):
        self.driverFacade = Driver_Facade()
        self.driverFacade.start(headless)
        if(default_login):self.login()
        return

    def close(self):
        self.driverFacade.close()
        self.driverFacade = None
        return

    def get_page_of(self,option,id): #, save_file=False, screenshot=False):
        # 浏览器驱动
        __driver__ = self.driverFacade.driver

        # 发起请求URL
        f_path     = Crawler_Utils.FILE_PATH[option]
        base_url   = Crawler_Utils.URL_DICT[option]
        get_query  = "?id=" + str(id) 
        render_url = base_url + get_query

        # 发起请求
        __driver__.get(render_url)              # WebDriver平台打开URL
        __driver__.implicitly_wait(5)           # 隐样等待加载，最多五秒
                
        # 滚动到底部（AJAX动态加载）
        # ===========================
            # Scroll method - 1 
            # __driver__.executeScript("window.scroll_till_bottomTo(0, document.body.scroll_till_bottomHeight)");

            # Scroll method - 2                  
            # html = __driver__.find_element_by_tag_name('html')
            # html.send_keys(Keys.END)

            # # Scroll method - 3
            # SCROLL_PAUSE_TIME = 0.5
            # driver = __driver__
            # # Get scroll height
            # last_height = driver.execute_script("return document.body.scrollHeight")
            # while True:
                # # Scroll down to bottom
                # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # # Wait to load page
                # time.sleep(SCROLL_PAUSE_TIME)
                # # Calculate new scroll height and compare with last scroll height
                # new_height = driver.execute_script("return document.body.scrollHeight")
                # if new_height == last_height:
                #     break
                # last_height = new_height
        # ===========================

        # 获取数据
        __driver__.switch_to.frame("g_iframe")          # 切换到搜索结果的内联标签
        response = __driver__.page_source               # 得到浏览器渲染好的HTML网页

        # 以下为 DEBUG 用
        # ===========================
            # if(screenshot):                                 # 截图（方便DEBUG查看网页是否加载完）
            #     __driver__.save_screenshot(f_path+"z.png")  
            # if(save_file):                                  # 保存HTML文件
            #     html_f_path = f_path+'temp.html'        # HTML 文件路径
            #     # os.remove(html_f_path)                # 删除已有文件
            #     with open(html_f_path,'w+') as f:       # 新建文件并写入HTML数据
            #         f.write(response)                   # (w+ 选项会覆盖已有文件)
            #         f.close()                           # 关闭文件
        # ===========================
        
        return response
    def craw_userPage(self, id):
        return self.get_page_of('user',id)
    def craw_playlistPage(self, id):
        return self.get_page_of('playlist',id)
    def craw_songPage(self, id):
        return self.get_page_of('song',id)

    def craw(self, id, recursive=True, save_json = False):
        """
        Crawler for user page, if passed parameter of retursive 
        will also get individual playlist pages archived by that user 
        """
        if(self.login_state == False):
            raise Exception("You have not logged in !")

        html_user = self.craw_userPage(id)
        parsed_user = self.parser.parse_userPage(html_user, recursive, recur_limit=sys.maxsize)
        if(save_json): JSON.save(text=parsed_user, path=Crawler_Utils.FILE_PATH['user'] + 'export.json')
        return parsed_user