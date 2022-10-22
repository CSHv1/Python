import random
import time
import re
import math
import pandas as pd
import requests
from bs4 import BeautifulSoup
import myt_category_pages
import user_agents

products_per_page = 60

# Essential in order to get past bot detection. Either this or, use something like fake agent
# https://stackoverflow.com/questions/61400692/how-to-bypass-bot-detection-and-scrape-a-website-using-python

final_df = pd.DataFrame(columns=['Day',
                                 'Designer',
                                 'Product Name',
                                 'Price',
                                 'Image',
                                 'Link',
                                 'Category Link'])
urls_to_scrape = []

# GENERATE LISTING OF URLS BASED ON SITE STRUCTURE

for page in range(0, len(myt_category_pages.top_level_category)):

    root_url = myt_category_pages.top_level_category[page]
    k = requests.get(root_url, headers={"User-Agent": random.choice(user_agents.user_agent_list)})
    soup = BeautifulSoup(k.content, 'html.parser')  # Formats it pretty well tbh

    # Dynamic Expression for Pages to Scrape
    product_category_amount = int((soup.find("p", class_="amount amount-has-pages")).text.replace(" products", "").strip())
    # pages_to_scrape = 1
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
    df['Category Link'] = str(url)

    df = df[['Day',
             'Designer',
             'Product Name',
             'Price',
             'Image',
             'Link',
             'Category Link']]

    final_df = pd.concat([final_df, df], axis=0)
    products_pulled_total = len(final_df)
    print(f"{url} has been scraped. Total Product Count: {products_pulled_total}.")

# Final String Manipulation

# Gender Entry Creation


def gender_fn(url_val):

    if 'men' in url_val:
        return 'Mens'
    else:
        return 'Womens'


final_df['Gender'] = [gender_fn(x) for x in final_df['Category Link']]

# Hardcode currency to pounds, since we're pulling from the UK site
final_df['Currency'] = 'GBP'

# Extract top-level category from page here
pattern = '([a-z]{1,})(.)(html)'
final_df['Top Level Category'] = [re.search(pattern, x)[1].title() for x in final_df['Category Link']]


# Done at the end to output to csv location
output_timestamp = pd.to_datetime('now', utc=True).strftime("%Y-%m-%d")
final_df.to_csv(f'{output_timestamp}_myt_product_scrape.csv', index=False, encoding='utf-8')

