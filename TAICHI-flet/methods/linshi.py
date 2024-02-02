# from http import cookies
# import sys
# sys.path.append('E:\mybook\myprojects/vscode\TAICHI-flet')
# from utils import HTMLSession

# headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
#         "referer": "https://www.hifini.com/search-_E4_BD_A0_E5_A5_BD-1.htm",
#         'Cookie':'bbs_sid=h8p9t0rkcg1b3rga9ssm3b7kfi; Hm_lvt_4ab5ca5f7f036f4a4747f1836fffe6f2=1698903525; ea9e6905311b3819f7ed8ba3403d6d47=1f376e145790139b2be08f6c028a61ff; Hm_lpvt_4ab5ca5f7f036f4a4747f1836fffe6f2=1698904703; a9c155dbe55506fce02faf36e1b7736a=dfac923c2a5f2f05eccf7d007cb6d6ad; cookie_test=MOm21w_2FMORJPPeWWfMYD4smbrsE8xhNtiwgmOw8qwweTaBj_2B',
#         'Accept-Encoding':'gzip, deflate, br',
#         'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
#         'Cache-Control': 'no-cache',
#         'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
#     }

# session = HTMLSession(headers)

# url = 'https://www.hifini.com/search-_E4_BD_A0_E5_A5_BD-1-1.htm'
# res = session.post(url)
# print(res.text)
# print(res.status_code)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree

# 创建一个Chrome浏览器实例
driver = webdriver.Edge()

# 打开目标网页
driver.get("https://www.hifini.com/search-_E4_BD_A0_E5_A5_BD-1-1.htm")

# 使用显式等待等待页面加载完成
wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "media-body")))

# 获取网页内容
page_content = driver.page_source
# 打印网页内容
# 使用lxml解析页面内容
html_tree = etree.HTML(page_content)

# 使用XPath来提取所需的元素
elements = html_tree.xpath('//div[@class="media-body"]/div/a')

# 打印提取的元素
for element in elements:
    print(element.text)  # 输出元素文本内容

# 关闭浏览器实例
driver.quit()

# from msedge.selenium_tools import Edge, EdgeOptions

# options = EdgeOptions()
# options.use_chromium = True
# options.add_argument('headless')
# browser = Edge(options=options)
# browser.get('https://www.hifini.com/search-_E4_BD_A0_E5_A5_BD-1-1.htm')
# print(browser.page_source)
# body = res.page_source.html.xpath('//div[@class="media-body"]/div/a')
# print(body)
# browser.quit()


# print(browser.page_source)
# browser.close()

# import visdom
# import torch
# # 新建一个连接客户端
# # 指定env = 'test1'，默认是'main',注意在浏览器界面做环境的切换
# vis = visdom.Visdom(env='test2')
# # 绘制正弦函数
# x = torch.arange(1, 100, 0.01)
# y = torch.sin(x)
# vis.line(X=x,Y=y, win='sinx',opts={'title':'y=sin(x)'})
# # 绘制36张图片随机的彩色图片
# vis.images(torch.randn(36,3,64,64).numpy(),nrow=6, win='imgs',opts={'title':'imgs'})
