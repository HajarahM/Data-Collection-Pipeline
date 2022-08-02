import selenium
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time
import requests
import uuid6
import os
import json
import inspect



class Scraper:
    def __init__(self, homepage, acceptcookiesid, productname, producttypeurl, productid):
        """
        Description
        ----------
        Global variables repeatedly used in the methods within this 'Scraper' class.
        
        Parameters
        ----------
        Parameters passed into this class are all strings: homepage url, XPATHs to accept cookies and product (id), the product name, and the url to the product page.
        If the user wants to get all the products listed, the url to be passed has to be for the last page.        
        """
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=self.options)
        self.homepage = homepage
        self.acceptcookiesid = acceptcookiesid
        self.productname = productname
        self.producttypeurl = producttypeurl
        self.productid = productid        
        self.links = []
        self.pdt_dict = {'SysUID': [], 'ProductID': [], 'Link': [], 'Brand': [], 'Description': [], 'Price': [], 'Imagelink': []}

    def createFolder(self, directory):
        """ 
        Description
        -----------
        Creates a new folder in the specified directory if it doesn't already exist. Incase of an OS-Error, an error message is printed out.
        
        Parameters
        ----------
        directory: the path to the directory where the new file is to be saved. "./" being the current folder of the python file.
        
        Returns
        -------
        File is created, no return value.
        """
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            print ('Error: Creating directory. ' +  directory)

    def launch_homepage(self):
        """ 
        Description
        -----------
        Launches the homepage specified when this class is called - named in the __init__ method
        
        Parameters
        ----------
        homepage: the homepage URL of the website
        
        Returns
        -------
        File is created, no return value.
        """
        self.driver.get(self.homepage)

    def max_window(self):
        """ 
        Description
        -----------
        Maximizes the window of the page that has been opened to fit the screen.
        
        Parameters and Returns
        ----------
        No input parameters, no returns
        """
        self.driver.maximize_window()
    
    def accept_cookies(self):
        """ 
        Description
        -----------
        Method to bypass cookies if there is an 'accept cookies' button.
        
        Parameters
        ----------
        acceptcookiesid: XPATH of the 'accept cookies' button to be specified when this class is called - named in the __init__ method
        
        Returns
        -------
        'accept cookies' button is clicked, no return value.
        """
        try:
            accept_cookies_button = self.driver.find_element(by=By.XPATH, value=self.acceptcookiesid)
            accept_cookies_button.click() 
        except:
            pass # If there is no cookies button, we won't find it, so we can pass

    def scroll_down(self):
        """ 
        Description
        -----------
        Scroll down to the bottom of the page that has been opened and waits for 2 seconds for loading of data and images on the page.
        
        Parameters and Returns
        ----------
        No input parameters, no return
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
        producttypeurl: url to the list of products you want to fetch specified when this class is called - named in the __init__ method
        productid: XPATH of container identifier used by website common to each product
        productname: name of product specified when this class is called - named in the __init__ method
        
        Returns
        -------
        self.links[]: A list of links to each of the product pages
        """
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
        """ 
        Description
        -----------
        Uses the "createFolder()" function to create the main folder named 'raw_data' in which the product libraries will be saved.
        
        Parameters
        ----------
        directory: the path to the directory where the new file is to be saved (in this case to be saved as "./raw_data/"). "./" being the current folder of the python file.
        
        Returns
        -------
        No return value.
        """        
        self.createFolder('./raw_data/') #create raw_data folder and product folder
        
    def get_pdtrefid(self, link): #get pdt number from website
        """ 
        Description
        -----------
        Obtain Product Reference ID (pdtrefid) from the link that has been fetched and saved into the self.links list
        
        Parameters
        ----------
        link: product link url from the self.links list
               
        Returns
        -------
        pdtrefid: int, Product Reference ID to be used as identifier from website - file name for each product - to avoid future duplication of downloads
        """   
        pdtrefid = link[link.rindex('-')+1:].strip('/')   
        return pdtrefid

    def create_pdtfolder(self, link):   # create folder with pdt number      
        """ 
        Description
        -----------
        Uses the "createFolder()" function to create the individual product folders named with the product number obtained from the "get_pdtrefid" function for specified link
        
        Parameters
        ----------
        link: product link url from the self.links list
        pdtrefid: the product id returned by the "get_pdtrefid()" function
        
        Returns
        -------
        No return value, product folder is created and named with the product number
        """ 
        pdtrefid = self.get_pdtrefid(link)
        self.createFolder(f'./raw_data/{pdtrefid}/')
              
    def generate_UUID(self):
        """ 
        Description
        -----------
        Locally generate a unique universal/global indentifier for each product
        
        Parameters
        ----------
        No input parameters
               
        Yields
        -------
        uuid: hex int, unique universal ID is generated
        """   
        uuid = uuid6.uuid7().hex
        return uuid

    def get_text(self, link): 
        """ 
        Description
        -----------
        Method to extract data that identifies each specific product from product page
        
        Parameters
        ----------
        link: product link url from the self.links list to product page
                
        Returns
        -------
        brand: brand of the product
        pdtdescription: brief description of the product
        pdtprice: Price of product in '£'
        currency: the currency was commented out due to failure to identify the respective unique XPATH
        """     
        self.driver.get(link) 
        time.sleep(0.5)          
        #extract all text per product page
        self.brand = self.driver.find_element(by=By.XPATH, value='//span[@class="pip-header-section__title--big notranslate"]').text            
        self.pdtdescription = self.driver.find_element(by=By.XPATH, value='//span[@class="pip-header-section__description-text"]').text                 
        self.pdtprice = self.driver.find_element(by=By.XPATH, value='//span[@class="pip-price__integer"]').text 
        # self.currency = self.driver.find_element(by=By.XPATH, value='//span[@class="pip-price__currency-symbol pip-price__currency-symbol--leading \n\t pip-price__currency-symbol--superscript"]').text       
        
    def get_image_source(self, link):
        """ 
        Description
        -----------
        Method to extract the image link (url) of each specific product from product page
        
        Parameters
        ----------
        link: product link url from the self.links list to product page
                
        Returns
        -------
        image_src: url to the image of the product
        """
        self.driver.get(link)
        time.sleep(0.5)
        image_src = self.driver.find_element(by=By.XPATH, value='//img[@class="pip-aspect-ratio-image__image"]').get_attribute('src')
        return image_src
        
    def download_image(self, link):   
        """ 
        Description
        -----------
        Method to download the image of each specific product from product page using the link returned by the "get_image_source" method/function
        
        Parameters
        ----------
        link: product link url from the self.links list to product page
        get_image_source(): method/function that returns the image url
                
        Returns
        -------
        retrieved_image: image of specific product
        """
        image_link = self.get_image_source(link)     
        retrieved_image = requests.get(image_link).content        
        return retrieved_image

    def update_pdt_dict(self, link):
        """ 
        Description
        -----------
        Method to update the product dictionary list (self.pdt_dict[]) with UUID, image url, product ID, link to product page, and product text (brand, description and price)
        
        Parameters
        ----------
        link: product link url from the self.links list to product page
        generate_UUID(): method that returns unique locally-generated product ID
        get_image_source(): method/function that returns the image url
        get_pdtrefid(): methods/function that returns the product ID assigned by the website
        self.pdt_dict[]: product dictionary list
                
        Returns
        -------
        self.pdt_dict[]: updated product dictionary list
        """
        uuid = self.generate_UUID()
        image_link = self.get_image_source(link) 
        pdtrefid = self.get_pdtrefid(link)
        self.pdt_dict['SysUID'].append(uuid) 
        self.pdt_dict['ProductID'].append(pdtrefid)             
        self.pdt_dict['Link'].append(link) 
        self.pdt_dict['Brand'].append(self.brand) 
        self.pdt_dict['Description'].append(self.pdtdescription)  
        self.pdt_dict['Price'].append(self.pdtprice)
        self.pdt_dict['Imagelink'].append(image_link)                              
        
    def save_locally(self, link): 
        """ 
        Description
        -----------
        Creates product folder locally into the raw-data and saves in it the updated product dictionary. 
        Then creates a subfolder for images where it saves the downloaded product image.
        
        Parameters
        ----------
        link: product link url from the self.links list
        pdtrefid: the product id returned by the "get_pdtrefid()" function
        retrieved_image: the retrieved image returned by the "download_image()" function
        
        Returns
        -------
        No return value, images folder is created within product folder and product image saved; product dictionary is saved into a data.json file in the product folder.
        """ 
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
        """ 
        Description
        -----------
        Main method that puts all steps together to make/compile product files by looping through each link in the self.links list and performing the respective actions below for each link.
        
        Parameters
        ----------
        link: product link url from the self.links list
        create_pdtfolder(): create each product folder with product website-reference ID as it's name
        get_text(): get the data of specific product from product page
        update_pdt_dict(): update product dictionary list
        save_locally(): save product data and images locally
        
        Returns
        -------
        No return value, product folder created and saved with respective data and images
        """
        for link in self.links:
            self.create_pdtfolder(link)
            self.get_text(link)
            self.update_pdt_dict(link)
            self.save_locally(link)
        return
                
    def close_window(self):
        """ 
        Description
        -----------
        Closes the webpage and browser
        
        Parameters and Returns
        ----------
        No input parameters, no return
        """
        self.driver.close()

    def stop_running(self):
        """ 
        Description
        -----------
        Quits the driver to stop running
        
        Parameters and Returns
        ----------
        No input parameters, no return
        """
        self.driver.quit()   

def fetch():
    """ 
    Description
    -----------
    Main function that takes in all inputs and runs scraper class methods
        
    Parameters
    ----------
    homepage: input of homepage url
    productname: string, name of product
    acceptcookiesid: XPATH to accept cookies button
    producttypeurl: url of the specific product type of the products to be downloaded
    productid:  XPATH of the products to be downloaded
    bot: Scraper class with all input parameters
        
    Returns
    -------
    No return value.
    """
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

print(inspect.getdoc())