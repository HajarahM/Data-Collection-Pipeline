from time import sleep
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
driver.get("https://www.ikea.com/gb/en/cat/sofa-beds-20874/?page=9")
accept_cookies_button = driver.find_element(by=By.XPATH, value='//*[@id="onetrust-accept-btn-handler"]')
accept_cookies_button.click()
sleep(20)
print("Finding elements...")
links = []



# for i in range(3):
#     try:
#         show_more_button = driver.find_element(by=By.XPATH, value = '//div[@class="catalog-bottom-container"]' and '//*[@class="plp-btn__label"]')        
#         show_more_button.click() 
#         sleep(2)   
#     except Exception as e: 
#         print (e) 
    
sofas_list = driver.find_elements(by=By.XPATH, value='//div[@data-testid="plp-product-card"]')
for item in sofas_list:
    links.append(item.find_element(by=By.XPATH, value='.//a').get_attribute('href'))
    #move to next page

print(len(links))

#close window
driver.close()