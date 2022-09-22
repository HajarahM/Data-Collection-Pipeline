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
        pdt_dict['SysUID'] = uuid 
        pdt_dict['ProductID'] = pdtrefid       
        pdt_dict['Link'] = link 
        pdt_dict['Brand'] = self.brand
        pdt_dict['Description'] = self.pdtdescription
        pdt_dict['Price'] = self.pdtprice
        pdt_dict['Imagelink'] = image_link
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
def assertIsFile(self, path):
        if not os.path.exists(path) :
            raise AssertionError("File does not exist: %s" % str(path))  
        else: print(f"{str(path)} exists") 

def test_make_pdtfiles(self):
        product_links = [
            'https://www.ikea.com/gb/en/p/kleppstad-wardrobe-with-2-doors-white-80437234/',
            'https://www.ikea.com/gb/en/p/vihals-storage-unit-white-90483268/',
            'https://www.ikea.com/gb/en/p/songesand-wardrobe-white-90347351/'
             ]
        dictionary_list = self.obj_scraper.make_pdtfiles('./raw_data/', product_links)
        self.assertIsInstance(dictionary_list, list) # list returned is in format 'list'
        self.assertEqual(len(dictionary_list), 3) # number of items returned are 3                    
        path = './raw_data/' #test if raw_data file is created/exists
        self.assertIsFile(path)
        path1 = './raw_data/ikeadata.json' #test if json file for list of dictionaries is created/exists
        self.assertIsFile(path1)
```
#### Milestone 6: Scalably Store the Data
To scalably store the data, first in AWS console, I created an S3 bucket "ikeascraper" and in RDS created a database "ikeascraper" both of which I wrote scripts to create connections and to; 
        1. Upload the raw_data folder including product images to S3 (using boto3)
        sample code below;
```python
        def upload_files(path):
                s3 = boto3.resource('s3',
                        aws_access_key_id={S3_ACCESS_KEY_ID},
                        aws_secret_access_key={S3_ACCESS_KEY})
                bucket = s3.Bucket('ikeascraper')
    
                for subdir, dirs, files in os.walk(path):
                        for file in files:
                                full_path = os.path.join(subdir, file)
                                with open(full_path, 'rb') as data:
                                        bucket.put_object(Key=full_path, Body=data)
        
                print('upload complete')
        2. Upload the products database file ikeadata.json to RDS
```python
        from sqlalchemy import create_engine
        from sqlalchemy import inspect
        import pandas as pd

        # create_engine(f"{database_type}+{db_api}://{credentials['RDS_USER']}:{credentials['RDS_PASSWORD']}@{credentials['RDS_HOST']}:{credentials['RDS_PORT']}/{credentials['RDS_DATABSE']}")
        engine = create_engine(f"postgresql+psycopg2://postgres:{RDS_PASSWORD}@{RDS_HOST}:{RDS_PORT}/ikeascraper")
        old_product_info = engine.execute('''SELECT * FROM public."productsDB"''').all()

        jsonfile = pd.read_json('./raw_data/ikeadata.json') #Read the json file which will return a dictionary
        productsDB = pd.DataFrame(jsonfile) #Convert that dictionary into a dataframe

        print(productsDB)   

        #import list from ikeascraper
        productsDB.to_sql('productsDB', engine, if_exists='append') # Use the to_sql method with pandas

        inspect(engine).get_table_names()
```
#### Milestone 7: Preventing re-scraping and getting more data
##### Checking scalability of the scraper and checking that it runs without issues
        I revised the scraper to make it more flexible by adding functionality for user to input the desired number of page search results. I then tested the scraper for different number of pages and it scraped the results irrespective of the number of pages specified.
        Sample code for number of pages:
```python        
        def _scroll_down_showmore(self, result_pages):
            for page in range(result_pages):
                show_more = self.driver.find_element(by=By.XPATH, value='//a[@class="load-more-anchor"]')
                show_more.location_once_scrolled_into_view
                show_more_button = self.driver.find_element(by=By.XPATH, value='//a[@class="show-more__button button button--secondary button--small"]')
                show_more_button.click()
                time.sleep(0.5)
```
##### Preventing Rescraping
        Functionality to prevent rescraping was implemented through the "get_product_links" method. With user input of RDS connection credentials, the function compares new scraped links to existing (old) links in the database and then only fetches links that don't already exist in the database and then saves respective data.
        Sample Code here ...
```python  
        engine = create_engine(f"postgresql+psycopg2://postgres:{RDS_PASSWORD}@{RDS_HOST}:{RDS_PORT}/ikeascraper")
        old_links = engine.execute('''SELECT "Link" FROM public."productsDB"''').all()
                
        self._accept_cookies()
        self.driver.get(self._search_product())
        print("Loading all images...")               
        self._scroll_down_showmore(number_of_pages)
        time.sleep(7)
        print("Fetching links...")        
        links = []
        product_list = self.driver.find_elements(by=By.XPATH, value='//*[@class="serp-grid__item search-grid__item product-fragment"]')
        for item in product_list:
            # get links
            a_tag = item.find_element(by=By.XPATH, value='.//a')
            link = a_tag.get_attribute('href')
            
            if link in old_links:
                pass
            else:
                links.append(link)
```
#### Milestone 8: Containerising the scraper and running it on a cloud server
##### Containerising using Docker
After testing all public methods functionality , refactoring the bode and running the scraper in headless mode, I then moved on to containerising the scraper by creating a Docker image which runs the scraper. I created a Dockerfile to build the scraper image locally, sample code below ...
```python  
        #base image
        FROM python:3.8
        # install google chrome
        #Adding trusting keys to apt for repositories, you can download and add them using the following command:
        RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
        RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
        RUN apt-get -y update
        RUN apt-get install -y google-chrome-stable
        # install chromedriver
        RUN apt-get install -yqq unzip
        RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
        RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
        # set display port to avoid crash
        ENV DISPLAY=:99
        COPY . .
        # upgrade pip
        RUN pip install --upgrade pip
        # install dependencies
        RUN pip install -r requirements.txt
        CMD ["python3","main.py"]
```
I then pushed the Docker image to my Dockerhub account for cloud storage.
##### Running Scraper on a Cloud Server using AWS EC2
To run the scraper on a cloud server, I created an EC2 instance on my AWS account. I then pulled the docker image from dockerhub on the ECS instance and raun the scraper on the EC2 instance.
NOTE: In order to run the scraper on the EC2 instance, you must setup your AWS credentials (Access Key ID and Key) on the EC2 instance after pulling the docker image.