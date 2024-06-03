from playwright.sync_api import sync_playwright
import re
import pandas as pd
import requests as rq
from bs4 import BeautifulSoup

url = "https://www.flipkart.com/search?q=laptop&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"

def getLaptopData(container):
    product = container.find('div',{'class':'KzDlHZ'})
    ProductName = product.text.split('-')[0].strip()

    star = container.find('div',{'class':'XQDdHH'})
    try:
        Stars = star.text
    except:
        Stars = 0

    Rating = container.find('span',{'class':'Wphh3N'})
    try:
        ratRev = re.findall(r'\d+,?\d*', Rating.text)
        Ratings = ratRev[0]
        Reviews = ratRev[1]
    
    except:
        Ratings = 0
        Reviews = 0
    

    CurrentPrice = container.find('div', {'class': 'Nx9bqj _4b5DiR'}).text

    mrp = container.find('div',{'class':'yRaY8j ZYYwLA'})
    try:
        MRP = mrp.text
    except:
        MRP = 0

    info = container.findAll('li', {'class':'J+igdf'})
    Processor = info[0].text
    Ram = info[1].text
    Oprating_System = info[2].text
    Storage = info[3].text
    Disply = info[4].text
    Warranty = info[5].text

    return{
        'ProductName': ProductName,
        'Stars': Stars,
        'Ratings':Ratings,
        'Reviews' : Reviews,
        'CurrentPrice': CurrentPrice,
        'Mrp': MRP,
        'Processor' : Processor,
        'Ram':Ram,
        'Oprating_system':Oprating_System,
        'Storage': Storage,
        'Display': Disply,
        'Warranty': Warranty

    }

if __name__ == '__main__':
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_load_state("networkidle")
        page.evaluate("() => window.scroll(0,document.body.scrollHeight)")
        page.screenshot(path="Flipkart2.png", full_page=True)
        flipHtml = page.inner_html("body")
        bs4FlipHtml = BeautifulSoup(flipHtml, "html.parser")

        containers = bs4FlipHtml.findAll('div',{'class':'tUxRFH'})

        laptops = []
        for container in containers:
            laptop_Data = getLaptopData(container)
            laptops.append(laptop_Data)

        df = pd.DataFrame(laptops)
        df.to_csv('laptopList.csv', index=False)
        print(df)
