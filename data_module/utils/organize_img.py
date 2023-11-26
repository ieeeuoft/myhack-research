import os
import pandas as pd
import shutil

def organize_data(arr_item):
    og = './img'
    for item in arr_item:
        path = os.path.join(og, item[1])
        os.makedirs(path, exist_ok=True)
        
    parent_folder = './dataset'
    df = pd.read_excel('../IEEE Hardware Inventory 2023-2024.xlsx')
    unique_categories = pd.unique(df['categories'])

    for category in unique_categories: 
        path = os.path.join(parent_folder, category)
        os.makedirs(path, exist_ok=True)
        
    num_rows = df.shape[0]
    column_name = 'categories'

    for i in range(1, num_rows, 1):
        cell_value = df.at[0, column_name]
        target = './dataset/{category}'.format(category=cell_value)
        original = './img/{name_item}'.format(name_item=arr_item[0][1])
        shutil.move(original, target)