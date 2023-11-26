import os
import pandas
from utils.organize_img import organize_data
from utils.scraper import amazon_image_scrape as az_scrape
from utils.scraper import google_image_scrape as gg_scrape
from utils.parse_list import parse_data
from datetime import datetime
import time

parent_dir = 'img'
os.makedirs(parent_dir, exist_ok=True)  # create the parent directory if it doesn't exist

master_df = pd.DataFrame([], columns=['Title', 'URL', 'Time', 'Source']) # create master data frame

parse_data()

# scrape images for each hardware item
for name in arr_item:
    # output_amazon_df = az_scrape(name[0], name[1])
    # master_df = pd.concat([output_amazon_df , master_df], axis=0)
    output_google_df = gg_scrape(name[0], name[1])
    master_df = pd.concat([output_google_df, master_df], axis=0)
    
master_df.to_excel("image_metadata.xlsx") # export data frame to excel file

organize_data()
