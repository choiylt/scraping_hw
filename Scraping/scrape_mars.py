from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd

url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"


def scrape():
    mars_library = {}
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    news_title = soup.find_all('div', class_='content_title')[0].find('a').text.strip()
    news_p = soup.find_all('div', class_='rollover_description_inner')[0].text.strip()
    mars_library['news_title'] = news_title
    mars_library['news_p'] = news_p

    url1 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    response1 = requests.get(url1)
    soup1 = BeautifulSoup(response1.text, 'html.parser')
    half_addy = soup1.find_all('a', class_='fancybox')[0].get('data-fancybox-href').strip()

    Big_Pic = "https://www.jpl.nasa.gov"+half_addy
    mars_library['featured_image_url'] = Big_Pic

    url2 = "https://twitter.com/marswxreport?lang=en"
    response2 = requests.get(url2)
    soup2 = BeautifulSoup(response2.text, 'html.parser')

    weather = soup2.find_all(
        'p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')[0].text

    mars_library['mars_weather'] = weather

    url3 = 'https://space-facts.com/mars/'

    tables = pd.read_html(url3)
    df = tables[0]
    df.columns = ['Description', 'Values']

    mars_facts = df.to_html(justify='left')
    mars_library['mars_facts'] = mars_facts

    url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response4 = requests.get(url4)
    soup4 = BeautifulSoup(response4.text, 'html.parser')

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url4)

    html = browser.html

    soup4 = BeautifulSoup(html, "html.parser")
    results = soup4.find_all('h3')

    hemisphere_image_urls = []
    tempdict = {}

    for result in results:
        item = result.text
        browser.click_link_by_partial_text(item)
        html1 = browser.html
        soup5 = BeautifulSoup(html1, "html.parser")
        image = soup5.find_all('div', class_="downloads")[0].find_all('a')[0].get("href")
        tempdict["title"] = item
        tempdict["img_url"] = image
        hemisphere_image_urls.append(tempdict)

        tempdict = {}
        browser.click_link_by_text('Back')

    mars_library['hemisphere_image_urls'] = hemisphere_image_urls

    return mars_library