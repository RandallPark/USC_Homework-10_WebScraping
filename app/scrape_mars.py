from bs4 import BeautifulSoup as bs
#import splinter
from splinter import Browser
import time
import datetime
import os
#Global variable for saving return from usgs_get_images function.
hemisphere_image_urls = []
# path = !which chromedriver

def get_path(target_file):
    path=os.getenv('PATH')
    for file_path in path.split(os.path.pathsep):
        file_path=os.path.join(file_path,target_file)
        if os.path.exists(file_path) and os.access(file_path,os.X_OK):
            return file_path

def init_browser():
    # Set the executable path and initialize the chrome browser in splinter
    #executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    path = get_path('chromedriver')
    executable_path = {'executable_path': path}
    browser = Browser("chrome", **executable_path)
    return browser

def nasa_news(browser):
    # Set URL for Nasa news
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)
    # Command line print out to verify program is running.
    print('-----Getting Nasa News-----')
    #assign string html splinter response to local variable
    nasa_html= browser.html

    #Create BeautifulSoup object out of webpage html
    soup = bs(nasa_html, 'html.parser')

    #Isolate unordered list containing news stories.
    nasa_news = soup.find('ul', class_='item_list')

    #Isolate the List Item/s from the 'ul' container
    news_stories = nasa_news.find_all('li')

    first_story = news_stories[0]
    ### #first_story
    # Identify and return title
    news_title = first_story.find('div', class_ = "bottom_gradient").h3.text
    # Identify and story summary
    news_p = first_story.find('div', class_ = "article_teaser_body").text

    # Get link for full Article (not required)
    news_link_div = first_story.find('div', class_='image_and_description_container')


    news_link = (news_link_div.find('a')['href'])
    #news_link

    # Print results for title and paragraph
    print('-------------')
    print(f'Title: {news_title}:')
    print(f'Discription: >>> {news_p} <<<')
    print('-------------')

    return (news_title, news_p, news_link)

def usgs_get_images(browser):
    # List to contain dictionary of 'title', 'image_url' values.
    global hemisphere_image_urls
    # if image urls not saved yet
    if not hemisphere_image_urls:
        browser = init_browser()
        
        # Set url for USGS
        usgs_start_url= 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

        #Go to initial page
        browser.visit(usgs_start_url)
        time.sleep(.01)
        print("------\nOpening Browser\n------")
        #List of WebDriveElements
        usgs_items = browser.find_by_css("a.itemLink h3")

        for i in range(len(usgs_items)):
            print(f"------\nLoop {i+1}\n------")
            usgs_items = browser.find_by_css("a.itemLink h3")
            usgs_items[i].click()
            time.sleep(.1)

            #From image page get URL for image.
            li_item = browser.find_by_css("div.downloads li").first
            to_soup = bs(li_item.html, "html.parser")
            usgs_img_url = to_soup.find('a')['href']
            
            #From image page get Title 
            title_item = browser.find_by_css("div.content h2").text
            #print items
            usgs_dict = { 'title' : title_item, 'img_url': usgs_img_url}
            hemisphere_image_urls.append(usgs_dict)
            #Go to initial page
            browser.visit(usgs_start_url)
            time.sleep(.1)

        print('Program Complete\n\nImages for:')
        for i in range(len(hemisphere_image_urls)):
            print(f'Found following images:\n{hemisphere_image_urls[i]["title"]}')

    # return image urls
    return hemisphere_image_urls

def scrape_info():
    browser = init_browser()
    news_title, news_p, news_link = nasa_news(browser)
    hemisphere_image_urls = usgs_get_images(browser)
    current_dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    scraped_data = {
        'hemisphere_image_urls' : hemisphere_image_urls,
        'news_title' : news_title,
        'news_p' : news_p,
        'news_link' : news_link,
        'time_of_scrape' : current_dt,
    }
    return scraped_data



