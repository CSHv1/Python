# AIM: TO BUILD A WEB SCRAPER FOR A FASHION WEBSITE
# OUTPUT TO A CSV WITH A TIMESTAMP COLUMN, THEN PLACE INTO G-DOC FOR SOME LEVEL OF COMPETITOR ANALYSIS?
# BONUS POINTS IF YOU CAN FIGURE OUT HOW TO SCHEDULE IT

# 1) Iterate through pages based on numbering system and site structure. Use this as an append.
# 2) Can then use a while loop to create numbers for pages, then you get to an error.
# 3) Combine all data pulls together as an appended DataFrame with the same elements
# 4) BONUS: Can I export to a Google Sheet?
# 5) Adding Categorisation & Gender based on page to enhance the web scraped dataset

import user_agents
import myt_category_pages
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random
import math
products_per_page = 60

# user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
# Essential in order to get past bot detection. Either this or, use something like fake agent
# https://stackoverflow.com/questions/61400692/how-to-bypass-bot-detection-and-scrape-a-website-using-python

final_df = pd.DataFrame(columns=['Day', 'Designer', 'Product Name', 'Price', 'Image', 'Link'])
urls_to_scrape = []

# GENERATE LISTING OF URLS BASED ON SITE STRUCTURE

for page in range(0, len(myt_category_pages.top_level_category)):

    root_url = myt_category_pages.top_level_category[page]
    k = requests.get(root_url, headers={"User-Agent": random.choice(user_agents.user_agent_list)})
    soup = BeautifulSoup(k.content, 'html.parser')  # Formats it pretty well tbh

    # Dynamic Expression for Pages to Scrape
    product_category_amount = int((soup.find("p", class_="amount amount-has-pages")).text.replace(" products", "").strip())
    pages_to_scrape = math.ceil(product_category_amount / products_per_page)
    urls_to_scrape.append(root_url)

    for i in range(pages_to_scrape):
        if i == 0:
            pass
        else:
            new_url = f"{root_url}?p={i}"
            urls_to_scrape.append(new_url)

for url in urls_to_scrape:

    time.sleep(2)

    k = requests.get(url, headers={"User-Agent": random.choice(user_agents.user_agent_list)})

    soup = BeautifulSoup(k.content, 'html.parser')  # Formats it pretty well tbh

    # Empty List Definitions
    designer_name_list = []
    product_title_list = []
    price_list = []
    product_image_list = []
    link_list = []

    # Expression for Designer Name :: DONE
    for designer in soup.find_all("span", class_="ph1"):
        designer_name_list.append(designer.text)

    # Expression for Product Title and Designer Name :: DONE
    for title in soup.find_all("a", class_="product-image"):
        product_title_list.append(title.get("title"))

    product_title_list = [x for x in product_title_list if x is not None]

    # Expression for Price :: DONE
    for price in soup.find_all("span", class_="price"):
        price_list.append(price)

    # Expression here removes promotional pricing for old price, only extracts current price
    price_list = [price.text for price in price_list if ('old-price' not in str(price))]
    price_list = [price.replace(',', '').replace('£', '').replace(' ', '') for price in price_list]

    for link in soup.find_all("a", class_="product-image"):
        link_list.append(link.get("href"))

    # Expression for Product Image ::
    for a in soup.find_all("img"):
        product_image_list.append(a.get("data-rollover"))

    product_image_list = [x.replace('//', '').replace('_b1.jpg', '.jpg') for x in product_image_list if x is not None]

    my_t_dict = {'Designer': designer_name_list,
                 'Product Name': product_title_list,
                 'Price': price_list,
                 'Image': product_image_list,
                 'Link': link_list}

    # Setting up for file

    df = pd.DataFrame(my_t_dict)
    df['Day'] = pd.to_datetime('now', utc=True).strftime("%Y-%m-%d")
    df = df[['Day', 'Designer', 'Product Name', 'Price', 'Image', 'Link']]
    final_df = pd.concat([final_df, df], axis=0)
    products_pulled_total = len(final_df)
    print(f"{url} has been scraped. Total Product Count: {products_pulled_total}. Size of DF: {len(my_t_dict)}")



# Done at the end to output to csv location
output_timestamp = pd.to_datetime('now', utc=True).strftime("%Y-%m-%d")
final_df.to_csv(f'{output_timestamp}_myt_product_scrape.csv', index=False, encoding='utf-8')
