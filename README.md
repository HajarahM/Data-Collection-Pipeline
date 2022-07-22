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

Within this method, I used the sleep function which was critical to allowing the scraper time to list all product from the specified url and fetch respective product links.

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

