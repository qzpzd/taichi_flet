import json
import re
import time
from dataclasses import dataclass, field
from hashlib import md5
from typing import Optional, Generator, List
from urllib.parse import quote

from utils import HTMLSession

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from lxml import etree

from msedge.selenium_tools import Edge, EdgeOptions
@dataclass
class DataSong:
    photo_url: str  # 图片链接
    big_photo_url: str  # 大图链接
    music_name: str  # 歌曲名称
    singer_name: str  # 歌手名称
    music_url: Optional[str] = field(default=None)  # 音乐链接


class HIFINI:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "referer": "https://www.hifini.com",
    }
    search_url = "https://www.hifini.com/search-{target}-1-{page}.htm"
    recommend_url = "https://www.hifini.com/"
    base_url = "https://www.hifini.com/"

    @classmethod
    def search_musics(cls, target, page=1) ->  List[Generator[DataSong, None, None]]:
        result = []
        if not target:
            for music in cls.recommend_musics():
                # yield music
                result.append(music)
        else:
            session = HTMLSession(cls.headers)
            quota_target = quote(target).replace("%", "_")
            url = cls.search_url.format(target=quota_target, page=page)
            # res = session.post(url)
            #----------------------------------------------------
            #1.创建一个Chrome浏览器实例
            # driver = webdriver.Edge()
            
            
            # 确保这里的路径指向刚刚下载的msedgedriver.exe
            service = "E:\\浏览器下载文件\\edgedriver_win64\\msedgedriver.exe"
            #2.不打开浏览器
            options = EdgeOptions()
            options.use_chromium = True
            options.add_argument('headless')
            driver = Edge(executable_path=service,options=options)

            # 打开目标网页
            driver.get(url)
            # 使用显式等待等待页面加载完成
            wait = WebDriverWait(driver, 10)
            a = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "media-body")))
            # 获取网页内容
            page_content = driver.page_source
            # 使用lxml解析页面内容
            html_tree = etree.HTML(page_content)
            # 使用XPath来提取所需的元素
            body = html_tree.xpath('//div[@class="media-body"]/div/a')
            #-----------------------------------------------
            
            # if res.status_code != 200:
            #     # yield False, res.text
            #     print(False, res.text)
            # else:
            #     body = res.html.xpath('//div[@class="media-body"]/div/a')
            
            if body:
                for a in body:
                    detail_url = "https://www.hifini.com/"+a.get('href')
                    # print(detail_url)
                    detail = cls.get_detail_music(detail_url, session)
                    if not detail:
                        continue
                    else:
                        # yield DataSong(**detail)
                        result.append(DataSong(**detail))
                    
        if len(result)<8:
            page+=1
            session = HTMLSession(cls.headers)
            quota_target = quote(target).replace("%", "_")
            url = cls.search_url.format(target=quota_target, page=page)
            # res = session.post(url)
            # if res.status_code != 200:
            #     # yield False, res.text
            #     print(False, res.text)
            # else:
            #     body = res.html.xpath('//div[@class="media-body"]/div/a')
            # 创建一个Chrome浏览器实例
            options = EdgeOptions()
            options.use_chromium = True
            options.add_argument('headless')
            driver = Edge(executable_path=service,options=options)
            # 打开目标网页
            driver.get(url)
            # 使用显式等待等待页面加载完成
            wait = WebDriverWait(driver, 10)
            a = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "media-body")))
            # 获取网页内容
            page_content = driver.page_source
            # 使用lxml解析页面内容
            html_tree = etree.HTML(page_content)
            # 使用XPath来提取所需的元素
            body = html_tree.xpath('//div[@class="media-body"]/div/a')
            if body:
                for a in body:
                    detail_url = "https://www.hifini.com/"+a.get('href')
                    # print(detail_url)
                    detail = cls.get_detail_music(detail_url, session)
                    if not detail:
                        continue
                    else:
                        # yield DataSong(**detail)
                        result.append(DataSong(**detail))

        return result
    @classmethod
    def recommend_musics(cls) -> List[Generator[DataSong, None, None]]:
        session = HTMLSession(cls.headers)
        # res = session.get(cls.recommend_url)
        
        # if res.status_code != 200:
        #     yield False, res.text
        # else:
        #     body = res.html.xpath('//div[@class="media-body"]/div/a')
        #     print(body)
        # 创建一个Chrome浏览器实例
        service = "E:\\浏览器下载文件\\edgedriver_win64\\msedgedriver.exe"
        options = EdgeOptions()
        options.use_chromium = True
        options.add_argument('headless')
        driver = Edge(executable_path=service,options=options)
        # 打开目标网页
        driver.get("https://www.hifini.com/search-_E4_BD_A0_E5_A5_BD-1-1.htm")
        # 使用显式等待等待页面加载完成
        wait = WebDriverWait(driver, 10)
        a = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "media-body")))
        # 获取网页内容
        page_content = driver.page_source
        # 使用lxml解析页面内容
        html_tree = etree.HTML(page_content)
        # 使用XPath来提取所需的元素
        body = html_tree.xpath('//div[@class="media-body"]/div/a')
        if body:
            for a in body:
                # if a.absolute_links:
                detail_url = "https://www.hifini.com/"+a.get('href')
                detail = cls.get_detail_music(detail_url, session)
                if not detail:
                    continue
                else:
                    yield DataSong(**detail)

    @classmethod
    def get_detail_music(cls, url, session=None):
        if session is None:
            session = HTMLSession(cls.headers)
        result = {}
        res = session.get(url)
        aplayer = res.html.xpath('//div[@class="aplayer"]')
        if not aplayer:
            return result
        else:
            strr2 = res.text
            music_url = re.findall(" url: '(.*?)',", strr2, re.S)
            if not music_url:
                return result
            music_name = re.findall(" title: '(.*?)',", strr2, re.S)
            if not music_name:
                return result
            photo_url = re.findall(" pic: '(.*?)'", strr2, re.S)
            if not photo_url:
                return result
            singer_name = re.findall(" author:'(.*?)',", strr2, re.S)
            if not singer_name:
                return result
            # Modify photo_url and big_photo_url to ensure they end with ".jpg"
            photo_url[0] = photo_url[0].split('.jpg')[0] + '.jpg'
            print(photo_url[0])
            result.update(
                {
                    "music_url": cls.base_url + music_url[0],
                    "music_name": music_name[0],
                    "photo_url": photo_url[0],
                    "big_photo_url": photo_url[0],
                    "singer_name": singer_name[0],
                }
            )
            # print(result)
            return result


class LiuMingYe:
    headers = {
        # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        # "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        "origin": "https://tools.liumingye.cn",
    }
    search_url = "https://test.quanjian.com.cn/m/api/search"
    recommend_url = "https://test.quanjian.com.cn/m/api/home/recommend"
    base_music_url = "https://test.quanjian.com.cn/m/api/link/id/{id}/quality/128"

    @classmethod
    def search_musics(cls, target) -> Generator[DataSong, None, None]:
        if not target:
            for music in cls.recommend_musics():
                yield music
        else:
            t = time.time() * 10000
            params = {"_t": t, "type": "YQM", "text": target, "page": 1, "v": "beta"}
            tar_str = json.dumps(params)
            s = md5(tar_str.encode()).hexdigest()
            params["token"] = s
            session = HTMLSession(cls.headers)
            res = session.post(cls.search_url, data=params)
            if res.status_code != 200 or res.json()["code"] != 200:
                yield False, res.text
            else:
                for data in res.json()["data"]["list"]:
                    music_name = data["name"]
                    singer_name = data["artist"] and data["artist"][0]["name"]
                    music_id = data["id"]
                    music_url = cls.base_music_url.format(id=music_id)
                    photo_url = data["pic"].format(size=40)
                    big_photo_url = data["pic"].format(size=500)
                    yield DataSong(
                        photo_url, big_photo_url, music_name, singer_name, music_url
                    )

    @classmethod
    def recommend_musics(cls) -> List[Generator[DataSong, None, None]]:
        t = int(time.time() * 1000)
        params = {"_t": t}
        tar_str = json.dumps(params)
        s = md5(tar_str.encode()).hexdigest()
        params["token"] = s
        session = HTMLSession(cls.headers)
        # print(params)
        res = session.post(cls.recommend_url, params=params)
        if res.status_code != 200 or res.json()["code"] != 200:
            yield False, res.text
        else:
            for data in res.json()["data"]["recommendSong"]:
                music_name = data["name"]
                singer_name = data["artist"] and data["artist"][0]["name"]
                _photo_url = (
                    data.get("pic")
                    or data["album"].get("pic")
                    or "https://picsum.photos/{size}"
                )
                photo_url = _photo_url.format(size=40)
                big_photo_url = _photo_url.format(size=500)
                if "url" in data and data["url"]:
                    music_url = data["url"]
                else:
                    if "hash" in data and data["hash"]:
                        music_id = data["hash"]
                    elif "id" in data and data["id"]:
                        music_id = data["id"]
                    else:
                        continue
                    music_url = cls.base_music_url.format(id=music_id)
                yield DataSong(
                    photo_url, big_photo_url, music_name, singer_name, music_url
                )
