import selenium
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time
import requests
import uuid6


class Scraper:
    def __init__(self, homepage, acceptcookiesid, productname, producttypeurl, productid, productrefid):
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=self.options)
        self.homepage = homepage
        self.acceptcookiesid = acceptcookiesid
        self.productname = productname
        self.producttypeurl = producttypeurl
        self.productid = productid
        self.productrefid = productrefid
        self.links = []    
        self.dict_properties = {'link': [], 'ProductID': [], 'SysUID': [], 'Brand': [], 'Description': [], 'Price': [], 'Image': []}

    def launch_homepage(self):
        self.driver.get(self.homepage)

    def max_window(self):
        self.driver.maximize_window()
    
    def accept_cookies(self):
        time.sleep(0.5)
        accept_cookies_button = self.driver.find_element(by=By.XPATH, value=self.acceptcookiesid)
        accept_cookies_button.click() 

    def scroll_down(self):
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(1)
    
    def get_links(self): # and website assigned product ID
        self.driver.get(self.producttypeurl)
        self.accept_cookies()
        print("Loading all images...")
        time.sleep(10)
        print("Fetching links...")
        self.links = []
        self.product_list = self.driver.find_elements(by=By.XPATH, value=self.productid)
        for item in self.product_list:
            # or self.links.append(item.find_element(by=By.XPATH, value='.//a').get_attribute('href'))  
            a_tag = item.find_element(by=By.XPATH, value='.//a')
            self.link = a_tag.get_attribute('href')
            self.links.append(self.link)
            
            # and get IDs
            self.pdtrefid = item.find_element(by=By.XPATH, value=self.productrefid)
            self.dict_properties['ProductID'].append(self.pdtrefid)    

        # print(len(self.links)) 
        print(f'{len(self.links)} product links stored in {self.productname} list')
        return self.links

    # def get_pdtnumber(self):
    #     self.driver.get(self.producttypeurl)
    #     time.sleep(3)
    #     self.pdtrefid = self.driver.find_element(by=By.XPATH, value=self.productrefid)
    #     return(self.pdtrefid)

    # def generate_UUID(self):
    #     self.uuid = uuid6.uuid7().hex
    #     return(self.uuid)

    def get_image_source(self):
        self.driver.get(self.link)
        time.sleep(0.5)
        self.image_src = self.driver.find_element(by=By.XPATH, value='//img[@class="pip-aspect-ratio-image__image"]').get_attribute('src')

    def download_images(self):
        retrieved_image = requests.get(self.image_src).content
        with open(f'./images/{self.brand}_{self.productname}.jpg', 'wb') as outimage:
            outimage.write(retrieved_image)

    #need to revise######   
    def get_product_images(self, i):
        self.all_links = self.get_links()
        for i, link in enumerate(self.all_links):
            self.get_image_source(link)
            self.download_images(i)
        self.links = []

    def get_text(self):
        self.dict_properties.extend(self.get_links())
        self.driver.get(self.link)
        time.sleep(3)        
        for self.link in self.dict_properties:
            self.dict_properties['Link'].append(self.link) 
            self.dict_properties['Image'].append(self.get_product_images()) 
            #extract all text per product page
            self.brand = self.driver.find_element(by=By.XPATH, value='//span[@class="pip-header-section__title--big notranslate"]').text
            self.dict_properties['Brand'].append(self.brand) 
            self.pdtdescription = self.driver.find_element(by=By.XPATH, value='//span[@class="pip-header-section__description-text"]').text
            self.dict_properties['Description'].append(self.pdtdescription)         
            self.pdtprice = self.driver.find_element(by=By.XPATH, value='//span[@class="pip-price__integer"]').text
            self.dict_properties['Price'].append(self.pdtprice)  
            #generate UUID
            self.uuid = uuid6.uuid7().hex
            self.dict_properties['SysUID'].append(self.uuid)  
        # print(f"{self.brand}, {self.pdtdescription} at £{self.pdtprice}")
        # self.currency = self.driver.find_element(by=By.XPATH, value='//span[@class="pip-price__currency-symbol pip-price__currency-symbol--leading \n\t pip-price__currency-symbol--superscript"]').text
            
    def store_data(self):
        self.scroll_down()
        self.get_links()
        self.get_text()
        self.get_product_images()


        
    def close_window(self):
        self.driver.close()

    def stop_running(self):
        self.driver.quit()

def fetch():
    #inputs
    homepage = "https://www.ikea.com"
    acceptcookiesid = '//*[@id="onetrust-accept-btn-handler"]'
    productname = "sofa-beds"
    producttypeurl = "https://www.ikea.com/gb/en/cat/sofa-beds-20874/?page=9"
    productid = '//div[@data-testid="plp-product-card"]'
    productrefid = '//div[@data-ref-id="59419227"]'
    
    bot = Scraper(homepage, acceptcookiesid, productname, producttypeurl, productid, productrefid)

    #actions
    bot.launch_homepage()
    bot.max_window()
    bot.accept_cookies()
    bot.store_data()
    bot.close_window()
    
if __name__ == "__main__":
    fetch()

#data.json file for dictionary
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