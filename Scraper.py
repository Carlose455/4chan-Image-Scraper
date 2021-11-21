
import requests 
from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 
import shutil
from webdriver_manager.chrome import ChromeDriverManager
import threading
from threading import Thread

thread_prefix = 'https://boards.4chan.org//thread/'

prefix = 'https:'

class Media_Scraper_4chan():

    def __init__(self, folder_name, thread_number, board):
        '''intializes basic gloabal variables'''
        self.board = board
        self.folder_name = folder_name
        self.thread_number = thread_number
        self.thread_url = 'https://boards.4chan.org/%s/thread/%s' % (board, thread_number)
        self.path = '/Users/karlos/Desktop/' + folder_name

    def path_exists(self):
        '''Determines if the global variable "path" (listed above) exsists'''
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        else: 
            pass

    def initialize_scrapper(self):
        '''Initializes the scrappers used to acquire the content necessary, and sets them as global variables'''
        driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver = driver
        driver.get(self.thread_url)
        soup_driver = BeautifulSoup(driver.page_source,"html.parser")
        self.soup_driver = soup_driver

        webpage_response = requests.get(self.thread_url)
        webpage = webpage_response.content
        soup_webpage = BeautifulSoup(webpage, "html.parser")
        self.soup_webpage = soup_webpage

    def img_num(self):
        '''Acquires the number of images found on in the thread using global variable "soup_driver"'''
        try:
            item = self.soup_driver.select('body > div.navLinks.desktop > div > span.ts-images')[0].text
            self.item = item
        except:
            item = self.soup_driver.select('body > div.navLinks.desktop > div > em')[0].text
            self.item = item 
    
        self.driver.quit() 

    def create_directory(self): 
       '''Determines the name of the thread, and creates a directory within "path" with the appropriate name.
       If it exists its contents will be overwritten''' 
        pagename = self.soup_webpage.find('title').text
        newpagename = pagename.replace('/', '|')
        newpath = self.path + '/' + newpagename
        self.newpath = newpath
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        else:
            shutil.rmtree(newpath)        
            os.makedirs(newpath)

    def begin_scraping(self):
            '''Acquires the media files of the 4chan thread (including poster as well), and 
            saves it to the global variables "links"'''
            imglinks = self.soup_webpage.find_all(attrs={'class':'fileThumb'})
            links = []
            for link in imglinks: 
                links.append(prefix + str(link.get('href')))
            self.links = links

    def download_image_links(self):
        '''Saves the images to the newpath directory'''
        counter = 1

        for index, link in enumerate(self.links):
            try: 
                res = requests.get(link)
                name = link.split('/')[-1]
                print(name)
                count = f"{counter}/{self.item}"
                print(count)
                counter += 1
                with open(self.newpath + '/' + str([index+1]) + str(name), 'wb') as f:
                    f.write(res.content) 
            except:
                continue

    def runall(self):
        '''Will run all the def's at the same time'''
        if __name__ == '__main__':
            Thread(target = self.path_exists()).start()
            Thread(target = self.initialize_scrapper()).start()
            Thread(target = self.img_num()).start()
            Thread(target = self.create_directory()).start()
            Thread(target = self.begin_scraping()).start()
            Thread(target = self.download_image_links()).start()

            
run = Media_Scraper_4chan(folder_name = '', thread_number = '', board = '')

run.runall() 
            
