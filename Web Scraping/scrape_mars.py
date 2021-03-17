from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd



def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    
    executable_path = {"executable_path": r"C:\Users\15037\Downloads\chromedriver_win32\chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    # NOTE: we're using the chromedriver approach for another example,
    # but we could certainly use the requests library as well.
    browser = init_browser()
    mars_dict = {}

    ### NASA Mars News

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html

    soup = BeautifulSoup(html, 'html.parser')

    # Examine the results, then determine element that contains sought info
    # results are returned as an iterable list
    results = soup.find('div', class_='slide')

    mars_dict["news_title"] = results.find('div', class_='content_title').text.strip()

    mars_dict["news_p"] = results.find('div', class_='rollover_description_inner').text.strip()

    # ### JPL Mars Space Images - Featured Image

    # URL of page to be scraped
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    elems = browser.find_by_tag("img")
    mars_dict["featured_image_url"] = None
    for e in elems:
        if mars_dict["featured_image_url"] == None:
            mars_dict["featured_image_url"] = e["data-src"]

    # ### Mars Facts

    url = 'https://space-facts.com/mars/'

    tables = pd.read_html(url)

    type(tables)

    df = tables[0]

    html_table = df.to_html()

    html = html_table.replace('\n', '')

    soup = BeautifulSoup(html, 'html.parser')

    Tr = []
    for tr in soup.find_all('tr'):
        Td = []
        for td in tr.find_all('td'):
            Td.append(td.text)
        if Td:
            Tr.append(Td)

    mars_dict["mars_facts"] = Tr

    # ### Mars Hemispheres

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    # # Retrieve page with the requests module
    browser.visit(url)
    html = browser.html

    # # Create BeautifulSoup object
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find_all('a', class_='itemLink product-item')
    print(results)
    hemisphere_image_urls = []

    title = None
    image = None

    for result in results:

        if not title:
            try:
                title = result.find('h3').text
            except Exception as e:
                print(e)
        
        if not image:
            try:
                image = 'https://astrogeology.usgs.gov/'
                image += result.find('img', class_="thumb")['src']
            except Exception as e:
                print(e)

        if (title and image):

            hem_dict = {
                'title' : title,
                'img_url' : image
            }

            hemisphere_image_urls.append(hem_dict)

            title = None
            image = None

    mars_dict["hemispheres"] = hemisphere_image_urls
    
    return mars_dict

