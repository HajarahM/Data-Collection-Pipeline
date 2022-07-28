import selenium
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time
import requests
import uuid6
import os
import json



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
        self.links = [[], []]
        self.pdt_dict = {'SysUID': [], 'ProductID': [], 'Link': [], 'Brand': [], 'Description': [], 'Price': [], 'Imagelink': []}

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
        time.sleep(7)
        print("Fetching links...")
        self.links = []
        product_list = self.driver.find_elements(by=By.XPATH, value=self.productid)
        for item in product_list:
            # get links
            a_tag = item.find_element(by=By.XPATH, value='.//a')
            self.link = a_tag.get_attribute('href')
            self.links.append(self.link)                          
        print(f'{len(self.links)} items stored in {self.productname} list')
        # return (self.links) 
        
    def create_mainfolder(self):
        #create raw_data folder and product folder
        self.createFolder('./raw_data/')
        
    def get_pdtrefid(self, link):
        pdtrefid = link[link.rindex('-')+1:].strip('/')   
        return pdtrefid

    def create_pdtfolder(self, link):   #get pdt number from website and create folder with pdt number      
        pdtrefid = self.get_pdtrefid(link)
        self.createFolder(f'./raw_data/{pdtrefid}/')
              
    def generate_UUID(self):
        uuid = uuid6.uuid7().hex
        return uuid

    def get_text(self, link):      
        self.driver.get(link) 
        time.sleep(0.5)          
        #extract all text per product page
        self.brand = self.driver.find_element(by=By.XPATH, value='//span[@class="pip-header-section__title--big notranslate"]').text            
        self.pdtdescription = self.driver.find_element(by=By.XPATH, value='//span[@class="pip-header-section__description-text"]').text                 
        self.pdtprice = self.driver.find_element(by=By.XPATH, value='//span[@class="pip-price__integer"]').text 
        # self.currency = self.driver.find_element(by=By.XPATH, value='//span[@class="pip-price__currency-symbol pip-price__currency-symbol--leading \n\t pip-price__currency-symbol--superscript"]').text       
        
    def get_image_source(self, link):
        self.driver.get(link)
        time.sleep(0.5)
        image_src = self.driver.find_element(by=By.XPATH, value='//img[@class="pip-aspect-ratio-image__image"]').get_attribute('src')
        return image_src
        
    def download_image(self, link):   
        image_link = self.get_image_source(link)     
        retrieved_image = requests.get(image_link).content        
        return retrieved_image

    def update_pdt_dict(self, link):
        uuid = self.generate_UUID()
        image_link = self.get_image_source(link) 
        pdtrefid = self.get_pdtrefid(link)
        self.pdt_dict['SysUID'].append(uuid) 
        self.pdt_dict['ProductID'].append(pdtrefid)             
        self.pdt_dict['Imagelink'].append(image_link) 
        self.pdt_dict['Brand'].append(self.brand) 
        self.pdt_dict['Description'].append(self.pdtdescription)  
        self.pdt_dict['Price'].append(self.pdtprice)                             
        
    def save_locally(self, link): 
        #save image         
        retrieved_image=self.download_image(link)  
        pdtrefid = self.get_pdtrefid(link)
        self.createFolder(f'./raw_data/{pdtrefid}/images') 
        with open(f'./raw_data/{pdtrefid}/images/{pdtrefid}.jpg', 'wb') as outimage:
            outimage.write(retrieved_image)
        #save data
        #create and save into data.json file
        with open(f'./raw_data/{pdtrefid}/data.json', 'w') as data:
            json.dump(self.pdt_dict, data, indent=4)                        

    def make_pdtfiles(self): 
        for link in self.links:
            self.create_pdtfolder(link)
            self.get_text(link)
            self.update_pdt_dict(link)
            self.save_locally(link)
        return
                
    def close_window(self):
        self.driver.close()

    def stop_running(self):
        self.driver.quit()   

def fetch():
    #inputs
    homepage = "https://www.ikea.com"
    acceptcookiesid = '//*[@id="onetrust-accept-btn-handler"]'
    productname = "sofa-beds"
    producttypeurl = "https://www.ikea.com/gb/en/cat/sofa-beds-20874"
    productid = '//div[@data-testid="plp-product-card"]'    
    
    bot = Scraper(homepage, acceptcookiesid, productname, producttypeurl, productid)

    #actions
    bot.launch_homepage()
    bot.max_window()
    bot.accept_cookies()
    bot.scroll_down()
    bot.get_links()
    bot.create_mainfolder()
    bot.make_pdtfiles()
    bot.close_window()
    bot.stop_running()
    
if __name__ == "__main__":
    fetch()