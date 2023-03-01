# -*- coding: UTF-8 -*-
"""PyRamen Homework Starter."""

# @TODO: Import libraries
import csv
from pathlib import Path
import pandas as pd
import numpy as np



# @TODO: Set file paths for menu_data.csv and sales_data.csv
#home = Path.home()
#menu_filepath = Path(home,"PyRamen","Resources","menu_data.csv")
#sales_filepath = Path(home,"PyRamen","Resources","sales_data.csv")

menu_filepath = Path(".","PyRamen","Resources","menu_data.csv")
sales_filepath = Path(".","PyRamen","Resources","sales_data.csv")

def create_report_df(menu_file, sale_file):
    #initiate variables
    report_item = {"ramen-type":"",
          "01-count": 0,
          "02-revenue": 0,
          "03-cogs": 0,
          "04-profit":0
         }
    
    report_lines = []
    
    #read file
    menu = pd.read_csv(menu_file)
    sales = pd.read_csv(sale_file)
    # left join two tables
        # (1) sort menu. A sorted table could make join faster
    menu.sort_values("item", inplace = True)
        # (2) change column name for left join
    sales.rename(columns={"Menu_Item":"item"}, inplace=True, errors='raise')
        # (3) join dataframe
    df_ramen = sales.merge(menu, on="item", how='left')
    # calculate item_revenue, item_cost, item_profit for each Line_item
    df_ramen['item_revenue'] = df_ramen['price']*df_ramen['Quantity']
    df_ramen['item_cost'] = df_ramen['cost']*df_ramen['Quantity']
    df_ramen['item_profit'] = df_ramen['item_revenue'] - df_ramen['item_cost']
    
    # get ramen type list
    type_lt=df_ramen.item.unique().tolist()
    
    # get report data
    for item in type_lt:
        df_item = df_ramen[df_ramen.item == item]
        
        ramen_type = item
        count = np.sum(df_item.Quantity)
        revenue = np.sum(df_item.item_revenue)
        cogs = np.sum(df_item.item_cost)
        profit = np.sum(df_item.item_profit)
        
        report_item = {"ramen-type":ramen_type,
          "01-count": count,
          "02-revenue": revenue,
          "03-cogs": cogs,
          "04-profit":profit
         }
        
        report_lines.append(report_item)
        
        #initiate variables. To avoid calculation errors caused by missing values
        report_item = {"ramen-type":"",
                      "01-count": 0,
                      "02-revenue": 0,
                      "03-cogs": 0,
                      "04-profit":0
                         }

    # write to dataframe
    return pd.DataFrame(report_lines)

# -------------------------------

the_report = create_report_df(menu_filepath, sales_filepath)

# write to csv
the_report.to_csv('./PyRamen/ramen_report.csv', sep=',', encoding='utf-8')
