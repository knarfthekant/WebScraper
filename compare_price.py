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
    costco = CostcoScraper()
    fb = FoodBasicsScraper()
    ll = LoblawsScraper()

    # Use ThreadPoolExecutor to run the tasks concurrently
    with cf.ThreadPoolExecutor() as executor:
        # Submit tasks to the executor
        future_fb = executor.submit(fb.get_price, input)
        future_costco = executor.submit(costco.get_price, input)
        future_ll = executor.submit(ll.get_price, input)

        # Wait for the results
        cf.wait([future_fb, future_costco, future_ll])
        print(future_costco.result())
        print(future_fb.result())
        print(future_ll.result())
    


