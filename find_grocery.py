"""
The find_grocery.py script is designed to scrape grocery prices from various websites (Walmart, Costco, Food Basics) using Selenium.

Author: Frank Shan
"""

import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# pandas and randomization
import pandas as pd
import time
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
# multithreading
from concurrent.futures import ProcessPoolExecutor
import concurrent.futures


def get_fb_price(input):
    driver = uc.Chrome()
    driver.get("https://www.foodbasics.ca")
    try:
        driver.find_element(By.XPATH, '//button[@id="onetrust-reject-all-handler"]').click()
    except NoSuchElementException:
        pass # No cookie banner found, continue

    def locate_fb_search_box():
        return WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@placeholder="Search products"]'))
        )
    try:
        # wait up to 3 seconds for the search box to be present
        search_box = locate_fb_search_box()
    except TimeoutException:
        print("Search box did not load in time, retrying...")
        driver.refresh()
        search_box = locate_fb_search_box()

    time.sleep(random.uniform(0.5, 1))
    driver.execute_script("arguments[0].scrollIntoView();", search_box)
    time.sleep(random.uniform(0.5, 1))
    search_box.click()
    for char in input:
        search_box.send_keys(char)
        time.sleep(random.uniform(0.05, 0.2))
    search_box.send_keys(Keys.ENTER)
    
    results = []
    
    time.sleep(5)
    elements = driver.find_elements(By.XPATH, '//div[contains(@class, "tile-product")]')
    for element in elements:
    # re-locate the product elements to ensure they are present
        product_name = element.find_element(By.XPATH, './/div[contains(@class, "head__title")]').text
        product_price = element.find_element(By.XPATH, './/div[contains(@class, "pricing__sale-price")]').text
        results.append((product_name, product_price)) 
    return results

def get_costco_price(input):
    driver = uc.Chrome()
    driver.get("https://www.costco.ca")

    try:
        # wait up to 3 seconds for the search box to be present
        search_box = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@aria-label="Search Costco"]'))
        )
    except TimeoutException:
        print("Search box did not load in time, retrying...")
        driver.refresh()
        search_box = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@aria-label="Search Costco"]'))
        )
    time.sleep(random.uniform(0.5, 1))
    driver.execute_script("arguments[0].scrollIntoView();", search_box)
    time.sleep(random.uniform(0.5, 1))
    search_box.click()
    for char in input:
        search_box.send_keys(char)
        time.sleep(random.uniform(0.05, 0.2))
    search_box.send_keys(Keys.ENTER)
    
    try:
        # wait up to 10 seconds for products to be present
        products = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "mui-ge5uuv")]'))
        )
    except TimeoutException:
        print("Products did not load in time.")
        return
    
    results = []
    for product in products:
        try:
            product_name = product.find_element(By.XPATH, './/h3[contains(@data-testid, "Text_ProductTile")]').text
            product_price = product.find_element(By.XPATH, './/div[contains(@data-testid, "Text_Price")]').text
        except NoSuchElementException:
            print("Product name or price not found.")
            continue
        results.append((product_name, product_price))
    return results

def get_ll_price(input):
    driver = uc.Chrome()
    driver.get("https://www.loblaws.ca/en")
    try:
        driver.find_element(By.XPATH, '//button[@id="onetrust-reject-all-handler"]').click()
    except NoSuchElementException:
        pass # No cookie banner found, continue

    def locate_fb_search_box():
        return WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Search for Product"]'))
        )
    try:
        # wait up to 3 seconds for the search box to be present
        search_box = locate_fb_search_box()
    except TimeoutException:
        print("Search box did not load in time, retrying...")
        driver.refresh()
        search_box = locate_fb_search_box()

    time.sleep(random.uniform(0.5, 1))
    driver.execute_script("arguments[0].scrollIntoView();", search_box)
    time.sleep(random.uniform(0.5, 1))
    search_box.click()
    for char in input:
        search_box.send_keys(char)
        time.sleep(random.uniform(0.05, 0.2))
    search_box.send_keys(Keys.ENTER)
    
    results = []
    time.sleep(5)
    elements = driver.find_elements(By.XPATH, '//div[@class="css-yyn1h"]')
    for element in elements:
        name = element.find_element(By.XPATH, './/h3[@data-testid="product-title"]').text
        price = element.find_element(By.XPATH, './/span[@data-testid="regular-price"]|.//span[@data-testid="sale-price"]').text
        results.append((name, price))
    return results


if __name__ == "__main__":
    input = input("Enter the grocery item you want to search for: ")
    with ProcessPoolExecutor() as executor:
        # Submit tasks to the executor
        future_fb = executor.submit(get_fb_price, input)
        future_costco = executor.submit(get_costco_price, input)
        future_ll = executor.submit(get_ll_price, input)

        # Wait for the results
        concurrent.futures.wait([future_fb, future_costco, future_ll])
        print(future_costco.result())
        print(future_fb.result())
        print(future_ll.result())
    


