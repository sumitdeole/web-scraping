## Web scraping project on *Walt Disney movies*

### **Description:** 
We will scrape movie information (producers, directors, cast, budget, etc.) of Walt Disney movies from Wikipedia pages. The project is divided into four exercises:

1. Get movie information on a famous Walt Disney Movie: [Toy Story 3](https://en.wikipedia.org/wiki/Toy_Story_3):
    - Code stored in *Toy_story_3.py*
2. Get the list of all [Walt Disney movies](https://en.wikipedia.org/wiki/List_of_Walt_Disney_Pictures_films):
    - In addition to recovering movie list from the link above, we pull movie specific details following step 1 for each movie.  
    - Code stored in *Disney_movies.py*
    - Data stored in JSON file *Disney_data.json*
3. Data cleaning: The cleaned data is stored in the JSON file *Disney_data_clean.json* (or alternatively, in a pickle file *disney_movie_data_cleaned_more.pickle*)
    - Convert dates into datetime objects: 
        - Preferred format: June 27, 1941
        - Edge case covered: "27 June 1941" *or* "June 27, 1941 ( 1941-06-27 ) [1]" 
    - Convert *Running time* into an integer
        - Originally, in a string format: "64 minutes"
        - Will be convered into an integer with the *minutes_to_integer(running_time)* method
    - Remove the wiki references/citations: [1], [2], [3], etc.
        - Present in many places. 
        - Removed the citations and ignored the cited weblinks
    - Repair the inconsistencies in the "Starring" list --> Split up the long strings, e.g., movie "The Great Locomotive Chase"
        - No comma separation between dnamees
        - Edge case 1: "Produced by": "David Blocker Larry Brezner Mark Frost"
        - Edge case 2: "Starring": "Shia LaBeouf Stephen Dillane Peter Firth Elias Koteas",
    - Replace number range in the "Budget" and "Box office" with numbers
        - Original, in string format: "$950,000" *or* "$267.4 million" 
        - Edge cases: "$3.355 million (worldwide rentals) [2]" *or* "$950,000 [2]" *or* "$3.7 million (U.S. rental) + $575,000 (foreign rental) [3]" *or* "60 million Norwegian Kroner (around $8.7 million in 1989)"
        - All monetary values converted to *float* with the *money_conversion(money)* method
4. Merge the cleaned movie list data (in step #3) with IMDB/Metascore/Rotten Tomatoes ratings of the Disney movies: Here, instead of scraping these websites for ratings separately, we will use publicly available APIs (e.g., [OMDb API](https://www.omdbapi.com/)).
5. Finally, let's save data in JSON and CSV formats


### Python packages
To perform the exercises listed above, the following Python packages are installed.
- Requests
- BeautifulSoup
- JSON
- regex
- Pytest
- Pickle



##### *Disclaimer:* I already confirmed what is allowed concerning web scraping in wikipedia's rules present in their robots.txt. All is well here. Original source: Youtube tutorial by Keith Galli
