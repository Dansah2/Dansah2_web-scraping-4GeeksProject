import os
from bs4 import BeautifulSoup
import requests
import time
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# select the webpage url to scrape data from
tesla_url = "https://companies-market-cap-copy.vercel.app/index.html"

# request to download fht efile from the internet
response = requests.get(tesla_url)

# if the request was opened correctly then store the data in a csv file
if response.status_code == 200:
    web_content = BeautifulSoup(response.text, 'html.parser')
else:
    print("Error, the web content was not receeived")

print(web_content)