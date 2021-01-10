
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})
chrome_options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.images': 2})
chrome_options.add_argument('--disable-dev-shm-usage')
d = webdriver.Chrome('/usr/bin/chromedriver',options=chrome_options)
d.get('https://selenium-python.readthedocs.io/locating-elements.html')
t = d.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div/div[1]/p[5]')
print(t.text)
d.get("https://linuxize.com/post/how-to-remove-symbolic-links-in-linux/")
t = d.find_element(By.XPATH, '/html/body/div[1]/main/article/div/div[2]/div[1]/div/div/div/section/div/p[15]')
print(t.text)
d.quit()