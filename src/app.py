import os
from bs4 import BeautifulSoup
import requests
import time
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# select the webpage url to scrape data from
tesla_url = "https://companies-market-cap-copy.vercel.app/index.html"

# request to download fht efile from the internet
response = requests.get(tesla_url)

# if the request was opened correctly then store the data in a csv file
if response.status_code == 200:
    web_content = BeautifulSoup(response.text, 'html.parser')
else:
    print("Error, the web content was not receeived")

#print(web_content.prettify())

# Find the table with the year evolution.
table = web_content.find("table")
#print(table)

# Obtain the data and its rows skipping the header row
rows = table.find_all("tr")[1:]

# Store the data in a DataFrame.
data = [[col.text.strip() for col in row.find_all("td")] for row in rows]
# print(data)

# create dataframe
data_df = pd.DataFrame(data, columns=['Date', 'Revenue', 'Percentage Change'])

# sort the data by date in descending order
data_df = data_df.sort_values('Date', ascending=False)
print(data_df)