from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from selenium import webdriver
import datetime as dt


def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_text = mars_soup(browser) 
    data={
        "news_title": news_title,
        "news_text": news_text,
        "featured_image": img(browser),
        "facts": mars_facts(),
        "hemispheres": hemis(browser),
        "last_modified": dt.datetime.now(),
    },
    browser.quit()
    return data


#     #scrape news article,
def mars_soup(browser):
    url_1 = "https://mars.nasa.gov/news/"
    browser.visit(url_1)
    html = browser.html
    news_scrape = BeautifulSoup(html, 'html.parser')
    soupy_news = news_scrape.select_one('ul.item_list, li.slide')
    #gather news article details
    news_title = soupy_news.find('h3').get_text()
    link_tag = soupy_news.find('a')
    news_link = link_tag['href']
    news_text = soupy_news.find("div", class_='article_teaser_body').get_text()
    return news_title, news_text

# scrape image,
def img(browser):
    url_2= 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url_2)
    soupy_jpg = browser.links.find_by_partial_text('FULL IMAGE').click()
    html = browser.html
    img_scrape = BeautifulSoup(html, 'html.parser')
    img_scrape_url= img_scrape.find("img", class_="fancybox-image").get('src')
    img_url= f'https://www.jpl.nasa.gov/{img_scrape_url}'
    return img_url

 #srcape table of mars facts ,
def mars_facts():
    marsdf = pd.read_html('https://space-facts.com/mars')[0]
    marsdf.columns=['Planetary Detail','Mars']
    marsdf.set_index('Planetary Detail', inplace=True)
    marsdf.to_html(classes='table table-striped')

#hemisphere info ,
def hemis(browser):
    url3='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url3)
    hemi_urls = []

    hemi_links = browser.find_by_css('a.product-item h3')

    for i in range(len(hemi_links)):
        hemis = {}
        browser.find_by_css('a.product-item h3')[i].click()
        sample = browser.links.find_by_text('Sample').first
        hemis['img_url'] = sample['href']
        hemis['title'] = browser.find_by_css('h2.title').text
        hemi_urls.append(hemis)
        browser.back(),
    return hemi_urls




if __name__ == "__main__":
    print (scrape_all())
   
