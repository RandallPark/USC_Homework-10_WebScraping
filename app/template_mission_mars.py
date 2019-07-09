# THIS WAS PREVIOUSLY YOUR JUPYTER NOTEBOOK
# Dependencies
import pandas as pd
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import time

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)


def scrape_info():
    browser = init_browser()
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')

    # Examine the results, then determine element that contains sought info
    print(soup.prettify())

    # results are returned as an iterable list
    news_title = soup.find('div', class_="content_title").text.strip()

    news_p = soup.find('div', class_="rollover_description_inner").text.strip()
    
    # Lets not crash the internet
    time.sleep(1)

    # Looking for the featured space picture
    # URL of page to be scraped 
    base_url = 'https://www.jpl.nasa.gov'
    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(img_url)


    # Gotta click the link where the full res img resides
    image = browser.find_link_by_partial_text('FULL IMAGE')
    print(image)
    image.click()

    # Lets not ring the alarms
    time.sleep(1)

    # Digging deeper to get that dang img URL 
    new_html = browser.html
    new_parse = BeautifulSoup(new_html, 'html.parser')

    grab_img = new_parse.find('div', class_="fancybox-inner")

    feat_src = (grab_img.find('img')['src'])

    mars_feat_img = f'{base_url}{feat_src}'
    browser.visit(mars_feat_img)

    # Boo!
    time.sleep(1)
    # Looking for the most recent Mars weather Tweet
    # URL of page to be scraped
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    twitter_html = browser.html
    response = requests.get(twitter_url)


    twitter_soup = BeautifulSoup(twitter_html, 'html.parser')

    tweets = twitter_soup.find('div', class_='content')

    mars_weather = tweets.find('p', class_='TweetTextSize').text
    print(mars_weather)

    # Lets not crash the internet
    time.sleep(1)
    #HEMISPHERE INFOOOO
    

    # CREATING MONGO DICTIONARY DATABASE 
    # Store data in a dictionary
    mars_mongo = {
        "NASA Mars News": news_title,
        "NASA Mars Info": news_p,
        "Mars Pic": mars_feat_img,
        "Mars Weather": mars_weather,
        # "Mars Hemisphere Pics" : hemisphere_one
        # "Mars Hemisphere Two" : hemisphere_two
        # "Mars Hemisphere Three" : hemisphere_three
        # "Mars Hemisphere Four" : hemisphere_four
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_mongo