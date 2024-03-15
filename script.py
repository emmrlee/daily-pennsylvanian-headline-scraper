"""
Scrapes a headline from The Daily Pennsylvanian website and saves it to a 
JSON file that tracks headlines over time.
"""

import os
import sys

import daily_event_monitor

import bs4
import requests
import loguru


def scrape_featured_headlines():
    """
    Scrapes the featured headlines from The Daily Pennsylvanian home page.

    Returns:
        list: The list of featured headline texts if found, otherwise an empty list.
    """
    req = requests.get("https://www.thedp.com")
    loguru.logger.info(f"Request URL: {req.url}")
    loguru.logger.info(f"Request status code: {req.status_code}")

    featured_headlines = [] # Initialize an empty list to store the headlines

    if req.ok:
        soup = bs4.BeautifulSoup(req.text, "html.parser")
        # Find all the featured divs
        target_divs = soup.find_all("div", class_="special-edition")
        # Grab the links from each featured div
        for target_div in target_divs:
            headline_link = target_div.find("a", class_="frontpage-link standard-link")
            headline = "" if headline_link is None else headline_link.text
            featured_headlines.append(headline)
            loguru.logger.info(f"Data point: {headline}")

    return featured_headlines

def scrape_first_news_headlines():
    """
    Scrapes the headlines from The Daily Pennsylvanian news section first page.

    Returns:
        list: The list of first page news headline texts if found, otherwise an empty list.
    """
    req = requests.get("https://www.thedp.com/section/news")
    loguru.logger.info(f"Request URL: {req.url}")
    loguru.logger.info(f"Request status code: {req.status_code}")

    first_news_headlines = [] # Initialize an empty list to store the headlines

    if req.ok:
        soup = bs4.BeautifulSoup(req.text, "html.parser")
        # Find all the headline headers
        target_divs = soup.find_all("h3", class_="standard-link")
        # Grab the links from each headline header
        for target_div in target_divs:
            headline_link = target_div.find("a")
            headline = "" if headline_link is None else headline_link.text
            first_news_headlines.append(headline)
            loguru.logger.info(f"Data point: {headline}")

    return first_news_headlines

if __name__ == "__main__":

    # Setup logger to track runtime
    loguru.logger.add("scrape.log", rotation="1 day")

    # Create data dir if needed
    loguru.logger.info("Creating data directory if it does not exist")
    try:
        os.makedirs("data", exist_ok=True)
    except Exception as e:
        loguru.logger.error(f"Failed to create data directory: {e}")
        sys.exit(1)

    # Load daily event monitor
    loguru.logger.info("Loading daily event monitor")
    dem = daily_event_monitor.DailyEventMonitor(
        "data/daily_pennsylvanian_headlines.json"
    )

    # Run scrape
    loguru.logger.info("Starting scrape")
    try:
        featured_headlines = scrape_featured_headlines()
    except Exception as e:
        loguru.logger.error(f"Failed to scrape featured headlines: {e}")
        featured_headlines = []
    try:
        first_news_headlines = scrape_first_news_headlines()
    except Exception as e:
        loguru.logger.error(f"Failed to scrape first news headlines: {e}")
        first_news_headlines = []

    # Save data
    if featured_headlines:
        for featured_headline in featured_headlines: 
            dem.add_today(featured_headline)
        dem.save()
        loguru.logger.info("Saved daily event monitor")
    if first_news_headlines:
        for first_news_headline in first_news_headlines: 
            dem.add_today(first_news_headline)
        dem.save()
        loguru.logger.info("Saved daily events monitor")

    def print_tree(directory, ignore_dirs=[".git", "__pycache__"]):
        loguru.logger.info(f"Printing tree of files/dirs at {directory}")
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            level = root.replace(directory, "").count(os.sep)
            indent = " " * 4 * (level)
            loguru.logger.info(f"{indent}+--{os.path.basename(root)}/")
            sub_indent = " " * 4 * (level + 1)
            for file in files:
                loguru.logger.info(f"{sub_indent}+--{file}")

    print_tree(os.getcwd())

    loguru.logger.info("Printing contents of data file {}".format(dem.file_path))
    with open(dem.file_path, "r") as f:
        loguru.logger.info(f.read())

    # Finish
    loguru.logger.info("Scrape complete")
    loguru.logger.info("Exiting")
