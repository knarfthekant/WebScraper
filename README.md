# Grocery Price Scraper

This Python project uses **Selenium** to scrape grocery product and pricing data from three major Canadian retailers: **Food Basics**, **Loblaws**, and **Costco**. The extracted data is processed and compared using **pandas**, providing a simple way to monitor and compare prices across stores for budget-conscious shoppers or data analysis tasks.

## Features

- **Automated web scraping** from dynamic, JavaScript-rendered pages
- Extracts **product names** and **prices** (what essentially matters)
- Cleans and structures data with `pandas` for easy analysis
- Compares products across multiple retailers to find the best prices

## Technologies Used

- `Python 3.8+`
- `Selenium`
- `pandas`
- `ChromeDriver`
- `undetected_chromedriver`

## Usage
When running the script, the grocery item will be prompted:
```Enter the grocery item you want to search for:```
Simply type the item you want to search for and let the bot do the rest for you!

## Notes
- Websites may change their structure over time; XPath/CSS selectors may require updates.
- The Web Scraper runs with undetected_chromedriver and mimics human browsing to avoid simple bot detection mechanisms (CAPTCHA). However, rate limiting and polite scraping practices are recommended to avoid being blocked.
