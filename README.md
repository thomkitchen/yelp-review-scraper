# yelp-review-scraper
Web scraper that grabs all reviews for a business's yelp page and returns them as a string for parsing. Originally designed for a Natural Language Processing project
## Use
Import module into project. Use the get_review() functions by feeding it the Yelp URL of the business/product you want to get the reviews for as a parameter.
ex. get_review("http://yelp.url.of.business.com")
### Note
Runs on HTML naming conventions of Yelp. If they change their HTML/CSS structure, update the code at the marked locations