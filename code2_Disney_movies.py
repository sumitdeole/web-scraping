# Project title: Web scraping project on Walt Disney movies

#################################################################
# Exercise 2
# Get the list of all Walt Disney movies
#################################################################


import requests
from bs4 import BeautifulSoup as bs
import prettify
import random
import json


page = "https://en.wikipedia.org/wiki/List_of_Walt_Disney_Pictures_films"
response = requests.get(page)
soup = bs(response.content, "html.parser")

# Print out the html
contents = soup.prettify()
print(contents)

# Capture the info table - use an alternative to Toy_story_3py: select method
movies = soup.select(".wikitable.sortable i")
movies[0:10]
movies[0].a["href"]
movies[0].a["title"]



#Build a function to deal with case where there are multiple names (a list) in the cell
def get_content_value(row_data):
    if row_data.find("li"):
        return [li.get_text(" ",strip=True).replace("\xa0", " ") for li in row_data.find_all("li")]
    else:
        return row_data.get_text(" ",strip=True).replace("\xa0", " ")

def get_info_box(url):
  # First we copy code from task 1
  response = requests.get(url).content
  soup = bs(response, "html.parser")
  # Capture the info table
  info_box = soup.find(class_="infobox vevent")
  info_rows = info_box.find_all("tr")
  for row in info_rows:
    print(row.prettify())
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
  return movie_info



page = "https://en.wikipedia.org/wiki/List_of_Walt_Disney_Pictures_films"
response = requests.get(page)
soup = bs(response.content, "html.parser")


movies = soup.select(".wikitable.sortable i a") # or one step less soup.select(".wikitable.sortable i") --> throws movies without links in errors

base_path = "https://en.wikipedia.org/"
movie_info_list = []
for index, movie in enumerate(movies):
  # To avoid making too many requests: if index==10 (on new line)--> break
  # method is not fool proof for all different wiki syntax, employ the "try" method
  try:
    relative_path=movie["href"]
    title = movie["title"]
    full_path=base_path+relative_path
    movie_info_list.append(get_info_box(full_path))
  except Exception as e:
    print(movie.get_text())
    print(e)



# Save data - json preferable

def save_data(title, data):
  with open(title, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii= False, indent=2)


def load_data(title):
  with open(title, encoding="utf-8") as f:
    return json.load(f)

save_data("Disney_data.json", movie_info_list)
