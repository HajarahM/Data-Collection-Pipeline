from time import sleep
import selenium
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time
import urllib
import requests

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
print("Loading ...")
sleep(10)
driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
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

# driver.get(link)
driver.get('https://www.ikea.com/gb/en/p/hemnes-day-bed-w-3-drawers-2-mattresses-white-asvang-firm-s09428106/')
time.sleep(2)        
brand = driver.find_element(by=By.XPATH, value='//span[@class="pip-header-section__title--big notranslate"]').text
pdtdescription = driver.find_element(by=By.XPATH, value='//span[@class="pip-header-section__description-text"]').text
pdtmeasurement = driver.find_element(by=By.XPATH, value='//button[@class="pip-link-button pip-header-section__description-measurement"]').text
pdtprice = driver.find_element(by=By.XPATH, value='//span[@class="pip-price__integer"]').text
print(f"{brand}, {pdtdescription} {pdtmeasurement} at £{pdtprice}")
# currency = driver.find_element(by=By.XPATH, value='//span[@class="pip-price__currency-symbol pip-price__currency-symbol--leading pip-price__currency-symbol--superscript"]').text

image_src = driver.find_element(by=By.XPATH, value='//img[@class="pip-aspect-ratio-image__image"]').get_attribute('src')
retrieved_image = requests.get(image_src).content
with open('./images/sofa-bed.jpg', 'wb') as outimage:
    outimage.write(retrieved_image)

#close window
driver.close()