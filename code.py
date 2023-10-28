#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 10:50:36 2023

@author: michaeltjeng
"""

import pandas as pd

# Load the dataset
data = pd.read_csv('data.csv', encoding='latin1')

# Set display  options to show all columns
pd.set_option('display.max.columns', None)

# Show the first few rows of the dataset
print(data.head())