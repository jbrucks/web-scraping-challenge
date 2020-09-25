from splinter import Browser
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

# mars_parts = {}

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def mars_scrape():
    browser = init_browser()
    mars_parts = {}
# def mars_news_scrape():
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latesthttps://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_parts['news_title'] = soup.find('li', class_='slide').\
    find('div', class_='image_and_description_container').find('div', class_='list_text').\
    find('div', class_='content_title').find('a').text

    mars_parts['news_p'] = soup.find('li', class_='slide').\
    find('div', class_='image_and_description_container').find('div', class_='list_text').\
    find('div', class_="article_teaser_body").text

    # return mars_parts
     
# def feature_img_scrape():
    # browser = init_browser()
    photo_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(photo_url)    

    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)
    browser.click_link_by_partial_text('more info')
    html2 = browser.html

    photo_soup = BeautifulSoup(html2, 'html.parser')

    featured_image_url = photo_soup.find('figure', class_='lede').\
    find('a')['href']
    base_photo_url = 'https://www.jpl.nasa.gov/'
    
    mars_parts['feature_photo_url'] = base_photo_url + featured_image_url

    # return mars_parts


# def mars_weather():
    # browser = init_browser()
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    time.sleep(5)
    twitter_html = browser.html
    twitter_soup = BeautifulSoup(twitter_html, 'html.parser')

    mars_parts['mars_weather'] = twitter_soup.find('div', class_='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0').\
    find('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0').text

    # return mars_parts

# def mars_facts():
    # browser = init_browser()
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)
    time.sleep(5)
    facts_html = browser.html
    facts_soup = BeautifulSoup(facts_html, 'html.parser')

    tables = pd.read_html(facts_url)
    mars_facts_df = tables[0]
    mars_parts['mars_html_table'] = mars_facts_df.to_html(index=False, header=None)

    # return mars_parts

# def mars_hemis():
    # browser = init_browser()
    hemis_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemis_url)

    hemis_html = browser.html
    hemis_soup = BeautifulSoup(hemis_html, 'html.parser')

    all_hemis = hemis_soup.find_all('div', class_='description')

    hemisphere_img_urls = []

    for hemis in all_hemis:
        # hemisphere_img_urls = []

        base_url = "https://astrogeology.usgs.gov"
        title = hemis.find('h3').text
        img_url = hemis.find('a')['href']
        hem_url = base_url + img_url

        browser.visit(hem_url)
        time.sleep(5)
        hem_html = browser.html
        hem_soup = BeautifulSoup(hem_html, 'html.parser')
        hemis_full_link = hem_soup.find('li').find('a')['href']
    
        hemisphere_img_urls.append(dict({'title': title, 'img_url': hemis_full_link}
        # {'title': title[0], 'img_url': hemis_full_link[0]},
        # {'title': title[1], 'img_url': hemis_full_link[1]},
        # {'title': title[2], 'img_url': hemis_full_link[2]},
        # {'title': title[3], 'img_url': hemis_full_link[3]}
        ))
        
    mars_parts['hemisphere_img_urls'] = hemisphere_img_urls

    return mars_parts