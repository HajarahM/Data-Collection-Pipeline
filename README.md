# Data Collection Pipeline

## Virtual Environment - DCP
The virtual environment created for this project is named DCP with the following libraries installed in it: pip, ipykernel, and selenium.

## Scraper Project using Selenium
The scraper project is Project 2 or the aiCore bootcamp training with an aim to harness skills in data mining by fetching different types of data from websites, importing it into tables/dictionaries to serve data analytical purposes.

### Selected website for Project
The website I selected for this project is ikea.com specially due to the variety of it's list of products and simplicity.

## Modules Used
Imported modules include selenium, weddriver, Chrome, and time.

## Functionality

### Navigation
The Scraper has methods to launch a selected webpage, maximize the window, accept cookies (with input of specific cookies ID of the selected website), *scroll up or down, etc

### Prototypes

#### Milestone 1: Getting the individual page for each entry/product
The first prototype has the ability to fetch all the links of a specified product and stores them in a list.

Inputs to this prototype include: Url of selected website, product name, url to the listing of the product type or product and that product's reference ID.

Within this method, I used the sleep function which was critical to allowing the scraper time to list all product from the specified url and fetch respective product links as well as a method to bypass cookies incase the cookies pop-up appears.

Example Code for this prototype
```python
self.driver.get(self.producttypeurl)
    self.accept_cookies()
    sleep(20)
    print("Fetching links...")
    links = []
    product_list = self.driver.find_elements(by=By.XPATH, value=self.productid)
    for item in product_list:
        links.append(item.find_element(by=By.XPATH, value='.//a').get_attribute('href'))
    print(f'{len(links)} product links stored in {self.productname} list')        
```
#### Milestone 2 - 4: Collect Data & Images from the individual pages and save locally
I created multiple methods to navigate through the site and perform different functionalities, these include;

##### Retrieve text and image data from a single details page
The information obtained from each page includes the specific product description, price and brand/make. This is retrieved using the .text function as in the sample code below.
```python
def get_text(self, link):      
        self.driver.get(link) 
        time.sleep(0.5)          
        #extract all text per product page
        self.brand = self.driver.find_element(by=By.XPATH, value='//span[@class="pip-header-section__title--big notranslate"]').text            
        self.pdtdescription = self.driver.find_element(by=By.XPATH, value='//span[@class="pip-header-section__description-text"]').text                 
        self.pdtprice = self.driver.find_element(by=By.XPATH, value='//span[@class="pip-price__integer"]').text 

def get_image_source(self, link):
        self.driver.get(link)
        time.sleep(0.5)
        image_src = self.driver.find_element(by=By.XPATH, value='//img[@class="pip-aspect-ratio-image__image"]').get_attribute('src')
        return image_src
        
def download_image(self, link):   
    image_link = self.get_image_source(link)     
    retrieved_image = requests.get(image_link).content        
    return retrieved_image
```
##### Generating a unique ID and UUID for each product

###### Unique ID from website (Product ID)
I generated the unique ID from the website from the product links based on naming of the site, I found that the last digits after the last (-) referred to the product ID which was unique to every product and then removed the '/' that came after the ID in the url. 
Sample code below
```python
def get_pdtrefid(self, link):
        pdtrefid = link[link.rindex('-')+1:].strip('/')   
        return pdtrefid
```
###### System-generated Universally (or Globally) Unique ID (UUID)
I then wrote a method to locally generated a global User ID using python for every product.
Sample code below (with uuid6 import)
```python
def generate_UUID(self):
        uuid = uuid6.uuid7().hex
        return uuid
```
##### Storing extracted data into a dictionary
Next I wrote a method to create a dictionary for each product and then map each product feature to feature value.
Sample code below
```python
def update_pdt_dict(self, link):
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
```
##### Saving raw data and images locally
Finally I wrote a method to product folders within a main raw-data folder, saved using the product ID previously obtained from the website. Within the product folder is the product dictionary as a .json file with respective data and a subfolder for image/s.
Sample code below (with json import)
```python
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
```
#### Milestone 5: Documentation and Testing

##### Documentation
After successfully testing the functionality of the Scraper, I then moved onto documentation. I used the NumPy Docstring format, adding docstrings to all the methods, easy enough for other users to understand.

##### Unit Testing
Next I created unit test functions for the 3 public methods that make up the main functionality of the Scraper.
###### Launch_homepage
First I tested the launch_homepage method - the unittest checks for the following functionality with respective sample code;
 - if driver.get is called twice
 - if the find_element function is returning the specified xpath for the go-shopping button
 - and if time.sleep is called twice, first for 0.5seconds and next for 1sec
```python
 @patch('selenium.webdriver.remote.webdriver.WebDriver.get')
    @patch('selenium.webdriver.remote.webdriver.WebDriver.find_element')
    @patch('time.sleep')
    def test_launch_homepage(self, 
        mock_sleep: Mock,
        mock_find_element: Mock,
        mock_get: Mock
        ):

        self.obj_scraper.launch_homepage()
        # check if 'find_element' function is called with xpath
        mock_get.assert_called
        get_call_count = mock_get.call_count
        mock_find_element.assert_called_once_with(by='xpath', value='.//*[@class="website-link svelte-bdk5aj"]') # test if go-shopping button found
        mock_sleep.assert_has_calls(calls=[call(0.5), call(1)], any_order=True) # test sleep times called twice
        self.assertEqual(get_call_count, 2) # get_call called twice   
```
###### get_links
Next I tested the 'get_links' method to check whether the specified number of links on the page is returned and whether the returned object is in 'list' format
```python
def test_get_links(self):
        self.obj_scraper.launch_homepage()
        result_links = self.obj_scraper.get_links()        
        self.assertIsInstance(result_links, list) # list returned is in format 'list'
        self.assertEqual(len(result_links), 22) # number of items returned are 22
```
###### make_pdtfiles (Make Product Files)
Lastly I tested the make_pdtfiles method which is supposed to save all scapeed data and files locally. To take a quick test, I passed only 3 product links directly into the product list in the test and checked with the created list of dictionaries would contain all the 3 dictionaries and was in 'list' format. 
Next, I checked if the raw_data file was created along with the json file. Sample code below;
```python
def test_make_pdtfiles(self, mock_file: Mock):
        product_links = [
            'https://www.ikea.com/gb/en/p/kleppstad-wardrobe-with-2-doors-white-80437234/',
            'https://www.ikea.com/gb/en/p/vihals-storage-unit-white-90483268/',
            'https://www.ikea.com/gb/en/p/songesand-wardrobe-white-90347351/'
             ]
        dictionary_list = self.obj_scraper.make_pdtfiles('./raw_data/', product_links)
        self.assertIsInstance(dictionary_list, list) # list returned is in format 'list'
        self.assertEqual(len(dictionary_list), 3) # number of items returned are 3
        mock_file             
        path = pl.Path('./raw_data/') #test if raw_data file is created/exists
        self.assertIsFile(path)
        path1 = pl.Path('./raw_data/ikeadata.json')
        self.assertIsFile(path1)
```