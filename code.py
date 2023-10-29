#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 10:50:36 2023

@author: michaeltjeng
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# define function to load csv and preprocess data
def load_and_preprocess_data(file_path):
    data = pd.read_csv(file_path, encoding='latin1')
    data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'], errors='coerce')
    data = data.dropna(subset=['InvoiceDate'])
    data['TotalSales'] = data['Quantity'] * data['UnitPrice']
    data.set_index('InvoiceDate', inplace=True)
    return data

def get_monthly_sales(data):
    return data.groupby('Country').resample('M')['TotalSales'].sum().reset_index()

def get_top_countries(monthly_sales, n=5):
    return monthly_sales.groupby('Country')['TotalSales'].sum().nlargest(n).index

def plot_sales_over_time(top_countries_data, top_countries):
    plt.figure(figsize=(14, 7))
    for country in top_countries:
        country_data = top_countries_data[top_countries_data['Country'] == country]
        plt.plot(country_data['InvoiceDate'], country_data['TotalSales'], label=country)
    plt.title('Monthly Sales Over Time by Country')
    plt.xlabel('Date')
    plt.ylabel('Total Sales (£)')
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=6))
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    plt.legend(title='Country')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
# main program
if __name__ == "__main__":
    pd.set_option('display.max.columns', None)
    
    data = load_and_preprocess_data('data.csv')
    monthly_sales = get_monthly_sales(data)
    top_countries = get_top_countries(monthly_sales)
    top_countries_data = monthly_sales[monthly_sales['Country'].isin(top_countries)]
    
    plot_sales_over_time(top_countries_data, top_countries)

# Extracting hour information from InvoiceDate
data['Hour'] = data.index.hour

# Grouping data by hour and summing total sales
sales_by_hour = data.groupby('Hour')['TotalSales'].sum().reset_index()

sales_by_hour.head()

def plot_sales_by_hour(sales_by_hour):
    plt.figure(figsize=(10, 6))
    plt.bar(sales_by_hour['Hour'], sales_by_hour['TotalSales'], color='skyblue')
    
    # Formatting
    plt.title('Sales by Hour of the Day')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Total Sales (£)')
    plt.xticks(range(24))  # Set x-ticks to show every hour
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# Plot bar chart
plot_sales_by_hour(sales_by_hour)
