from itertools import product
import selenium
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from time import sleep

class Scraper:
    def __init__(self, homepage, acceptcookiesid, productname, producttypeurl, productid):
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=self.options)
        self.homepage = homepage
        self.acceptcookiesid = acceptcookiesid
        self.productname = productname
        self.producttypeurl = producttypeurl
        self.productid = productid

    def launch_homepage(self):
        self.driver.get(self.homepage)

    def max_window(self):
        self.driver.maximize_window()
    
    def accept_cookies(self):
        accept_cookies_button = self.driver.find_element(by=By.XPATH, value=self.acceptcookiesid)
        accept_cookies_button.click() 

    def fetch_product_links(self):
        self.driver.get(self.producttypeurl)
        self.accept_cookies()
        sleep(20)
        print("Fetching links...")
        links = []
        product_list = self.driver.find_elements(by=By.XPATH, value=self.productid)
        for item in product_list:
            links.append(item.find_element(by=By.XPATH, value='.//a').get_attribute('href'))
        # print(len(links)) 
        print(f'{len(links)} product links stored in {self.productname} list')
        # print(links)

    def close_window(self):
        self.driver.close()

def fetch():
    #inputs
    homepage = "https://www.ikea.com"
    acceptcookiesid = '//*[@id="onetrust-accept-btn-handler"]'
    productname = "sofa-beds"
    producttypeurl = "https://www.ikea.com/gb/en/cat/sofa-beds-20874/?page=9"
    productid = '//div[@data-testid="plp-product-card"]'
    
    bot = Scraper(homepage, acceptcookiesid, productname, producttypeurl, productid)

    #actions
    bot.launch_homepage()
    bot.max_window()
    bot.accept_cookies()
    bot.fetch_product_links()
    bot.close_window()
    
if __name__ == "__main__":
    fetch()