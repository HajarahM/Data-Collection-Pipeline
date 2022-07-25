import selenium
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)

driver.get('https://www.ikea.com/gb/en/cat/sofas-fu003/')
accept_cookies_button = driver.find_element(by=By.XPATH, value='//*[@id="onetrust-accept-btn-handler"]')
accept_cookies_button.click()
# sofas_list = driver.find_elements(by=By.XPATH, value='//div[@data-testid="plp-product-card"]')
# show_more_button = driver.find_element(by=By.XPATH, value='//*[@class="plp-btn__label"]')
# show_more_button.click()
# links = []
# for item in sofas_list:
#     links.append(item.find_element(by=By.XPATH, value='.//a').get_attribute('href'))
#     #move to next page
#     try:        
#         show_more_button.click()
#         links.append(item.find_element(by=By.XPATH, value='.//a').get_attribute('href'))
#     except:
#         pass
# print(links)

#close window
# driver.close()