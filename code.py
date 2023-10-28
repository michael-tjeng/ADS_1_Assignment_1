#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 10:50:36 2023

@author: michaeltjeng
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Load the dataset
data = pd.read_csv('data.csv', encoding='latin1')

# Set display options to show all columns
pd.set_option('display.max.columns', None)

# Convert 'InvoiceDate' to datetime format
data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'], errors='coerce')

# Drop rows where 'InvoiceDate' could not be converted to datetime
data = data.dropna(subset=['InvoiceDate'])

# Calculate total sales
data['TotalSales'] = data['Quantity'] * data['UnitPrice']

# Set InvoiceDate as the index
data.set_index('InvoiceDate', inplace=True)

# Resample the data by month and sum the total sales for each country
monthly_sales = data.groupby('Country').resample('M')['TotalSales'].sum().reset_index()

# Find the top 5 countries by total sales
top_countries = monthly_sales.groupby('Country')['TotalSales'].sum().nlargest(5).index

# Filter the data to include only the top countries
top_countries_data = monthly_sales[monthly_sales['Country'].isin(top_countries)]

# Line Plot: Monthly Sales Over Time by Country
plt.figure(figsize=(14, 7))

# Loop through each country and plot the data
for country in top_countries:
    country_data = top_countries_data[top_countries_data['Country'] == country]
    plt.plot(country_data['InvoiceDate'], country_data['TotalSales'], label=country)

# Formatting the plot
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
