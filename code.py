#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 10:50:36 2023

@author: michaeltjeng
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Define function to load CSV and preprocess data
def load_and_preprocess_data(file_path):
    data = pd.read_csv(file_path, encoding='latin1')
    data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'], errors='coerce')
    data = data.dropna(subset=['InvoiceDate'])
    data['TotalSales'] = data['Quantity'] * data['UnitPrice']
    data.set_index('InvoiceDate', inplace=True)
    return data

# Define function to get monthly sales
def get_monthly_sales(data):
    return data.groupby('Country').resample('M')['TotalSales'].sum().reset_index()

# Define function to get top countries
def get_top_countries(monthly_sales, n=5):
    return monthly_sales.groupby('Country')['TotalSales'].sum().nlargest(n).index

# Define function to plot sales over time
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

# Define function to get sales by hour
def get_sales_by_hour(data):
    data['Hour'] = data.index.hour
    sales_by_hour = data.groupby('Hour')['TotalSales'].sum().reset_index()
    return sales_by_hour

# Define function to plot sales by hour
def plot_sales_by_hour(sales_by_hour):
    plt.figure(figsize=(10, 6))
    plt.bar(sales_by_hour['Hour'], sales_by_hour['TotalSales'], color='skyblue')
    plt.title('Sales by Hour of the Day')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Total Sales (£)')
    plt.xticks(range(24))  # Set x-ticks to show every hour
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# Define function to plot total sales by country with a legend
def plot_total_sales_by_country(data):
    total_sales_by_country = data.groupby('Country')['TotalSales'].sum().sort_values(ascending=False)
    top_5_countries = total_sales_by_country.head(5)
    other_countries_sum = total_sales_by_country[5:].sum()
    pie_data = top_5_countries.append(pd.Series(other_countries_sum, index=['Other Countries']))
    
    explode = (0.1, 0.1, 0.1, 0.1, 0.1, 0.1)
    colors = plt.cm.Paired(range(len(pie_data)))
    
    plt.figure(figsize=(7, 7))
    wedges, texts = plt.pie(pie_data, startangle=140, explode=explode, colors=colors, textprops=dict(color="w"))
    labels = [f"{label}: {perc:.1f}% ({amount:,.0f} £)" for label, perc, amount in zip(pie_data.index, 100*pie_data/pie_data.sum(), pie_data)]
    plt.legend(wedges, labels, title="Countries", loc="center left", bbox_to_anchor=(0.8, 0, 0.5, 1))
    plt.title('Total Sales by Country')
    plt.axis('equal')
    plt.show()

# Main program
if __name__ == "__main__":
    pd.set_option('display.max.columns', None)
    
    # Load and preprocess data
    data = load_and_preprocess_data('data.csv')
    
    # Monthly sales analysis
    monthly_sales = get_monthly_sales(data)
    top_countries = get_top_countries(monthly_sales)
    top_countries_data = monthly_sales[monthly_sales['Country'].isin(top_countries)]
    plot_sales_over_time(top_countries_data, top_countries)
    
    # Sales by hour analysis
    sales_by_hour = get_sales_by_hour(data)
    plot_sales_by_hour(sales_by_hour)
    
    # Total sales by country with a legend
    plot_total_sales_by_country(data)

