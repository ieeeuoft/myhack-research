import pandas as pd
import openpyxl
import os
import cv2 as cv
import shutil

def parse_data():
    # read hardware component Excel sheet
    hardware_components = pd.read_excel(
        '../IEEE Hardware Inventory 2023-2024.xlsx',
        sheet_name='2022-2023 inventory',
    )

    size_list = hardware_components['name'].size # total number of hardware items
    arr_item = [] # holds all item's full names

    # loop through the rows and get the item's: name, manufacturer, and model
    for i in range(size_list):
        curr_item = []
        # if a field does not exist, replace with empty string
        name = "" if str(hardware_components['name'].iloc[i]) == "nan" else str(hardware_components['name'].iloc[i])
        manufacturer = "" if str(hardware_components['manufacturer'].iloc[i]) == "nan" else str(hardware_components['manufacturer'].iloc[i])
        model = "" if str(hardware_components['model_number'].iloc[i]) == "nan" else str(hardware_components['model_number'].iloc[i])
        curr_item.append(name + " " + manufacturer + " " + model) # append into arr
        curr_item.append(name.replace(" ", ""))
        arr_item.append(curr_item)