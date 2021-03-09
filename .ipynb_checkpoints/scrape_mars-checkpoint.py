{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {},
   "outputs": [],
   "source": [
    "from splinter import Browser\n",
    "from bs4 import BeautifulSoup\n",
    "from webdriver_manager.chrome import ChromeDriverManager\n",
    "import pandas as pd\n",
    "from selenium import webdriver\n",
    "import datetime as dt"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "metadata": {},
   "outputs": [],
   "source": [
    "#scrape all\n",
    "def scrape_all():\n",
    "    executable_path = {'executable_path': ChromeDriverManager().install()}\n",
    "    browser = Browser('chrome', **executable_path, headless=True)\n",
    "    news_title, news_text = mars_soup(browser)\n",
    "    data={\n",
    "        \"news_title\": news_title,\n",
    "        \"news_text\": news_text,\n",
    "        \"featured_image\": img(browser),\n",
    "        \"facts\": mars_facts(),\n",
    "        \"hemispheres\": hemis(browser),\n",
    "        \"last_modified\": dt.datetime.now()\n",
    "    }\n",
    "    browser.quit()\n",
    "    return data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "metadata": {},
   "outputs": [],
   "source": [
    "#scrape news article\n",
    "def mars_soup(browser):\n",
    "    \n",
    "    url_1 = \"https://mars.nasa.gov/news/\"\n",
    "    browser.visit(url_1)\n",
    "    html = browser.html\n",
    "    news_scrape = BeautifulSoup(html, 'html.parser')\n",
    "\n",
    "    soupy_news = news_scrape.select_one('ul.item_list, li.slide')\n",
    "    soupy_news\n",
    "    #gather news article details\n",
    "\n",
    "    news_title = soupy_news.find('h3').get_text()\n",
    "    link_tag = soupy_news.find('a')\n",
    "    news_link = link_tag['href']\n",
    "    news_text = soupy_news.find(\"div\", class_='article_teaser_body').get_text()\n",
    "\n",
    "    return news_title, news_text\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "metadata": {},
   "outputs": [],
   "source": [
    "#scrape image\n",
    "def img(browser):\n",
    "    url_2= 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'\n",
    "    browser.visit(url_2)\n",
    "    soupy_jpg = browser.links.find_by_partial_text('FULL IMAGE').click()\n",
    "    html = browser.html\n",
    "    img_scrape = BeautifulSoup(html, 'html.parser')\n",
    "    img_scrape_url= img_scrape.find(\"img\", class_=\"fancybox-image\").get('src')\n",
    "    img_scrape_url\n",
    "    img_url= f'https://www.jpl.nasa.gov/{img_scrape_url}'\n",
    "    return img_url"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "metadata": {},
   "outputs": [],
   "source": [
    "#srcape table of mars facts \n",
    "def mars_facts():\n",
    "    marsdf = pd.read_html('https://space-facts.com/mars')[0]\n",
    "    marsdf.columns=['Planetary Detail','Mars']\n",
    "    marsdf.set_index('Planetary Detail', inplace=True)\n",
    "    marsdf.to_html(classes=\"table table-striped\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "metadata": {},
   "outputs": [],
   "source": [
    "#hemisphere info \n",
    "def hemis(browser):\n",
    "    url3='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'\n",
    "    browser.visit(url3)\n",
    "    hemi_urls = []\n",
    "\n",
    "    hemi_links = browser.find_by_css(\"a.product-item h3\")\n",
    "\n",
    "    for i in range(len(hemi_links)):\n",
    "        hemis = {}\n",
    "        browser.find_by_css(\"a.product-item h3\")[i].click()\n",
    "        sample = browser.links.find_by_text('Sample').first\n",
    "        hemis['img_url'] = sample['href']\n",
    "        hemis['title'] = browser.find_by_css(\"h2.title\").text\n",
    "        hemi_urls.append(hemis)\n",
    "        browser.back()\n",
    "    return hemi_urls"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 27,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "[WDM] - ====== WebDriver manager ======\n",
      "[WDM] - Current google-chrome version is 88.0.4324\n",
      "[WDM] - Get LATEST driver version for 88.0.4324\n",
      "[WDM] - Driver [/Users/lilycarbonara/.wdm/drivers/chromedriver/mac64/88.0.4324.96/chromedriver] found in cache\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\n",
      "\n",
      "{'news_title': \"NASA's Perseverance Drives on Mars' Terrain for First Time\", 'news_text': 'The first trek of the agency’s largest, most advanced rover yet on the Red Planet marks a major milestone before science operations get under way.', 'featured_image': 'https://www.jpl.nasa.gov/image/featured/mars3.jpg', 'facts': None, 'hemispheres': [{'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg', 'title': 'Cerberus Hemisphere Enhanced'}, {'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg', 'title': 'Schiaparelli Hemisphere Enhanced'}, {'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg', 'title': 'Syrtis Major Hemisphere Enhanced'}, {'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg', 'title': 'Valles Marineris Hemisphere Enhanced'}], 'last_modified': datetime.datetime(2021, 3, 8, 19, 10, 12, 38811)}\n"
     ]
    }
   ],
   "source": [
    "if __name__ ==\"__main__\":\n",
    "    print(scrape_all())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python (PythonData)",
   "language": "python",
   "name": "myenv"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
