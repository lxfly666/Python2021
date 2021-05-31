from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


# 这部分用来设置运行时不显示浏览器窗口
chrome_options = Options()
#chrome_options.add_argument("--headless")
# 模拟浏览器进行访问
browser = webdriver.Chrome(options=chrome_options)
browser.get("http://www.baidu.com")

# browser.find_element_by_id("loginName").send_keys("liuxf")
# browser.find_element_by_id("password").send_keys("988110")
time.sleep(2)

# loginButton = browser.find_element_by_xpath("//*[class='button_blue']")
# loginButton.click()



print(browser.page_source.encode('GBK', 'ignore'))
