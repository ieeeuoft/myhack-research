import requests
import pandas as pd
import re
import os
import time
import urllib
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from urllib.parse import urlencode, urljoin

# used to avoid Amazon blocking the scraper 
SCRAPEOPS_API_KEY = 'ced5bffb-0941-4ba2-8faa-ee55f55f1f0a'

def scrapeops_url(url):
    payload = {'api_key': SCRAPEOPS_API_KEY, 'url': url, 'country': 'us'}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url

def amazon_image_scrape(name_item, topic_name):
    search_url = f'https://www.amazon.com/s?k={topic_name}&page=1'

    html = requests.get(scrapeops_url(search_url))
    
    print(html)
    soup = BeautifulSoup(html.content, features="lxml")
    links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})

    arr_list = [] # store searched result links

    df = pd.DataFrame([], columns=['Title', 'Source URL', 'Time', 'Source']) # create data frame

    for link in links:
        arr_list.append(link.get('href'))

    for count, link in enumerate(arr_list):
        webpage_url = "https://www.amazon.com" + link
        webpage = requests.get(webpage_url, headers=HEADERS)
        new_soup = BeautifulSoup(webpage.content, "lxml")
        
        title = None
        
        # get product title
        try:
            title = new_soup.find("span", attrs={"id": 'productTitle'}).text.strip()
        except AttributeError:
            print("Cannot retrieve product title")

        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

        row = {
            "Title": title,
            "Source URL": webpage_url,
            "Time": formatted_time,
            "Source": "Amazon"
        }

        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)

        images = re.findall('"hiRes":"(.+?)"', webpage.text)

        for num, img_url in enumerate(images):
            img_dir = "./img/{topic}/".format(topic=name_item)
            os.makedirs(img_dir, exist_ok=True)  # create the directory if it doesn't exist
            img_filename = img_dir + "image{num}_amazon.jpg".format(num=num)
            img_filename.format(topic=name_item, i=num)
            urllib.request.urlretrieve(img_url, img_filename) # retrieve images

    return df

def scroll_to_end(webdriver):
    webdriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(10)

def google_image_scrape(topic_name, name_item):
    chrome_options = webdriver.ChromeOptions() # creates instance of ChromeOptions class
    chrome_options.add_argument('--headless') # runs Chrome in headless mode
    chrome_options.add_argument('--no-sandbox') # disable sandbox mode in Chrome
    chrome_options.add_argument('--disable-dev-shm-usage') # disables '/dev/shm/ for shared resources
    driver = webdriver.Chrome('chromedriver', options=chrome_options) # defines path to ChromeDriver executable
    driver.maximize_window()
    
    df = pd.DataFrame([], columns=['Title', 'Source URL', 'Time', 'Source']) # create data frame
    
    search_url = "https://www.google.com/search?q={topic}&tbm=isch&ved=2ahUKEwii57id66j_AhVUGFkFHYNpAuYQ2-cCegQIABAA&oq=bluetooth+wireless+module+bluefruit+le+shield+adafruit&gs_lcp=CgNpbWcQAzIECCMQJ1DnCFjnCGC1EWgAcAB4AIABP4gBdpIBATKYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=Cxt8ZOK1JtSw5NoPg9OJsA4&bih=568&biw=1251&hl=en"
    driver.get(search_url.format(topic=topic_name)) # replaces topic in the search_url to the desired topic
    
    # Wait for images to load
    while True:
        last_height = driver.execute_script('return document.body.scrollHeight')

        scroll_to_end(driver)
        
        new_height = driver.execute_script('return document.body.scrollHeight')
        
        if new_height == last_height:
            break
        
        last_height = new_height
        
    
    img_results = driver.find_elements(By.XPATH, "//img[contains(@class,'Q4LuWd')]") # returns a list of image elements found on webpage
    div_elements = driver.find_elements(By.CSS_SELECTOR, 'div.isv-r.PNCib.MSM1fd.BUooTd')
            
    images = []
    for i in range(len(img_results)):
        img_src = img_results[i].get_attribute('src')
        if img_src:
            images.append(img_src)
            current = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
            title_element = div_elements[i].find_element(By.CSS_SELECTOR, 'h3.bytUYc')
            title = title_element.text

            try:
                link_element = div_elements[i].find_element(By.CSS_SELECTOR, 'a.VFACy.kGQAp.sMi44c.d0NI4c.lNHeqe.WGvvNb')
                url = link_element.get_attribute('href')
            except Exception:
                print("Link element not found within the div element")

            row = {"Title": title, "Source URL": url, "Time": current, "Source": "Google"}
            df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    
    for num in range(len(images)):
        img_dir = "./img/{topic}/".format(topic=name_item)
        os.makedirs(img_dir, exist_ok=True)  # Create the directory if it doesn't exist
        img_filename = img_dir + "image{num}_google.jpg".format(num=num)
        urllib.request.urlretrieve(str(images[num]), img_filename)
    
    driver.quit()
    
    return df

