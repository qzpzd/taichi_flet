import requests
from bs4 import BeautifulSoup

def get_weather_info(city):
    # 构建URL，替换province和city为实际的省份和城市名称
    url = f"http://www.weather.com.cn/weather1d/{city}.shtml"

    # 发送GET请求获取页面内容
    response = requests.get(url,headers={'Content-Type': 'text/html; charset=utf-8'})
    # 检查响应的编码方式并设置
    response.encoding = 'utf-8'

    if response.status_code == 200:
        # 使用Beautiful Soup解析页面内容
        soup = BeautifulSoup(response.text, 'html.parser')
       
        # 在网页上查找包含天气信息的元素（需要查看页面结构以确定正确的元素）
        weather_element = soup.find('div', class_='t')
        
        # print(weather_element )
        if weather_element:
            # 查找白天和夜间的天气信息
            print(weather_element.find('ul', class_='clearfix').find_all('p', class_='wea')[1])
            day_weather = weather_element.find('ul', class_='clearfix').find('p', class_='wea').text.strip()
            night_weather = weather_element.find('ul', class_='clearfix').find_all('p', class_='wea')[1].text.strip()

            # 查找白天和夜间的温度信息
            day_temperature = weather_element.find('ul', class_='clearfix').find('p', class_='tem').text.strip()
            night_temperature = weather_element.find('ul', class_='clearfix').find_all('p', class_='tem')[1].text.strip()

            # 查找白天和夜间的风速信息
            day_wind_speed = weather_element.find('ul', class_='clearfix').find('p', class_='win').find('span').text.strip()
            night_wind_speed = weather_element.find('ul', class_='clearfix').find_all('p', class_='win')[1].find('span').text.strip()
            
            # 将天气信息合并为一个字符串
            # weather_info = f"白天天气: {day_weather}\n白天温度: {day_temperature}\n白天风速: {day_wind_speed}\n夜间天气: {night_weather}\n夜间温度: {night_temperature}\n夜间风速: {night_wind_speed}"
            weather_info = {
                                "白天天气": day_weather,
                                "白天温度": day_temperature,
                                "白天风速": day_wind_speed,
                                "夜间天气": night_weather,
                                "夜间温度": night_temperature,
                                "夜间风速": night_wind_speed
                            }

            return weather_info
        else:
            return "无法获取天气信息，请检查输入的省份和城市是否正确。"
    else:
        return "无法访问网站，请检查URL是否正确。"

# 例子：获取北京市的天气信息
#province = "beijing"
#city = "101010100"  # 北京的城市代码，需要查找对应城市的代码
#result = get_weather_info(province, city)
#print(result)


