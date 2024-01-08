from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd

# NASA Exoplanet URL
START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"

# Webdriver
browser = webdriver.Chrome("D:/Setup/chromedriver_win32/chromedriver.exe")
browser.get(START_URL)

time.sleep(10)

planets_data = []

# Define Exoplanet Data Scrapping Method
def scrape():

    for i in range(0,10):
        print(f'Scrapping page {i+1} ...' ) ###
        
        # BeautifulSoup Object     
        soup = BeautifulSoup(browser.page_source, "html.parser")##

        # Loop to find element using XPATH
        for ul_tag in soup.find_all("ul", attrs={"class", "exoplanet"}): ##

            li_tags = ul_tag.find_all("li") ##
           
            temp_list = []

            for index, li_tag in enumerate(li_tags):

                if index == 0:                   
                    temp_list.append(li_tag.find_all("a")[0].contents[0])##
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")

            planets_data.append(temp_list)

        # Find all elements on the page and click to move to the next page
        browser.find_element(by=By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()

# Calling Method    
scrape()

# Define Header
headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date"]

# Define pandas DataFrame   
planet_df_1 = pd.DataFrame(planets_data, columns=headers)

# Convert to CSV
planet_df_1.to_csv('scraped_data.csv',index=True, index_label="id")

#make a page request using the request module
page = requests.get(url)

# Parse Page
soup = bs(page.text,'html.parser')

# Get <table> with class = 'wikitable sortable'
star_table = soup.find_all('table', {"class":"wikitable sortable"})

total_table = len(star_table)


temp_list= []

# IMP NOTE: The page at the given URL is maintained by "wikipedia", which might be updated in future.
# Hence check the index number poperly for star_table[1]
# Currently, there are there 3 table with class = "class":"wikitable sortable" and "Field brown dwarfs" Table is the 2nd table
# Thus the index is 1
table_rows = star_table[1].find_all('tr')

for tr in table_rows:
    td = tr.find_all('td')
    row = [i.text.rstrip() for i in td]
    temp_list.append(row)

Star_names = []
Distance =[]
Mass = []
Radius =[]

print(temp_list)

for i in range(1,len(temp_list)):
    
    Star_names.append(temp_list[i][0])
    Distance.append(temp_list[i][5])
    Mass.append(temp_list[i][7])
    Radius.append(temp_list[i][8])

# Convert to CSV
headers = ['Star_name','Distance','Mass','Radius']  
df2 = pd.DataFrame(list(zip(Star_names,Distance,Mass,Radius,)),columns=['Star_name','Distance','Mass','Radius'])
print(df2)

df2.to_csv('dwarf_stars.csv', index=True, index_label="id")
