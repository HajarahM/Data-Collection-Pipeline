import selenium
from selenium import webdriver
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
# import requests
import time

class Scraper: 
    def __init__(self):        
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=self.options)
        self.website = 'https://www.wegotravel.co.uk'        
        self.accept_cookies_id = "CybotCookiebotDialogBodyLevelButtonAcceptWrapper"
    
    def webpage(self):
        self.driver.get(self.website)
        

    def bypass_cookies(self):
        # list_cookies = ['<a id="CybotCookiebotDialogBodyLevelButtonAccept" href="#" tabindex="0" lang="en">OK</a>', '<div id="CybotCookiebotDialogBodyLevelButtonAcceptWrapper" style="display: block;"><a id="CybotCookiebotDialogBodyLevelButtonAccept" href="#" tabindex="0" lang="en">OK</a></div>']
        try:        
            self.driver.switch_to.frame('fc_frame') # This is the id of the frame - not yet accurate
            accept_preferences_button = self.driver.find_element(by=By.XPATH, value='//*[@id="CybotCookiebotDialogBodyLevelButtonPreferences"]')            
            accept_preferences_button.click()
            accept_cookies_button = self.driver.find_element(by=By.XPATH, value='//*[@id=f"{self.accept_cookies_id}"]')
            accept_cookies_button.click()

        except:
            pass # If there is no cookies button, we won't find it, so we can pass

    def scroll_down(self):
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    def bypass_subscription(self):
        try:            
            self.driver.switch_to.frame('webpush-onsite') # This is the id of the frame
            accept_cookies_button = self.driver.find_element(by=By.XPATH, value='//*[@id="deny"]')
            accept_cookies_button.click()

        except:
            pass # If there is no cookies button, we won't find it, so we can pass

    def close_webpage(self): 
        time.sleep(10)
        self.driver.close()

    


def navigate():
    test = Scraper()
    test.webpage()
    test.bypass_cookies()
    # test.bypass_subscription()
    # test.scroll_down()
    test.close_webpage()

if __name__ == "__main__":
    navigate()