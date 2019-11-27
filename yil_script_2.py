import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
import re

# read in list of names
df = pd.read_csv('names.csv')
names = ["_".join(name.split(' ')) for name in df]
base_url = 'https://en.wikipedia.org/wiki/'


draft_year = []

for name in names:
    try:
        url = base_url+name
        # get the wikipedia page
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page)

        # get the infobox table
        tab = soup.find("table", {"class": "infobox vcard"})   

        # get the draft info from the table
        dr = tab.find("a", {"title": re.compile("[0-9]+ NBA draft")}) 
        draft_year.append(int(dr.text))

        print(f'succeded on {name}')
    except:
        # if we fail on extraction, place a -1 to be filled in by hand    
        print(f"failed on {name}")
        draft_year.append(-1)

# calulate acutal number of years
years = [-1 if year == -1 else 2015 - year for year in draft_year]


# get andrew's data
pp = pd.read_csv('temp.csv')
yil = pp['yil']

# combine mine and Andrew's results to create a master list of YIL
new_years = [y1 if y1>y2 else y2 for y1, y2 in zip(years, yil)]

pp['new_yil'] = years
pp['final_yil'] = new_years

# write to file
pp.to_csv('final_years.csv')
