import selenium
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)

#opening homepage 
driver.get('https://www.ikea.com')

#opening window in maximize mode
driver.maximize_window()

#accept_cookies
accept_cookies_button = driver.find_element(by=By.XPATH, value='//*[@id="onetrust-accept-btn-handler"]')
accept_cookies_button.click()

#list of links to sofas
driver.get('https://www.ikea.com/gb/en/cat/sofas-fu003/')
accept_cookies_button = driver.find_element(by=By.XPATH, value='//*[@id="onetrust-accept-btn-handler"]')
accept_cookies_button.click()
sofas_list = driver.find_elements(by=By.XPATH, value='//a[starts-with(@href,"https://www.ikea.com/gb/en/cat/sofas-fu003/")]')
links = []
for item in sofas_list:
    links.append(item.find_element(by=By.XPATH, value='.//a[starts-with(@href,"https://www.ikea.com/gb/en/cat/sofas-fu003/")]').get_attribute('href'))
    # links.append(item.find_element(by=By.XPATH, value='.//a[starts-with(@href,"https://www.ikea.com/gb/en/cat/sofas-fu003/?page=")]').get_attribute('href'))
print(links)

#close window
driver.close()

#data.json file for dictionary