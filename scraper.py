import selenium
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time

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
        self.links = []

    def launch_homepage(self):
        self.driver.get(self.homepage)

    def max_window(self):
        self.driver.maximize_window()
    
    def accept_cookies(self):
        accept_cookies_button = self.driver.find_element(by=By.XPATH, value=self.acceptcookiesid)
        accept_cookies_button.click() 
    
    def extract_links(self):
        self.driver.get(self.producttypeurl)
        self.accept_cookies()
        print("Loading all images...")
        time.sleep(20)
        print("Fetching links...")
        self.links = []
        product_list = self.driver.find_elements(by=By.XPATH, value=self.productid)
        for item in product_list:
            self.links.append(item.find_element(by=By.XPATH, value='.//a').get_attribute('href'))
        # print(len(self.links)) 
        print(f'{len(self.links)} product links stored in {self.productname} list')
        # print(self.links)

    def get_image_source(self, link: str):
        self.driver.get(link)
        time.sleep(0.5)
        self.src = self.driver.find_element(by=By.XPATH, value='//img[@class="pip-aspect-ratio-image__image"]').get_attribute('src')

    def download_images(self, i):
        self.urllib.request.urlretrieve(self.src, f"./product/{self.productname}_{i}.jpg")

    def get_product_images(self):
        all_links = self.extract_links()
        for i, link in enumerate(all_links):
            self.get_image_source(link)
            self.download_images(i)
        self.links = []

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
    bot.extract_links()
    bot.close_window()
    
if __name__ == "__main__":
    fetch()