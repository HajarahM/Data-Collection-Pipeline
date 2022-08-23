import time
import requests
import uuid6
import os
import json
import inspect
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class Scrape:
    def __init__(self, productname):
        """
        Description
        ----------
        Global variables repeatedly used in the methods within this 'Scraper' class.
        
        Parameters
        ----------
        productname: str, product to be searched on ikea website and scraped     
        """
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.options.add_argument("--headless") # comment out if you want to see the browser while scraping
        self.driver = webdriver.Chrome(options=self.options)
        self.homepage = "https://www.ikea.com"
        self.acceptcookiesid = '//*[@id="onetrust-accept-btn-handler"]'
        self.productname = productname         
        self.ikea_db_dict = [] # database of dictionaries     

    def _createFolder(self, directory):
        """ 
        Description
        -----------
        Creates a new folder in the specified directory if it doesn't already exist. Incase of an OS-Error, an error message is printed out.
        
        Parameters
        ----------
        directory: str, the path to the directory where the new file is to be saved. "./" being the current folder of the python file.
        """
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            print ('Error: Creating directory. ' +  directory)

    def launch_homepage(self): #search page
        """ 
        Description
        -----------
        Launches the homepage (of ikea) specified in the __init__ method, maximizes the wondow, and clicks on "go-shopping" and goes to the 'shopping' page
        
        Parameters
        ----------
        homepage: str, homepage of website
        """
        self.driver.get(self.homepage)
        self.driver.maximize_window()
        time.sleep(0.5)
        go_shopping_button = self.driver.find_element(by=By.XPATH, value='.//*[@class="website-link svelte-bdk5aj"]').get_attribute('href')
        self.driver.get(go_shopping_button)
        time.sleep(1)
     
    def _accept_cookies(self):
        """ 
        Description
        -----------
        Method to bypass cookies if there is an 'accept cookies' button.
        """
        
        try:
            accept_cookies_button = self.driver.find_element(by=By.XPATH, value=self.acceptcookiesid)
            accept_cookies_button.click() 
        except:
            pass # If there is no cookies button, we won't find it, so we can pass

    def _search_product(self):
        """ 
        Description
        -----------
        Method to search for product.
        Returns
        ------
        producttypeurl:  str, the url of the results page sorted by best-match                 
        """
        search = self.driver.find_element(by=By.XPATH, value='.//input[@class="search-field__input"]')
        search.send_keys(self.productname, Keys.RETURN)        
        time.sleep(5)
        producttypeurl = self.driver.current_url
        print (producttypeurl)
        return producttypeurl

    def _scroll_down(self):
        """ 
        Description
        -----------
        Scroll down to the bottom of the page that has been opened and waits for 2 seconds for loading of data and images on the page.        
        """
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(2)
    
    def get_links(self):
        """ 
        Description
        -----------
        Method to get all the links of the products listed on the specified product-type page (producttypeurl).
        
        Parameters
        ----------
        producttypeurl, srt: url to the list of products that have been searched
        productid: str, XPATH of container identifier used by website common to each product
        productname: str, name of product specified when this class is called - named in the __init__ method
        
        Returns
        -------
        links[]: list, A list of links to each of the product pages
        """
        self._accept_cookies()
        self.driver.get(self._search_product())
        print("Loading all images...")        
        time.sleep(7)
        self._scroll_down()
        print("Fetching links...")        
        links = []
        product_list = self.driver.find_elements(by=By.XPATH, value='//*[@class="serp-grid__item search-grid__item product-fragment"]')
        for item in product_list:
            # get links
            a_tag = item.find_element(by=By.XPATH, value='.//a')
            link = a_tag.get_attribute('href')
            links.append(link)                          
        print(f'The top {len(links)} items of {self.productname} have been found')
        return links
               
    def __get_pdtrefid(self, link): #get pdt number from website
        """ 
        Description
        -----------
        Obtain Product Reference ID (pdtrefid) from the link that has been fetched and saved into the 'links' list
        
        Parameters
        ----------
        link: str, product link url from the 'links' list
               
        Returns
        -------
        pdtrefid: int, Product Reference ID to be used as identifier from website - file name for each product - to avoid future duplication of downloads
        """   
        pdtrefid = link[link.rindex('-')+1:].strip('/')   
        return pdtrefid

    def __create_pdtfolder(self, link):   # create folder with pdt number      
        """ 
        Description
        -----------
        Uses the "createFolder()" function to create the individual product folders named with the product number obtained from the "get_pdtrefid" function for specified link
        
        Parameters
        ----------
        link: str, product link url from the 'links' list
        pdtrefid: int, the product id returned by the "get_pdtrefid()" function        
        """ 
        pdtrefid = self.__get_pdtrefid(link)
        self._createFolder(f'./raw_data/{pdtrefid}/')    
    
    def _get_data(self, link): 
        """ 
        Description
        -----------
        Method to extract data that identifies each specific product from product page
        
        Parameters
        ----------
        link: str, product link url from the 'links' list to product page        
        brand: str, brand of the product
        pdtdescription: str, brief description of the product
        pdtprice: int, Price of product in '£'
        currency: str, the currency was commented out due to failure to identify the respective unique XPATH
        """     
        self.driver.get(link) 
        time.sleep(0.5)          
        #extract all text per product page
        self.brand = self.driver.find_element(by=By.XPATH, value='//span[@class="pip-header-section__title--big notranslate"]').text            
        self.pdtdescription = self.driver.find_element(by=By.XPATH, value='//span[@class="pip-header-section__description-text"]').text                 
        self.pdtprice = self.driver.find_element(by=By.XPATH, value='//span[@class="pip-price__integer"]').text 
        # self.currency = self.driver.find_element(by=By.XPATH, value='//span[@class="pip-price__currency-symbol pip-price__currency-symbol--leading \n\t pip-price__currency-symbol--superscript"]').text       
        
    def __get_image_source(self, link):
        """ 
        Description
        -----------
        Method to extract the image link (url) of each specific product from product page
        
        Parameters
        ----------
        link: str: product link url from the 'links' list to product page
                
        Returns
        -------
        image_src: str: url to the image of the product
        """
        self.driver.get(link)
        time.sleep(0.5)
        image_src = self.driver.find_element(by=By.XPATH, value='//img[@class="pip-aspect-ratio-image__image"]').get_attribute('src')
        return image_src
        
    def __download_image(self, link):   
        """ 
        Description
        -----------
        Method to download the image of each specific product from product page using the link returned by the "get_image_source" method/function
        
        Parameters
        ----------
        link: product link url from the 'links' list to product page
        get_image_source(): method/function that returns the image url
                
        Returns
        -------
        retrieved_image: image of specific product
        """
        image_link = self.__get_image_source(link)     
        retrieved_image = requests.get(image_link).content        
        return retrieved_image

    def _update_pdt_dict(self, link):
        """ 
        Description
        -----------
        Method to update the product dictionary list (self.pdt_dict[]) with UUID, image url, product ID, link to product page, and product text (brand, description and price)
        
        Parameters
        ----------
        link: str, product link url from the 'links' list to product page
        
        Returns
        -------
        pdt_dict[]: list, updated product dictionary list
        """
        pdt_dict = {'SysUID': "", 'ProductID': "", 'Link': "", 'Brand': "", 'Description': "", 'Price': "", 'Imagelink': ""}
        uuid = uuid6.uuid7().hex # generate UUID (unique universal ID)
        image_link = self.__get_image_source(link) 
        pdtrefid = self.__get_pdtrefid(link)
        pdt_dict['SysUID'] = uuid 
        pdt_dict['ProductID'] = pdtrefid       
        pdt_dict['Link'] = link 
        pdt_dict['Brand'] = self.brand
        pdt_dict['Description'] = self.pdtdescription
        pdt_dict['Price'] = self.pdtprice
        pdt_dict['Imagelink'] = image_link

        self.ikea_db_dict.append(pdt_dict)

        return pdt_dict                          
        
    def _save_locally(self, link): 
        """ 
        Description
        -----------
        Creates product folder locally into the raw-data and saves in it the updated product dictionary. 
        Then creates a subfolder for images where it saves the downloaded product image.
        
        Parameters
        ----------
        link: product link url from the 'links' list      
        """ 
        #save image         
        retrieved_image=self.__download_image(link)  
        pdtrefid = self.__get_pdtrefid(link)
        self._createFolder(f'./raw_data/{pdtrefid}/images') 
        with open(f'./raw_data/{pdtrefid}/images/{pdtrefid}.jpg', 'wb') as outimage:
            outimage.write(retrieved_image)

        #create and save into data.json file
        pdt_dict = self._update_pdt_dict(link)  
        with open(f'./raw_data/{pdtrefid}/data.json', 'w') as data:
            json.dump(pdt_dict, data, indent=4)

        #save into Ikea products local database with list of product dictionaries          
        with open(f'./raw_data/ikeadata.json', 'w') as data:
            json.dump(self.ikea_db_dict, data, indent=4)                

    def make_pdtfiles(self, directory, product_links): 
        """ 
        Description
        -----------
        Main method that puts all steps together to make/compile product files by creating the main folder(raw-data)
        and looping through each link in the 'links' list and performing the respective actions below for each link.       
        """
        print("Saving data into files ...")
        self._createFolder(directory)         
        for link in product_links:
            self.__create_pdtfolder(link)
            self._get_data(link)            
            self._save_locally(link)   
        return self.ikea_db_dict        
    
    def fetch(self):
        """ 
        Description
        -----------
        Main function that takes in product name to be searched and runs scraper class methods
            
        Parameters
        ----------
        homepage: input of homepage url
        productname: str
                        name of product    
        """           
        start_time = time.time()        
        self.launch_homepage()      
        product_links=self.get_links()
        self.make_pdtfiles('./raw_data/', product_links)    
        self.stop_running()
        print("Your product files have been saved in the raw-data folder")
        print(f"It took ", (time.time() - start_time), " seconds to scrape the best-matched products of your search")
        return self.ikea_db_dict

    def stop_running(self):
        """ 
        Description
        -----------
        Closes the webpage and quits browser
        """
        self.driver.close()
        self.driver.quit()   
       
if __name__ == "__main__":
    bot = Scrape('chair')
    bot.fetch()

# print(inspect.getdoc())