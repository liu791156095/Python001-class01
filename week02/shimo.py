from selenium import webdriver
import time

try:
    browser = webdriver.Chrome()
    
    browser.get('https://shimo.im/login?from=home')
    time.sleep(1)

    browser.find_element_by_xpath('//input[@name="mobileOrEmail"]').send_keys('用户名')
    browser.find_element_by_xpath('//input[@name="password"]').send_keys('密码')
    time.sleep(1)
    browser.find_element_by_xpath('//button[contains(@class,"submit")]').click()

    cookies = browser.get_cookies() # 获取cookies
    print(cookies)
    time.sleep(3)

except Exception as e:
    print(e)
finally:    
    browser.close()