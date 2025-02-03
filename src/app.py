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

# if the request was executed correctly, parse it using BeautifulSoup
if response.status_code == 200:
    web_content = BeautifulSoup(response.text, 'html.parser')
else:
    print(f"Error, the web content was not received, the error code is {response.status_code}")

# find the table with the year evolution.
table = web_content.find("table")

# Obtain the data and its rows skipping the header row
rows = table.find_all("tr")[1:]

# strip the data from the table
data = [[col.text.strip() for col in row.find_all("td")] for row in rows]

# store the data in a dataframe
data_df = pd.DataFrame(data, columns=['Date', 'Revenue', 'Percentage_Change'])

# sort the data by date in descending order
data_df = data_df.sort_values('Date', ascending=False)

# remove the '$' and 'B' in the dataframe
data_df["Revenue"] = data_df["Revenue"].str.replace("[$B]", "", regex=True).astype(float)

# connect to the database
connection = sqlite3.connect('"tesla_revenues.db"')
cursor = connection.cursor()

# create the table.
cursor.execute("""
CREATE TABLE IF NOT EXISTS revenue (
    date TEXT,
    revenue REAL
)
""")

# insert the values from the dataframe into the revenue table
data_list = data_df[["Date", "Revenue"]].values.tolist()
cursor.executemany("INSERT INTO revenue (date, revenue) VALUES (?, ?)", data_list)


# store (commit) the changes you have made to the database
connection.commit()
connection.close()


# I utilized three different ways to plot the data. Please check the explore.ipynb file to see the plots.


# plot the data using a line chart

data_df = data_df.sort_values('Date')

plt.figure(figsize=(10, 5))
plt.plot(data_df['Date'], data_df['Revenue'], marker='o', label='Revenue', color='b')

plt.twinx()
plt.plot(data_df['Date'], data_df['Percentage_Change'], marker='s', linestyle='dashed', label='Percentage Change', color='r')

plt.title('Teslas Annual Revenues from 2009 - 2024 (in Billions)')
plt.xlabel('Year')
plt.legend()
plt.show()



# plot the data via a bar chart

plt.figure(figsize=(10, 5))
sns.barplot(x=data_df['Date'], y=data_df['Revenue'], hue=data_df['Date'], palette='Blues_r')

plt.title('Teslas Annual Revenues from 2009 - 2024 (in Billions)')
plt.xlabel('Year')
plt.ylabel('Revenue')
plt.xticks(rotation=45)
plt.show()



# plot the data using a scatter plot

plt.figure(figsize=(15, 5))
data_df['Percentage_Change'] = data_df['Percentage_Change'].str.replace('%', '', regex=False).str.strip()
data_df['Percentage_Change'] = data_df['Percentage_Change'].replace(['', pd.NA], np.nan)
data_df['Percentage_Change'] = data_df['Percentage_Change'].astype(float)
sns.regplot(x=data_df['Percentage_Change'], y=data_df['Revenue'], scatter_kws={'color': 'blue'}, line_kws={'color': 'red'})

plt.title('Teslas Revenue vs Percentage Change')
plt.xlabel('Percentage Change')
plt.ylabel('Revenue')
plt.show()