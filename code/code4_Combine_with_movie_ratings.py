# Project title: Web scraping project on Walt Disney movies

#################################################################
# Exercise 4
# Merge the cleaned movie list data (in step #3) with IMDB/Metascore/Rotten Tomatoes ratings
# of the Disney movies
# Use [OMDb API](https://www.omdbapi.com/)
# OMDb API: http://www.omdbapi.com/?i=tt3896198&apikey=d26269f0
# API key: d26269f0
#################################################################

import requests
import pickle
import os
import urllib

with open("Disney_data_cleaned.pickle", "rb") as fp:
    movie_info_list = pickle.load(fp)


def get_omdb_info(title):
    base_url = "http://www.omdbapi.com/?"
    parameters = {"apikey": "d26269f0", "t": title}
    params_encoded = urllib.parse.urlencode(parameters)
    full_url=base_url + params_encoded
    return requests.get(full_url).json()

def get_rotten_tomatoes_score(omdb_info):
  ratings = omdb_info.get("Ratings", [])
  for rating in ratings:
    # print(rating)   # To observe the issue with Rotten Tomotoes ratings
    if rating["Source"]=="Rotten Tomatoes":
      return rating["Value"]
    return None

# To test if the code works for one movie
# info = get_omdb_info("into the woods")
# get_rotten_tomatoes_score(info)

for movie in movie_info_list:
  title = movie["title"]
  omdb_info = get_omdb_info(title)
  movie["imdb"]= omdb_info.get("imdbRating", None)
  movie["metascore"]=omdb_info.get("Metascore", None)
  movie["rotten tomatoes"]=get_rotten_tomatoes_score(omdb_info)

movie_info_list[-50]


def save_data_pickle(name, data):
  with open(name, "wb") as f:
    pickle.dump(data, f)

def load_data_pickle(name):
  with open(name, "rb") as f:
    return pickle.load(f)

save_data_pickle("Disney_data_&_ratings.pickle", movie_info_list)
