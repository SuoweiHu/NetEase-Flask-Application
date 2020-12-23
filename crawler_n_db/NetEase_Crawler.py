# @ Author: Suowei Hu
# @ Date: 2020.12.16
# @ Comment: demo

import sys                                              # 加载编码格式，命令行入参
import os                                               # 为了删除文件
import time                                             # 设置强制延迟
import requests                                         # 网页请求
import json                                             # 导出数据字段为JSON文件
from bs4 import BeautifulSoup                           # 网页解析
from selenium import webdriver                          # Chrome浏览器驱动
from selenium.webdriver.common.keys import Keys         # 键盘输入/快捷键输入
from selenium.webdriver.chrome.options import Options   # 浏览器设置（设置无洁面浏览器，不加载图片）
from requests_testadapter import Resp                   # 读取本地HTML文件
# from selenium.webdriver.phantomjs.options import Options  # PhantomJS自动化无界面浏览器

class LocalFileAdapter(requests.adapters.HTTPAdapter):
    def build_response_from_file(self, request):
        file_path = request.url[7:]
        with open(file_path, 'rb') as file:
            buff = bytearray(os.path.getsize(file_path))
            file.readinto(buff)
            resp = Resp(buff)
            r = self.build_response(request, resp)

            return r

    def send(self, request, stream=False, timeout=None,
             verify=True, cert=None, proxies=None):

        return self.build_response_from_file(request)

LOGIN_INFO={
    'act' : '13735502141',
    'pad' : 'husuowei200029'
}
URL_DICT={                                          
    "login": "https://music.163.com/",              # Example URLS
    "user" : "https://music.163.com/#/user/home",   # https://music.163.com/#/user/home?id=505508015
    "playlist" : "https://music.163.com/#/playlist",# https://music.163.com/#/playlist?id=5375119825
    "song" : "https://music.163.com/#/song",        # https://music.163.com/#/song?id=1350330823
}
DEP_PATH={
    "webdriver" : 
    {
        "chrome"    : "chromedriver/87_0_4280_88",  # Chrome Version 87.0.4280.88 (Official Build) (x86_64)
        "phantomjs" : "phantomjs/bin/phantomjs"     # Phatomjs Version: ?
    }
}
FILE_PATH={
    "user"      : "../src/user/",
    "playlist"  : "../src/playlist/",
    "song"      : "../src/song/"
}

def save_toJson(text, path):
    s = json.dumps(text, indent=4, ensure_ascii=False)
    with open(path, "w+") as f:
        f.write(s)
        f.close()
    f.close()

def tryOut_templateUserPage_():
    # ========== 
    # Note this is a demo function hence lots redundance functions will be kept 
    # ==========

    # url = 'https://music.163.com/#/playlist?id=5375119825'
    # url = 'https://music.163.com/#/user/home?id=505508015'
    # url = 'http://www.jsphp.net/python/show-24-270-1.html'
    # __userAgent__   = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    # __referer__     = 'https://music.163.com/'
    # __header__ = Header(__userAgent__, __referer__)

    # options = Options()
    # options.add_argument('--headless')
    # driver = webdriver.Chrome(options=options)
    # driver = webdriver.Chrome()
    driver = webdriver.Chrome(executable_path=DEP_PATH['webdriver']['chrome'])
    # driver = webdriver.PhantomJS(executable_path="phantomjs/bin/phantomjs")
    
    time.sleep(1)
    # driver.render("result.png")
    driver.get(url)
    driver.maximize_window()

    # time.sleep(seconds)                 # 强制等待：等同于C++的Yield()
    driver.implicitly_wait(3)           # 隐式等待：等待页面全部加载完就执行， 参数为最多等待时间
    # element = WebDriverWait(driver, 5, 0.5).until(EC.presence_of_element_located((By.ID, 'su')))
                                        # 显式等待：显示等待是针对某一个元素进行相关等待判定, 一共等待 5 秒钟，每 0.5s 找一次，直到通过 ID 找到

    for i in range(1, 5):
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(1)

    driver.switch_to.frame("g_iframe") # 使用GET搜索之后跳转到了新的页面，所以必须要driver.switch_to.frame

    
    # iframe = driver.find_element_by_id('auto-id-LQKx0hR1U3P1Xp5r')
    # driver.switch_to.frame(iframe)

    driver.save_screenshot("result.png")
    print(driver.page_source)

    driver.close()
    driver.quit()

def driver_factory(headless = False):
    chrome_options = Options()
    chrome_dvrPath = DEP_PATH['webdriver']['chrome']

    if(headless):
        # chrome_options.add_argument('--no-sandbox')                       #解决DevToolsActivePort文件不存在的报错
        chrome_options.add_argument('window-size=1920x3000')                #指定浏览器分辨率 (无界面模式下默认不是全屏，所以需要设置一下分辨率)
        chrome_options.add_argument('--disable-gpu')                        #谷歌文档提到需要加上这个属性来规避bug
        chrome_options.add_argument('--hide-scrollbars')                    #隐藏滚动条, 应对一些特殊页面
        chrome_options.add_argument('blink-settings=imagesEnabled=false')   #不加载图片, 提升速度
        chrome_options.add_argument('--headless')                           #浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
        # chrome_options.binary_location = r“PATH"                          #手动指定使用的浏览器位置
        # driver = webdriver.Chrome(executable_path = chrome_dvrPath, options = chrome_options)
        driver = webdriver.Chrome(options = chrome_options)
        return driver 
    else:
        # driver = webdriver.Chrome(executable_path = chrome_dvrPath, options = chrome_options)
        driver = webdriver.Chrome(options = chrome_options)
        return driver

__driver__ = driver_factory(headless = True)       # 无界面？(Headless) 

def scroll(driver, repeat = 5):
    for i in range(1, repeat):
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(1)

def perf_login():
    base_url = URL_DICT["login"]
    __driver__.get(base_url)
    __driver__.implicitly_wait(5)
    time.sleep(1)
    __driver__.find_element_by_xpath('/html/body/div[1]/div[1]/div/div[1]/a').click()                               # 单击登录按钮
    # __driver__.implicitly_wait(5)
    time.sleep(1)
    __driver__.find_element_by_xpath("/html/body/div[6]/div[2]/div/div[2]/div/div[3]").click()                      # 单击其他登录方式
    __driver__.find_element_by_id('j-official-terms').click()       # 单击用户条款
    # __driver__.switch_to.frame("g_iframe")                        # 进入内联标签
    __driver__.find_element_by_xpath('/html/body/div[6]/div[2]/div/div[1]/div[1]/div[1]/div[2]/a').click()          # 单击手机登录
    input_account = __driver__.find_element_by_xpath('/html/body/div[6]/div[2]/div/div[1]/div[1]/div/div/input')    # 单击用户名框
    input_password = __driver__.find_element_by_xpath('/html/body/div[6]/div[2]/div/div[1]/div[2]/input')           # 单击密码框
    input_account.send_keys(LOGIN_INFO['act'])                      # 输入用户名
    input_password.send_keys(LOGIN_INFO['pad'])                     # 输入密码
    __driver__.find_element_by_xpath("/html/body/div[6]/div[2]/div/div[1]/div[5]/a").click()                        # 单击登陆
    # __driver__.page_source                                        # 获得登陆后网页源码 
    # __driver__.close()                 # 关闭登录页面 (经过测试关闭之后SessionID就会失效)

def craw_page(id, option, save_file=False):
    f_path = FILE_PATH[option]
    # 发起请求URL
    base_url = URL_DICT[option]
    get_query = "?id=" + str(id) 
    render_url = base_url + get_query
    # 发起请求
    __driver__.get(render_url)              # WebDriver平台打开URL
    time.sleep(2)                           # 强制等待加载，二秒
    __driver__.implicitly_wait(5)           # 隐样等待加载，最多五秒
    # scroll(__driver__)                    # 滚动到底部（AJAX动态加载）
    __driver__.switch_to.frame("g_iframe")          # 切换到搜索结果的内联标签
    # __driver__.save_screenshot(f_path+"z.png")    # 截图（方便DEBUG查看网页是否加载完）
    response = __driver__.page_source       # 得到浏览器渲染好的HTML网页
    # __driver__.close()                    # 关闭当前网页
    html_f_path = f_path+'temp.html'        # HTML 文件路径
    # os.remove(html_f_path)                # 删除已有文件
    if(save_file):
        with open(html_f_path,'w+') as f:   # 新建文件并写入HTML数据
            f.write(response)               # (w+ 选项会覆盖已有文件)
            f.close()                       # 关闭文件
    return response

def craw_userPage(id, save_file=False):
    return craw_page(id, 'user', save_file)
    
def craw_playlistPage(id, save_file=False):
    return craw_page(id, 'playlist', save_file)

def craw_songPage(id, save_file=False):
    return craw_page(id, 'song', save_file)

def parse_songPage(page_source,id=0):
    # ========================================
    # 歌曲的解析为第一个尝试所以可能不会这么规范
    # 如果要找模版写HTML解析请看用户和歌单的页面的解析
    # ========================================

    # # 尝试从本地文件导入HTML文件
    # requests_session = requests.session()
    # requests_session.mount('file://', LocalFileAdapter())
    # requests_session.get('file://../src/demo_11/song/temp.html')
    # c = requests_session.content
    # print(page_source)

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

def parse_playlistPage(page_source,id=0,recursive=False,recur_limit=5):
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
            sond_text = craw_songPage(song_id)
            song_dict = parse_songPage(sond_text)
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

def parse_userPage(page_source,id=0,recursive=False,recur_limit=5):
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
            playlist_text = craw_playlistPage(playlist_id)
            playlist_dict = parse_playlistPage(playlist_text)
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
            playlist_text = craw_playlistPage(playlist_id)
            playlist_dict = parse_playlistPage(playlist_text)
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


def demo():
    # 是否要递归查找歌单/歌曲信息
    recursive_song   = True       # 是否为用户的歌单爬歌曲的信息
    recursive_lyrics = True       # 是否为歌单爬歌词等歌的信息
    recur_limit_song = 3         # 一个用户最多拉多少个他的歌单
    recur_limit_lyrics = 3       # 一个歌单最多拉多少个的歌词

    # 登陆以创建用户和服务器的Session
    # （生成Session可以方便以后抓全数据）
    perf_login()           # 登陆页面

    # 使用Selenium抓渲染后的HTML文件
    # （这里只是做个例子，假设所有的ID都为已知
    s_html          = False 
    html_user       = craw_userPage(505508015, s_html)      # 用户页面
    html_playlist   = craw_playlistPage(2867860282, s_html) # 歌单页面
    html_song       = craw_songPage(1445299059, s_html)     # 歌曲页面

    # 解析HTML文件，获得数据字段
    parsed_user     = parse_userPage(html_user, recursive=recursive_song,recur_limit=recur_limit_song)             # 解析用户页
    parsed_playlist = parse_playlistPage(html_playlist, recursive=recursive_lyrics,recur_limit=recur_limit_lyrics) # 解析列表页
    parsed_song     = parse_songPage(html_song)             # 解析歌曲页

    # 保存为JSON文件
    save_toJson(text = parsed_user,     path = FILE_PATH['user'] + 'export.json')
    save_toJson(text = parsed_playlist, path = FILE_PATH['playlist'] + 'export.json')
    save_toJson(text = parsed_song,     path = FILE_PATH['song'] + 'export.json')

# if __name__ == '__main__':
#     # 使用webdriver打开一个浏览器instance
#     __driver__ = driver_factory(headless = False)       # 无界面？(Headless) 
#     main()
#     # 退出浏览器，释放资源为其他活动
#     # __driver__.close()    # 关闭当前页面（因为这里只有一页所以也会推出浏览器）
#     __driver__.quit()       # 退出webdriver驱动

# ==========================================
# 以上为原 DEMO——16 （做了些小的更改）

def parse(option, page_source, recursive=False, recur_limit=0):
    if(option=='user'):         parse_userPage(page_source, recursive=recursive,recur_limit=recur_limit)
    elif(option=='playlist'):   parse_playlistPage(page_source, recursive=recursive,recur_limit=recur_limit)
    elif(option=='song'):       parse_songPage(page_source)
    return

def save(option, parsed_dict):
    save_toJson(text = parsed_dict,     path = FILE_PATH[option] + 'export.json')
    return

def craw(id):
    perf_login()                                    # 登陆页面
    html_user       = craw_userPage(id, False)      # 用户页面
    parsed_user     = parse_userPage(html_user, recursive=True,recur_limit=sys.maxsize)             # 解析用户页
    # save_toJson(text = parsed_user,     path = FILE_PATH['user'] + 'export.json')
    return parsed_user