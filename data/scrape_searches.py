import requests
from unidecode import unidecode
from bs4 import BeautifulSoup


def search_lonely_planet(city_name, country_name):
    """ This function takes POST `/scrape/search/` data when a new 
        destination is searched, and returns a valid Lonely Planet URL.
    """
    print('searching.....')
    city_name = unidecode(city_name.lower())
    country_name = unidecode(country_name.lower())

    if requests.get(f'https://www.lonelyplanet.com/{country_name}/{city_name}').status_code == 200:
        city_url_to_scrape = f'https://www.lonelyplanet.com/{country_name}/{city_name}'
        return [city_url_to_scrape]

    # If city URL on lonely-planet isn't as straighforward, SEARCH the site:

    # Bypassing Response [403] with headers:
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        'referer': 'https://www.google.com/'
    }

    page = requests.get(
        f'https://www.lonelyplanet.com/search?q={city_name}', headers=header)
    soup = BeautifulSoup(page.content, 'html.parser')

    search_results = soup.find_all(
        # 'a', class_='jsx-1866906973 ListItemTitleLink')  # april 2022
        'a', class_='text-sm md:text-xl font-semibold text-link line-clamp-1')  # june 2022
    if len(search_results) == 0:
        return ''
    else:
        cities_urls_to_scrape = []
        for result in search_results:
            # without this extra if, returns all search results that match just the city
            if (unidecode(result['href'].split('/')[0]) == country_name):
                cities_urls_to_scrape.append(
                    f"https://www.lonelyplanet.com/{result['href']}")

        return cities_urls_to_scrape


# if len(search_results):
#     for result in search_results:
#         # check if BOTH city and country match user's POST request:
#         if (city_name in (unidecode(result.text.lower())) and (unidecode(result['href'].split('/')[0]) == country_name)):
#             city_url_to_scrape = f"https://www.lonelyplanet.com/{result['href']}"
#             break

# return city_url_to_scrape
