# Project title: Web scraping project on Walt Disney movies

#################################################################
# Exercise 2
# Get the list of all Walt Disney movies
#################################################################


import requests
from bs4 import BeautifulSoup as bs
import prettify
import random


page2 = "https://en.wikipedia.org/wiki/List_of_Walt_Disney_Pictures_films"
response2 = requests.get(page2).content
soup2 = bs(response2, "html.parser")

contents2 = soup2.prettify()

# Capture the info table
info_box2 = soup2.find(class_="mw-headline")

print(info_box2.prettify())

info_rows2 = info_box2.find_all("tr")
for row in info_rows:
    print(row.prettify())