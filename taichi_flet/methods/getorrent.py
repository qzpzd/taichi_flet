# --coding:utf-8--
from dataclasses import dataclass, field
import re
from typing import List
from urllib.parse import quote

from utils import HTMLSession
from bs4 import BeautifulSoup
import requests
from time import sleep
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Base:
    name = ""
    base_url = ""

    @classmethod
    def search(cls, keyword, page_count, fuzzy_match=False):
        raise NotImplementedError

    @classmethod
    def detail(cls, url):
        pass


@dataclass
class DataBTDetail:
    title: str  # 标题
    magnet: str  # 下载链接
    size: str  # 文件总大小
    date: str  # 更新日期
    detail_url: str = ""
    source: str = "磁力猫"


@dataclass
class DataBTDetailSubDetail:
    name: str  # 标题
    size: str  # 文件总大小
    


@dataclass
class DataBT:
    result: List[DataBTDetail] = field(default_factory=lambda: [])
    name: str = ""
    keyword: str = ""
    curr_page: int = 0
    next_page: bool = False


class BTSow(Base):
    name = "磁力猫"
    # base_url = "https://btsow.beauty/search/{keyword}/page/{page_count}"
    base_url ='https://clm.clmapp1.xyz/cllj.php?name={keyword}&sort=&page={page_count}'

    @classmethod
    def search(cls, keyword, page_count, fuzzy_match=False):
        res = DataBT(name=cls.name, keyword=keyword, curr_page=page_count)
        session = HTMLSession()
        page = session.get(cls.base_url.format(keyword=keyword, page_count=page_count))
        # print('page:',page)
        page_list = page.html.xpath('//ul[@class="pagination"]')
        if page_list:
            next_page = page_list[0].xpath('//*[@id="Search_list_wrapper"]/ul/li[4]/a')
            if next_page:
                next_page = True
            else:
                next_page = False
        else:
            next_page = False
        res.next_page = next_page

        result = page.html.xpath('//*[@id="Search_list_wrapper"]/li')
        # print(result)
        
        
        
        for x in result:
            tmp = x.xpath('//a[@class="SearchListTitle_result_title"]')[0]
            
            title1 = x.xpath('//a[@class="SearchListTitle_result_title"]/text()')
            
            title2 = x.xpath('//a[@class="SearchListTitle_result_title"]/em/text()')
            if title1==None:
                title = title2[0]
            elif len(title1)==2:
                title = title1[0] + title2[0] + title1[1] 
            elif len(title1)==2 and len(title2)==2:
                title = title1[0] + title2[0] + title1[1] + title2[0]
            else:
                title = title1[0] + title2[0]
            # print(title)
           
            # if not fuzzy_match:  # 需要精确匹配
            #     if keyword not in title:
            #         continue
            detail_url = tmp.attrs.get("href")
            
            size = str(x.xpath('//*[@class="Search_list_info"]/em[1]/text()')[0])[5:]
            # print(size)
            
            date = str(x.xpath('//*[@class="Search_list_info"]/em[2]/text()')[0])[5:]
            # print(date)
            _hash = detail_url.split("/")[-1]
            
            detali_page = session.get('https://clm.clmapp1.xyz/'+_hash)
           
            magnet = detali_page.html.xpath('//*[@id="val"]/text()')[0]
            # print(magnet)
            # magnet = "magnet:?xt=urn:btih:" + _hash + "&dn=" + quote(title[0])
            
            res.result.append(
                DataBTDetail(
                    title=title,
                    magnet=magnet,
                    size=size,
                    date=date,
                    detail_url=detail_url,
                    source=cls.name,
                )
            )
            
        return res

    @classmethod
    def detail(cls, url):
        
        res: List[DataBTDetailSubDetail] = []
        
        # 创建一个Chrome浏览器实例
        driver = webdriver.Chrome()

        try:
            # 打开网页
            driver.get("https://clm.clmapp1.xyz" + url[1:])

            # 使用JavaScript等待渲染完成
            driver.execute_script("return document.readyState == 'complete';")

            # 使用显式等待来等待元素加载完成
            wait = WebDriverWait(driver, 5)  # 增加等待时间到60秒
            wait.until(EC.presence_of_element_located((By.ID, "wjgs")))

            # 使用JavaScript获取内容
            js_script = """
            var elements = document.querySelectorAll('ul#sdsdsdsdafwe li');
            var result = [];

            for (var i = 0; i < elements.length; i++) {
                var parentElement = elements[i].querySelector('div.File_list_info');
                var name = parentElement.childNodes[0].textContent.trim();
                var sizeElement = parentElement.querySelector('div.File_btn');
                var size = sizeElement.textContent.trim();
                
                result.push(name + ' ' + size);
            }

            return result;

            """
            content = driver.execute_script(js_script)

            for line in content:
                parts = line.split()
                # print(len(parts))
                if len(parts) >= 3:
                    # 将前面的元素合并，去掉空格
                    name = " ".join(parts[:-2]).strip()
                    
                    # 倒数第二和倒数第三之间的空格保留
                    size = f"{parts[-2]} {parts[-1]}".strip()
                    
                    res.append(DataBTDetailSubDetail(name, size))
                else:
                    print(f"Skipping line: {line}")

        finally:
            # 关闭浏览器
            driver.quit()

        return res


class TorrentKitty(Base):
    name = "torrentkitty"
    url = "https://www.torrentkitty.red/"
    base_url = "https://www.torrentkitty.red/search/{keyword}/{page_count}"

    @classmethod
    def search(cls, keyword, page_count, fuzzy_match=False):
        res = DataBT(name=cls.name, keyword=keyword, curr_page=page_count)
        session = HTMLSession()

        page = session.get(cls.base_url.format(keyword=keyword, page_count=page_count))
        html = page.html
        page_list = html.xpath('//div[@class="pagination"]')
        if page_list:
            page_btn = page_list[0].xpath('//*[@id="Search_list_wrapper"]/ul/li[8]/a')
          
            if page_btn and page_btn[0].text == "首页":
                next_page = False
            else:
                next_page = True
        else:
            next_page = False
        res.next_page = next_page

        results = html.xpath('//*[@id="Search_list_wrapper"]')[1:]
        for tr in results:
            if "No result" in tr.text:
                return res
            title, size, date = tr.text.split("\n")[:3]
            magnet = tr.xpath('//*[@id="dw6b2aeb83361e8677dfa9614ef54dbf08"]')[0].attrs.get("href")
            detail_url = cls.url + tr.xpath('//a[@rel="information"]')[0].attrs.get(
                "href"
            )

            res.result.append(
                DataBTDetail(
                    title=title,
                    magnet=magnet,
                    size=size,
                    date=date,
                    detail_url=detail_url,
                    source=cls.name,
                )
            )
        return res

    @classmethod
    def detail(cls, url):
        res: List[DataBTDetailSubDetail] = []
        session = HTMLSession()
        page = session.get(url)
        detail_list = page.html.xpath('//table[@id="torrentDetail"]//tr')[1:]
        for detail in detail_list:
            name, size = detail.text.split("\n")
            res.append(DataBTDetailSubDetail(name, size))
        return res
