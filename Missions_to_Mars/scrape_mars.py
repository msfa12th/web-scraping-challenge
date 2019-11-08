#!/usr/bin/env python
# coding: utf-8

# # Mission to Mars Web Scraping
# by Mary Brown

def scrape():

    # Dependencies
    from bs4 import BeautifulSoup
    import requests
    from splinter import Browser
    import pandas as pd

    Mars_Dict ={}

    # ### NASA Mars News
    page = requests.get("https://mars.nasa.gov/news/")
    soup = BeautifulSoup(page.content, 'html.parser')

    news_title=soup.find_all('div',class_='content_title')[0].text
    news_title = news_title.replace('\n','')
    news_title
    
    news_p=soup.find_all('div',class_='rollover_description_inner')[0].text
    news_p = news_p.replace('\n','')
    news_p

    Mars_Dict = {'news_title': news_title, 'news_p': news_p}

    # ### JPL Mars Space Images - Featured Image
    get_ipython().system('which chromedriver')

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    urlDomain = 'https://www.jpl.nasa.gov'
    urlPath = '/spaceimages/?search=&category=Mars'
    urlFull = urlDomain + urlPath
    browser.visit(urlFull)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    browser.click_link_by_partial_text('FULL IMAGE')
    fullImage=soup.find_all(id="full_image")   
    imagePath=fullImage[0]['data-fancybox-href']
    featured_image_url= urlDomain + imagePath
    featured_image_url
    Mars_Dict['featured_image_url'] = featured_image_url

    # ### Mars Weather
    tpage = requests.get("https://twitter.com/marswxreport?lang=en")
    tsoup = BeautifulSoup(tpage.content, 'html.parser')
    latestTweet=tsoup.find_all('p',class_='TweetTextSize')
    latestTweet[0].text
    mars_weather=latestTweet[0].text
    Mars_Dict['mars_weather'] = mars_weather

    # ### Mars Fact
    url = 'https://space-facts.com/mars'
    tables = pd.read_html(url)
    df=tables[2]
    df=df.rename(columns={0: "description",1: "value"})
    df=df.set_index('description')
    df.to_html('table.html')
    fact_dict = df.to_dict()
    Mars_Dict['mars_facts'] = fact_dict


    # ### Mars Hemispheres
    urlDomain = 'https://astrogeology.usgs.gov'
    urlPath = '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    urlFull = urlDomain + urlPath
    browser.visit(urlFull)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    itemLinks = soup.find_all('a',class_="itemLink product-item")
    itemLinks

    myList = []
    myKeys = ['title', 'img_url']
    myDict ={}
    myText = ""
    for item in itemLinks:
        myValues = []
        myLink = urlDomain + item['href']
        if item.text != "":
            myText = item.text
            
            if myText.endswith(' Enhanced'):
                myText = myText[:-len(' Enhanced')]
                
            myValues.append(myText)
            
            browser.visit(myLink)
            html = browser.html
            soup = BeautifulSoup(html, 'html.parser')
            subItem = soup.find_all('img',class_='wide-image')
            myValues.append(urlDomain + subItem[0]['src'])
            myDict = {myKeys[0]:myValues[0], myKeys[1]:myValues[1]}
            myList.append(myDict)
        
    print(myList)
    Mars_Dict['mars_hemisphere'] = myList

return Mars_Dict



