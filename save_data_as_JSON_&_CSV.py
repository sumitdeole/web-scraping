# Project title: Web scraping project on Walt Disney movies

#################################################################
# Exercise 5
# Save data in JSON and CSV formats
#################################################################

import requests
import pickle
import os
import urllib
import json

# First load the pickle data
with open("Disney_data_&_ratings.pickle", "rb") as fp:
    movie_info_list = pickle.load(fp)

# To be able to store data into JSON, we need to make datetime function
movie_info_copy = [movie.copy() for movie in movie_info_list]
for movie in movie_info_copy:
    current_date=movie["Release date (datetime)"]
    if current_date:
        movie["Release date (datetime)"] = current_date.strftime("%B %d, %Y")
    else:
        movie["Release date (datetime)"] = None


# Now lets save the data
# First in JSON
def save_data(title, data):
  with open(title, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii= False, indent=2)

save_data("Disney_data_final.json", movie_info_copy)


# Now lets convert the data into CSV
# Need new libraries
import pandas as pd
df = pd.DataFrame(movie_info_list)
df.head() # To observe CSV data
df.info()
#Now save
df.to_csv("Disney_data_final.csv")


# To see which movie lasted the longest
running_times = df.sort_values(["Running time (int)"], ascending=True)
running_times[["title", "Running time (int)"]]