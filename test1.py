import selenium
from selenium import webdriver
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

class Scraper: 
    def __init__(self):        
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=self.options)
    
    def launch_webpage(self):
        self.driver.get('https://www.ikea.com/')
        

    def close_webpage(self): 
        time.sleep(10)
        self.driver.close()
 


def navigate():
    test = Scraper()
    test.launch_webpage()
    test.close_webpage()


if __name__ == "__main__":
    navigate()