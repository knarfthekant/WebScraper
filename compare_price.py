"""
The find_grocery.py script is designed to scrape grocery prices from various websites (Walmart, Costco, Food Basics) using Selenium.

Author: Frank Shan
"""

# pandas 
import pandas as pd

# multithreading
import concurrent.futures as cf

from scrape_fb import FoodBasicsScraper
from scrape_costco import CostcoScraper
from scrape_ll import LoblawsScraper


if __name__ == "__main__":
    input = input("Enter the grocery item you want to search for: ")
    fb = FoodBasicsScraper()
    ll = LoblawsScraper()

    
    # Use ThreadPoolExecutor to run the tasks concurrently
    with cf.ThreadPoolExecutor() as executor:
        # Submit tasks to the executor
        future_fb = executor.submit(fb.get_price, input)
        future_ll = executor.submit(ll.get_price, input)

        # Wait for the results
        cf.wait([future_fb, future_ll])
        fb_result = future_fb.result()
        ll_result = future_ll.result()

    df_fb = pd.DataFrame(fb_result, columns=['Product Name', 'Price'])
    df_ll = pd.DataFrame(ll_result, columns=['Product Name', 'Price'])
    # flattening the price column
    # Flatten price lists or strings, normalize whitespace, and extract the numeric value
    df_fb['Price'] = df_fb['Price'].apply(lambda x: x[0] if isinstance(x, list) else x)
    df_fb['Price'] = df_fb['Price'].replace(r'\s+', ' ', regex=True)
    df_fb['Price'] = df_fb['Price'].str.extract(r'(\d+\.\d+)')[0].astype(float)

    # Apply the same flattening and extraction to Loblaws data
    df_ll['Price'] = df_ll['Price'].apply(lambda x: x[0] if isinstance(x, list) else x)
    df_ll['Price'] = df_ll['Price'].replace(r'\s+', ' ', regex=True)
    df_ll['Price'] = df_ll['Price'].str.extract(r'(\d+\.\d+)')[0].astype(float)

    
    df_fb.sort_values(by='Price', ascending=True, inplace=True)
    df_fb.reset_index(drop=True, inplace=True)
    df_ll.sort_values(by='Price', ascending=True, inplace=True)
    df_ll.reset_index(drop=True, inplace=True)

    # Print the cleaned DataFrames
    print("Food Basics Results:")
    print(df_fb)
    print("\nLoblaws Results:")
    print(df_ll)
