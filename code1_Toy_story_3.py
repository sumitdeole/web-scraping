# Project title: Web scraping project on Walt Disney movies

#################################################################
# Exercise 1
# Toy Story 3: Get all info
#################################################################


import requests
from bs4 import BeautifulSoup as bs
import prettify
import random


page = "https://en.wikipedia.org/wiki/Toy_Story_3"
response = requests.get(page).content
soup = bs(response, "html.parser")

contents = soup.prettify()

# Capture the info table
info_box = soup.find(class_="infobox vevent")

print(info_box.prettify())

info_rows = info_box.find_all("tr")
for row in info_rows:
    print(row.prettify())


#Build a function to deal with case where there are multiple names (a list) in the cell
def get_content_value(row_data):
    if row_data.find("li"):
        return [li.get_text(" ",strip=True).replace("\xa0", " ") for li in row_data.find_all("li")]
    else:
        return row_data.get_text(" ",strip=True).replace("\xa0", " ")


# Save all rows in a dictionary
movie_info = {}
for index, row in enumerate(info_rows):
    if index==0:
        movie_info["title"]=row.find("th").get_text(" ",strip=True)
    elif index==1:
        continue
    else:
        content_key = row.find("th").get_text(" ",strip=True)
        content_value = get_content_value(row.find("td"))
        movie_info[content_key] = content_value

print(movie_info)

