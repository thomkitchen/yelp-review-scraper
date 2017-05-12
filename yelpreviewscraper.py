#
# Name:        Yelp Review Scraper
# Purpose:      Gather reviews from yelp page
#
# Author:      Thom Kitchen
#
# Created:     10/29/2014
# Last Modified: 03/26/2015
# Copyright:   (c) thom 2014
# Licence:     To Kill
#

import urllib3
import bs4
import sys

http = urllib3.PoolManager()


def get_reviews(url):
    """Get all reviews from a yelp url, return as string.

    Args:
        url: A url, pointing to the reviews for a product on yelp.

    Returns:
        List[2]: First element is the product name.
                 Second element is a string containing all reviews.
    """
# Empty string to hold reviews and bool to trigger
# cycle through pages of reviews
    reviews = ''
    has_next_page = False
# The calls to the web page and feeding those results into
# BeautifulSoup searching for reviews and next page button.
# Added exception handling
    try:
        response = http.request('GET', url)
    except urllib3.exceptions.HTTPError, e:
        print('HTTPError = ' + str(e))
        return
    except Exception, e:
        print("Error = " + str(e))
        return

    soup = bs4.BeautifulSoup(response.data)
    next_page_button = soup.findAll('a',
                                    {"class": "page-option prev-next next"})
    review_content = soup.findAll('p', {"itemprop": "description"})

# Grabs the product name to return in a list along with the reviews

    product_name = soup.select('h1.biz-page-title')[0].text


# Error check: CSS selector for reviews. may have changed
    if(len(review_content)) == 0:
        print("An error has occured. No review content was found.")
        return

# Check if there is a next page button, if so trigger review cycling
    if len(next_page_button) != 0:
        has_next_page = True

# Copies content of the CSS selector for reviews into a string object
    for node in review_content:
        reviews += node.text

# Routine for handling multiple pages of reviews
# to concat all into a single string object
    page_num = 1
    while has_next_page:
        response = http.request('GET', (url + "?start=" + str(page_num*40)))
        soup = bs4.BeautifulSoup(response.data)
        next_page_button = soup.findAll('a',
                                        {"class":
                                         "page-option prev-next next"})
        review_content = soup.findAll('p', {"itemprop": "description"})

        for node in review_content:
            reviews += node.text + '\n\n'

        if len(next_page_button) == 0:
            has_next_page = False
        page_num = page_num + 1

    return product_name.strip(), reviews
