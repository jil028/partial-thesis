# import libraries
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from time import sleep
import googlemaps
from datetime import datetime


# scprape the yellow businesses
# there's a total of 130 pages in the crowdsourced account
# provide the root url
URL = 'https://www.openrice.com/zh/gourmet/bookmarkrestaurant.htm?userid=66275053&city=hongkong&bpcatId=880470&page'
# initialize an empty list
final_openrice = []
# loop in all pages
for page in range(1, 131):
    # html code rendered in javascript --> use selenium
    # initialize chrome driver
    s = Service('Enter the path to Chromedriver')
    driver = webdriver.Chrome(service = s)
    # glue the url
    driver.get(URL + '=' + str(page));
    #give time for all javascripts to be finished loading
    sleep(10)
    page = driver.page_source
    # create a soup object
    soup = BS(page, "lxml")
    
    # find each div for the restaurant
    div = soup.find('div', id = 'poiListing')


    # extract the restaurant's name
    # can't use class = 'title' because there are other tags with the same class    
    restaurant_name_rows = div.find_all('div', {'class': 'titleLine'})
    # initialize an empty list
    restaurant_name = []
    # loop in 
    for r in restaurant_name_rows:
        restaurant_name.append(r.text.strip())
        

    # extract the address
    address_rows = div.find_all('a', {'class': 'main_color2'})
    # initialize an empty list
    address = []
    # loop in all links and use findNextSibling to find the text (the address) after each link
    for a in range(len(address_rows)):
        temp_address = address_rows[a].findNextSibling(text = True)
        address.append(temp_address.strip())


    # extract the district
    # initialize an empty list
    district = []
    for d in address_rows:
        district.append(d.text.strip())
    

    # extract the rating
    rating_rows = div.find_all('div', {'class': 'FL txt_bold ML5'})
    # initialize an empty list
    rating = []
    # loop in all links and use findNextSibling to find the text (the address) after each link
    for i in rating_rows:
        # rating: two significant digits
        rating.append(i.text[1:5].strip())
    

    # extract the price range
    # use css selector to keep div(s) whose class is 'FL' only
    price_rows = div.select('div[class="FL"]')
    # initialize an empty list
    price = []
    for p in price_rows:
        price.append(p.text.strip())
 
    # save as a list
    temp_openrice = list(zip(restaurant_name, address, district, rating, price))
    # save the list generated by each iteration
    final_openrice.extend(temp_openrice)



# save as a data frame
df_openrice = pd.DataFrame(final_openrice, columns = ['restaurant_name', 'address', 'district', 'rating', 'price'])
# save to csv
df_openrice.to_csv('openrice_yellow.csv')



# scprape the blue businesses
# there's a total of 151 pages for the crowdsourced account
# provide the root url
URL = 'https://www.openrice.com/zh/gourmet/bookmarkrestaurant.htm?userid=66275053&city=hongkong&bpcatId=879105&page'
# initialize an empty list
final_openrice = []
# loop in all pages
for page in range(1, 152):
    driver = webdriver.Chrome(executable_path = '/Users/jiayili/chromedriver')
    driver.get(URL + '=' + str(page));
    #give time for all javascripts to be finished loading
    sleep(10)
    page = driver.page_source
    soup = BS(page, "lxml")
    
    # find each div for the restaurant
    div = soup.find('div', id = 'poiListing')


    # extract the restaurant's name    
    restaurant_name_rows = div.find_all('div', {'class': 'titleLine'})
    # initialize an empty list
    restaurant_name = []
    # loop in 
    for r in restaurant_name_rows:
        restaurant_name.append(r.text.strip())
        

    # extract the address
    address_rows = div.find_all('a', {'class': 'main_color2'})
    # initialize an empty list
    address = []
    # loop in all links and use findNextSibling to find the text (the address) after each link
    for a in range(len(address_rows)):
        temp_address = address_rows[a].findNextSibling(text = True)
        address.append(temp_address.strip())


    # extract the district
    # initialize an empty list
    district = []
    for d in address_rows:
        district.append(d.text.strip())
    

    # extract the rating
    rating_rows = div.find_all('div', {'class': 'FL txt_bold ML5'})
    # initialize an empty list
    rating = []
    # loop in all links and use findNextSibling to find the text (the address) after each link
    for i in rating_rows:
        # rating: two significant digits
        rating.append(i.text[1:5].strip())
    

    # extract the price range
    # use css selector to keep div(s) whose class is 'FL' only
    price_rows = div.select('div[class="FL"]')
    # initialize an empty list
    price = []
    for p in price_rows:
        price.append(p.text.strip())
 

    # save as a list
    temp_openrice = list(zip(restaurant_name, address, district, rating, price))
    # save the list generated by each iteration
    final_openrice.extend(temp_openrice)


# save as a data frame
df_openrice = pd.DataFrame(final_openrice, columns = ['restaurant_name', 'address', 'district', 'rating', 'price'])
# save to csv
df_openrice.to_csv('openrice_blue.csv')

