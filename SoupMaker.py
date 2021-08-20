# coding: utf-8
#!/usr/bin/env python

# Functions included:
# constructor: URLsoup( <link>)
# e.g. betting = URLsoup('https://bet.hkjc.com/racing/pages/odds_wp.aspx?lang=ch&date=2021-05-01&venue=S1&raceno=1')

# scraper: get_html_src(keyword = <what must appear in the html>) # saves a copy of the html source according to the provided filename in the constructor & returns a soup obj
# e.g. betting.get_html_src(keyword = 'tableContent2')

# refresh (F5): refresh_page() #refreshes page
# e.g. betting.refresh_page()

# saver: save_html(<filename>) #saves the soup object into a html file #<timestamp>_<filename>.html
# e.g. betting.save_html('trial')

# quit (Ctrl+W): quit_driver() #quits the webdriver
# e.g. betting.quit_driver()

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime

from bs4 import BeautifulSoup
from html5lib import *

import time

class URLsoup:
    def __init__(self, name, url):
        self.url = url
        self.name = name
        self.ref_count = 0
        
        print("URLsoup object intiated")
        
        print("Initialing scraping process on " + str(self.url))
        
        options = Options()
        options.headless = True    
        self.driver = webdriver.Firefox(options=options) 
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.implicitly_wait(10)
        
        #deleting cookies
        self.driver.delete_all_cookies()
        self.driver.get_cookies()
        
        #send get request
        self.driver.get(self.url)
        print("Getting html...")    
        self.soup = ''
    
    def save_html(self, name):
        today_str_formatted = datetime.now().strftime("%Y%m%d_%H%M%S") 
        goodname = today_str_formatted + "_" + name + ".html"
        
        back_up = open(goodname, "w") # paste the captured html code into the txt
        back_up.write(self.soup.prettify())
        back_up.close()
        #print(type(soup))
        print("Done, check your folder to read -> " + goodname)
        #print(html_src)
        return
    
    def get_html_src(self, keyword = 'table_eng_text'):
        # delay to get full page source
        try:
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, keyword)))

        except Exception: 
            #this is hack but whatever
            print("Waiting for page to load...")
            pass

        finally:
            html_src = self.driver.page_source
            self.soup = BeautifulSoup(html_src, "html5lib")
            print('Got Source!!')
            return self.soup
        
    def refresh_page(self):
        self.driver.refresh()
        self.ref_count += 1
        

    def __del__(self):
        self.driver.quit()
        print("deleted soup")
        

        
class Race:
    def __init__(self, name, url):
        self.url = url
        self.name = name
        self.soup = URLsoup(name, url)
        print("URLsoup object intiated")
        
        print("Initialing scraping process on " + str(self.url))

    
    def save_html(self, name):
        return self.soup.save_html(name)
    
    def get_html_src(self, keyword = 'table_eng_text'):
        return self.soup.get_html_src(keyword=keyword)
        
    def refresh_page(self):
        if self.soup.ref_count >= 5:
            print("Restartng.....")
            del self.soup
            self.soup = URLsoup(self.name, self.url)
            print("Your soup is fresh now!")
        else: 
            print("Refreshng.....")
            self.soup.refresh_page()
            print("Your soup is fresh now!")
        
    def quit_soup(self):
        self.soup.__del__()

    def __del__(self):
        self.soup.__del__()
        print("quitted race")