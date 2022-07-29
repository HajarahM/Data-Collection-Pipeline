import selenium
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time
import requests
import uuid6
import os


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
        self.dict_properties = {'Link': [], 'ProductID': [], 'SysUID': [], 'Brand': [], 'Description': [], 'Price': [], 'Image': []}

    def createFolder(self, directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            print ('Error: Creating directory. ' +  directory)

    def launch_homepage(self):
        self.driver.get(self.homepage)

    def max_window(self):
        self.driver.maximize_window()
    
    def accept_cookies(self):
        try:
            accept_cookies_button = self.driver.find_element(by=By.XPATH, value=self.acceptcookiesid)
            accept_cookies_button.click() 
        except:
            pass # If there is no cookies button, we won't find it, so we can pass

    def scroll_down(self):
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(2)
    
    def get_links(self): # and website assigned product ID
        self.driver.get(self.producttypeurl)
        self.accept_cookies()
        print("Loading all images...")
        time.sleep(9)
        print("Fetching links...")
        self.links = []
        product_list = self.driver.find_elements(by=By.XPATH, value=self.productid)
        for item in product_list:
            # get links
            a_tag = item.find_element(by=By.XPATH, value='.//a')
            self.link = a_tag.get_attribute('href')
            self.dict_properties['Link'].append(self.link)            
            # and get IDs
            self.pdtrefid = item.find_element(by=By.XPATH, value=self.productrefid)
            self.dict_properties['ProductID'].append(self.pdtrefid)    
        # print(len(self.links)) 
        print(f'{len(self.links)} product links stored in {self.productname} list')
        
    # def get_pdtnumber(self):
    #     self.driver.get(self.producttypeurl)
    #     time.sleep(3)
    #     self.pdtrefid = self.driver.find_element(by=By.XPATH, value=self.productrefid)
    #     return(self.pdtrefid)

    def generate_UUID(self):
        uuid = uuid6.uuid7().hex
        return uuid

    def get_text(self):
        self.dict_properties['Link'].extend(self.get_links())
        self.driver.get(self.link)
        time.sleep(3)        
        for self.link in self.dict_properties:            
            #extract all text per product page
            self.brand = self.driver.find_element(by=By.XPATH, value='//span[@class="pip-header-section__title--big notranslate"]').text            
            self.pdtdescription = self.driver.find_element(by=By.XPATH, value='//span[@class="pip-header-section__description-text"]').text                 
            self.pdtprice = self.driver.find_element(by=By.XPATH, value='//span[@class="pip-price__integer"]').text 
            # self.currency = self.driver.find_element(by=By.XPATH, value='//span[@class="pip-price__currency-symbol pip-price__currency-symbol--leading \n\t pip-price__currency-symbol--superscript"]').text       
        return self.brand, self.pdtdescription, self.pdtprice

    def get_image_source(self):
        self.driver.get(self.link)
        time.sleep(0.5)
        image_src = self.driver.find_element(by=By.XPATH, value='//img[@class="pip-aspect-ratio-image__image"]').get_attribute('src')
        return image_src
        
    def download_images(self, image_src):   
        self.get_image_source()     
        retrieved_image = requests.get(image_src).content        
        return retrieved_image

    # #check if needed - need to revise######   
    # def get_product_images(self, i):
    #     self.all_links = self.get_links()
    #     for i, link in enumerate(self.all_links):
    #         self.get_image_source(link)
    #         self.download_images(i)
    #     self.links = []    

    def store_data(self):                     
        #call functions to get data from site              
        self.get_text()
        self.get_image_source()
        self.download_images()
        uuid = self.generate_UUID()

        #store in dictionary
        for self.link in self.dict_properties:
            
            self.dict_properties['SysUID'].append(uuid)            
            self.dict_properties['Image'].append(self.retrieved_image) 
            self.dict_properties['Brand'].append(self.brand) 
            self.dict_properties['Description'].append(self.pdtdescription)  
            self.dict_properties['Price'].append(self.pdtprice)     
        
    def save_locally(self):
        self.download_images()
        #create raw_data folder and product folder
        self.createFolder('./raw_data/')
        #create folder with the id of the product as it's name
        self.createFolder(f'./raw_data/{self.pdtrefid}/')
        for self.link in self.dict_properties:
            with open(f'./raw_data/{self.pdtrefid}/data.json', 'wb') as outimage:
                outimage.write(self.dict_properties)                        
            self.createFolder(f'./raw_data/{self.pdtrefid}/images')
            with open(f'./images/{self.pdtrefid}.jpg', 'wb') as outimage:
                outimage.write(self.retrieved_image)
                
    def close_window(self):
        self.driver.close()

    def stop_running(self):
        self.driver.quit()   

def fetch():
    #inputs
    homepage = "https://www.ikea.com"
    acceptcookiesid = '//*[@id="onetrust-accept-btn-handler"]'
    productname = "sofa-beds"
    producttypeurl = "https://www.ikea.com/gb/en/cat/sofa-beds-20874/?page=2"
    productid = '//div[@data-testid="plp-product-card"]'
    productrefid = '//div[@data-ref-id="59419227"]'
    
    bot = Scraper(homepage, acceptcookiesid, productname, producttypeurl, productid, productrefid)

    #actions
    bot.launch_homepage()
    bot.max_window()
    bot.accept_cookies()
    bot.scroll_down()
    bot.get_links()
    bot.store_data()
    bot.save_locally()
    bot.close_window()
    bot.stop_running()
    
if __name__ == "__main__":
    fetch()