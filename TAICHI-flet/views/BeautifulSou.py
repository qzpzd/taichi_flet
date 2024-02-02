from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class YourClassName:
    @classmethod
    def detail(cls, url):
        res = []

        # 创建一个Chrome浏览器实例
        driver = webdriver.Chrome()

        try:
            # 打开网页
            driver.get("https://www.ddyueshu.com/" + url)

            # 使用显式等待来等待元素加载完成
            wait = WebDriverWait(driver, 20)  # 最长等待时间为20秒
            b_element = wait.until(EC.presence_of_element_located((By.ID, "wjgs")))

            # 获取<b>元素中的文本内容
            text_content = b_element.text
            print("文本内容:", text_content)

        finally:
            # 关闭浏览器
            driver.quit()

# 使用示例
YourClassName.detail("paihangbang")
