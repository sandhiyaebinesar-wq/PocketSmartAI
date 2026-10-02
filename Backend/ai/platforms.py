from urllib.parse import quote_plus


PLATFORMS = {
    "Amazon": "https://www.amazon.in/s?k={query}",
    "Flipkart": "https://www.flipkart.com/search?q={query}",
    "IKEA": "https://www.ikea.com/in/en/search/?q={query}",
    "Swiggy": "https://www.swiggy.com/search?query={query}",
    "Zomato": "https://www.zomato.com/search?query={query}",
    "OYO": "https://www.oyorooms.com/search/?location={query}",
}


def create_search_link(platform, product):
    if platform not in PLATFORMS:
        platform = "Amazon"

    query = quote_plus(product)

    return PLATFORMS[platform].format(query=query)