import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np

# Set the user-agent header to mimic a web browser
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'}


# ============== creat a dataframe where the data will be stored =================
final_df=pd.DataFrame()


# ============== Extract information of 10 pages =================================
for j in range(0,10):
    url='https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?page={}'.format(j)

    # Send a GET request to the desired URL and retrieve the HTML content
    webpage = requests.get(url, headers=headers)

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(webpage.text, 'lxml')

    # Find all game elements on the webpage
    games = soup.find_all('td', class_='clamp-summary-wrap')

    # Initialize lists to store the scraped data
    Sr_no = []
    name = []
    platform = []
    release_date = []
    summary = []
    metascore = []
    userscore = []

# ===================== Extract information for each game element ========================
    for i in games:
        # Extract the serial number
        Sr_no.append(i.find('span', class_='title numbered').text.strip())

        # Extract the game name
        name.append(i.find('h3').text)

        # Extract the platform
        platform.append(i.find('span', class_='data').text.strip())

        # Extract the release date
        release_date.append(i.find_all('span')[3].text)

        # Extract the summary (if available)
        try:
            summary.append(i.find('div', class_='summary').text.strip())
        except:
            summary.append(np.nan)

        # Extract the Metascore (if available)
        try:
            metascore.append(i.find('div', class_='metascore_w large game positive').text)
        except:
            metascore.append(np.nan)

        # Extract the user score (if available)
        try:
            userscore.append(i.find('div', class_='metascore_w user large game positive').text)
        except:
            userscore.append(np.nan)

# =================Create a dictionary from the scraped data ===========================
    a = {
        'Sr_no': Sr_no,
        'name': name,
        'platform': platform,
        'release_date': release_date,
        'summary': summary,
        'metascore': metascore,
        'userscore': userscore
    }

# ========= Create a DataFrame from the dictionary =============
    temp_df = pd.DataFrame(a)
    final_df = final_df.append(temp_df)

# ++++++++++++++++++++++++++++ data cleaning +++++++++++++++++++++++++++

# remove (.) from "Sr_no" column
final_df['Sr_no']=final_df['Sr_no'].str.replace('.','')

# make "Sr_no" as index
final_df.set_index('Sr_no', inplace=True)

# Change the datatype of column as datetime
pd.to_datetime(final_df['release_date'])

# make a csv file from final_df
final_df.to_csv('games_data.csv')