# Daily Pennsylvanian Headline Scraper

A simple web scraper to scan Featured headlines from [The Daily Pennsylvanian's home page](https://www.thedp.com/) and compare the scanned results with the headlines that appear on the [News section first page](https://www.thedp.com/section/news).

<i>(built using [this template](https://github.com/jlumbroso/basic-git-scraper-template))</i>

## Goal

I'm curious about the kinds of content The Daily Pennsylvanian frequently promotes. More specifically, I want to see how often the paper promotes articles that fall under the News category. Thus, this program outputs headlines that appear in the News section first page AND the Featured section on the home page.

## Implementation Details
The `scrape_featured_headlines()` method will grab all the headlines that appear under featured divs by looking for `div` elements with a `special-edition` class.

The `scrape_first_news_headlines()` method will navigate to the News section's first page and grab all the headlines that appear as `h3` elements with a `standard-link` class

Before printing output to the json file, the program will identify only the headlines that appear in both scraped sets. If no News category headlines are placed under the Features section, no headlines should be written to the json file.

## Additional Notes
Repo made for CIS 3500 HW2

<i> Emma Lee | 3/14/2024 </i>
