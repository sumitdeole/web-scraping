# Project title: Web scraping project on Walt Disney movies

#################################################################
# Exercise 3
# Clean the data
## To do (Need to regenerate data file):
### Convert dates into datetime objects
### Convert running time into an integer
### Remove the wiki references/citations: [1], [2], [3], etc.
### Repair the inconsistencies in the "Starring" list --> Split up the long strings, e.g., movie "The Great Locomotive Chase"
### Replace number range in the "Budget" and "Box office" with numbers
#################################################################


# Import packages
from bs4 import BeautifulSoup as bs
from datetime import datetime
import requests
import json
import re
import pickle


# Get the html response
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
    elif row_data.find("br"): ### Solution to "Repair the inconsistencies in the "Starring" list" --> Split up the long strings, e.g., movie "The Great Locomotive Chase"
      return[text for text in row_data.stripped_strings]
    else:
        return row_data.get_text(" ",strip=True).replace("\xa0", " ")

# Repair dates
def clean_reference_tags(soup):
  for tag in soup.find_all(["sup","span"]):
    tag.decompose()

def get_info_box(url):
  # First we copy code from task 1
  response = requests.get(url).content
  soup = bs(response, "html.parser")
  # Capture the info table
  info_box = soup.find(class_="infobox vevent")
  info_rows = info_box.find_all("tr")
  for row in info_rows:
    print(row.prettify())
  clean_reference_tags(soup)
  movie_info = {}
  for index, row in enumerate(info_rows):
    if index==0:
      movie_info["title"]=row.find("th").get_text(" ",strip=True)
    # elif index==1: # Solution to deal with edge-case (when table header is absent) added below
    #   continue
    else:
      header = row.find("th")
      if header:
        content_key = row.find("th").get_text(" ",strip=True)
        content_value = get_content_value(row.find("td"))
        movie_info[content_key] = content_value
  return movie_info

# To run check whether our functions work properly, we could also test our an example url
# e.g.,
# get_info_box(https://en.wikipedia.org/wiki/Snow_White_and_the_Seven_Dwarfs_(1937_film))
# Observe the issue (also highlighted in Data_cleaning.py): we see  wiki references/citations: [1], [2], [3], etc.
# Solution: See the function method clean_reference_tags(soup) defined above
# Solution also removes double data entries, e.g., "Release date": [       "November 13, 1940 ( 1940-11-13 )"     ],


movies = soup.select(".wikitable.sortable i a") # or one step less soup.select(".wikitable.sortable i") --> throws movies without links in errors

base_path = "https://en.wikipedia.org/"
movie_info_list = []
for index, movie in enumerate(movies):
  # To avoid making too many requests: if index==10 (on new line)--> break
  # method is not fool proof for all different wiki syntax, employ the "try" method
  # if index == 10:
  #   break
  try:
    relative_path=movie["href"]
    title = movie["title"]
    full_path=base_path+relative_path
    movie_info_list.append(get_info_box(full_path))
  except Exception as e:
    print(movie.get_text())
    print(e)



# Convert dates into datetimes
print([movie.get("Release date", "N/A") for movie in movie_info_list])
# Typical format: June 27, 1941 --> but many edge cases
dates = [movie.get("Release date", "N/A") for movie in movie_info_list]
def clean_date(date):
  return date.split("(")[0].strip()


def date_conversion(date):
  if isinstance(date, list):
    date = date[0]
  if date=="N/A":
    return None
  date_string=clean_date(date)
  print(date_string)
  fmts = ["%B %d, %Y", "%d %B %Y"]
  for fmt in fmts:
    try:
      return datetime.strptime(date_string, fmt)
    except:
      pass
  return None



### Task: Convert running time into integer
# First, check whther all movies have running times
# Command
# print([movie.get("Running time", "N/A") for movie in movie_info_list])

### Task: Convert running time into integer
# First, check whether all movies have running times
# Command
# print([movie.get("Running time", "N/A") for movie in movie_info_list])
# Solution: Lets write a function "minutes_to_integer()"
def minutes_to_integer(running_time):
  if running_time=="N/A":
    return None
  if isinstance(running_time, list):
    entry=running_time[0]
    value= int(entry.split(" ")[0])
    return value
  else:
    value= int(running_time.split(" ")[0])
    return value
#Test example: print(minutes_to_integer("85 minutes")) --> Works
#But, edge case: running time as a list: print(minutes_to_integer(["85 minutes", "4 minutes"]))  - a simple function wont work --> hence, if statement with isinstance



# Test example: movie_info_list[-10]
# Test example: TO test whether our function works properly: print([movie.get("Running time (int)", "N/A") for movie in movie_info_list])




### Replace number range in the "Budget" and "Box office" with numbers
# Money conversion
# Given either a string or a list of strings as input, return a number (int or float) which is equal to the monetary value
# money_conversion("$12.2 million") --> 12200000    --> Word syntax
# money_conversion("$790,000") --> 790000  --> Value syntax
number = r"\d+(,\d{3})*\.*\d*"
amounts = r"thousand|million|billion"
standard = fr"\${number}(-|\sto\s)?({number})?\s({amounts})"

value_re = rf"\${number}"
word_re = rf"\${number}(-|\sto\s)?({number})\s({amounts})"

def word_to_value(word):
	value_dict = {"thousand": 1000, "million": 1000000, "billion": 1000000000}
	return value_dict[word]

def parse_word_syntax(string):
		value_string = re.search(number, string).group()
		value=float(value_string.replace(",",""))
		word = re.search(amounts, string, flags=re.I).group().lower()
		word_value = word_to_value(word)
		return value*word_value


def parse_value_syntax(string):
		value_string = re.search(number, string).group()
		value=float(value_string.replace(",",""))
		return value

def money_conversion(money):
		if money=="N/A":
			return None
		if isinstance(money, list):
			money=money[0]
		word_syntax = re.search(word_re, money, flags=re.I)
		value_syntax = re.search(value_re, money)
		if word_syntax:
			return parse_word_syntax(word_syntax.group())
		elif value_syntax:
			return parse_value_syntax(value_syntax.group())
		else:
			return None


for movie in movie_info_list:
  movie["Budget (float)"]=money_conversion(movie.get("Budget", "N/A"))
  movie["Box office (float)"]=money_conversion(movie.get("Box office", "N/A"))
  movie["Running time (int)"]=minutes_to_integer(movie.get("Running time", "N/A"))
  movie["Release date (datetime)"] = date_conversion(movie.get("Release date", "N/A"))


# Save data - json preferable

# def save_data(title, data):
#   with open(title, "w", encoding="utf-8") as f:
#     json.dump(data, f, ensure_ascii= False, indent=2)
#
#
# def load_data(title):
#   with open(title, encoding="utf-8") as f:
#     return json.load(f)
#
# save_data("Disney_data_clean.json", movie_info_list)
# Alert: Cannot continue saving the file into JSON as datetime errs
# SO for now, lets save the data in Pickle and return to it in exercise 5

# Alternatively, use pickle to save and reloaad data

def save_data_pickle(name, data):
  with open(name, "wb") as f:
    pickle.dump(data, f)

def load_data_pickle(name):
  with open(name, "rb") as f:
    return pickle.load(f)

save_data_pickle("Disney_data_cleaned.pickle", movie_info_list)
 # To call saved data
with open("Disney_data_cleaned.pickle", "rb") as fp:
    movie_info_list = pickle.load(fp)

