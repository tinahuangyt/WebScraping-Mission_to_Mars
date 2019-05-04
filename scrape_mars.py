#!/usr/bin/env python
# coding: utf-8

#Import dependencies
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup as bs
import requests
import pymongo

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


#executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
#browser = Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_data = {}

    # ### NASA Mars News
    #Visit NASA Mars news website and scrape headlines
    nasa_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(nasa_url)
    html = browser.html
    soup = bs(html, 'html.parser')

    # Retrieve the latest element that contains news title and news paragraph
    article = soup.find("div", class_='list_text')
    nasa_headline = article.find('div', class_='content_title').text
    nasa_paragraph = article.find('div', class_='article_teaser_body').text

    print(nasa_headline)
    print(nasa_paragraph)
    mars_data["nasa_headline"] = nasa_headline
    mars_data["nasa_paragraph"] = nasa_paragraph


    # ### JPL Mars Space Images 
    #Visit JPL featured speace image website 
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)
    html = browser.html
    soup = bs(html, 'html.parser')

    # Retrieve current Featured Mars Image 
    image_url = soup.find("article", class_='carousel_item').a['data-fancybox-href']
    featured_image_url = "https://www.jpl.nasa.gov" + image_url
    print(featured_image_url)
    mars_data["featured_image_url"] = featured_image_url

    # ### Mars Weather
    #Visit Mars Weather twitter account
    twitter_url ="https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)
    html = browser.html
    soup = bs(html, 'html.parser')

    #Retrieve current Mars weather report
    tweets = soup.find("div", class_="stream")
    mars_weather = tweets.find("p").text
    print(mars_weather)
    mars_data["mars_weather"] = mars_weather


    # ### Mars Facts
    #Visit Mars Facts webpage and use Pandas to scrape fact table
    import pandas as pd 

    url = "https://space-facts.com/mars/"
    marsfact_df = pd.read_html(url)[0]

    #Convert to dataframe and clean up
    marsfact_df = marsfact_df.rename(columns={0:"Parameter",1:"Value"})
    marsfact_df = marsfact_df.set_index("Parameter")
    marsfact_df

    #Convert to html table string
    marsfact_html = marsfact_df.to_html()
    marsfact_html= marsfact_html.replace('\n','')
    marsfact_html
    mars_data['marsfact_html'] = marsfact_html


    # ### Mars Hemispheres
    #Visit USGS Astrogeology site to scrape image
    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_url)
    html = browser.html
    soup = bs(html, 'html.parser')

    #List of hemispheric names with links for the images
    hemi_list =[]

    hemi_all = soup.find_all("h3")

    for hemi in hemi_all:
        hemi_list.append(hemi.text)

    hemi_list


    hemisphere_image_urls = []
    hemi_dic = {}

    for hemi in hemi_list:
        
        browser.click_link_by_partial_text(hemi)
        html = browser.html
        soup = bs(html, 'html.parser')
        img = soup.find("div", class_='downloads')
        link = img.find('a')
        url = link['href']
        
        hemi_dic["title"] = hemi
        hemi_dic["img_url"] = url
        hemisphere_image_urls.append(hemi_dic)
        
        browser.back()
        
    print(hemisphere_image_urls)
    mars_data['hemisphere_image_urls'] = hemisphere_image_urls

    return mars_data

    print(mars_data)

#if __name__ == "__main__":
    #scrape()
