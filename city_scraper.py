
import requests
from bs4 import BeautifulSoup
from unidecode import unidecode
import json


URLs = [
    'https://www.lonelyplanet.com/thailand/bangkok',
    'https://www.lonelyplanet.com/spain/andalucia/malaga-province',
    'https://www.lonelyplanet.com/thailand/phuket-the-andaman-coast',
    'https://www.lonelyplanet.com/italy/milan',
    'https://www.lonelyplanet.com/taiwan/taipei',
    'https://www.lonelyplanet.com/china/shanghai',
    'https://www.lonelyplanet.com/canada/vancouver',
    'https://www.lonelyplanet.com/usa/san-francisco',
    'https://www.lonelyplanet.com/usa/honolulu-and-waikiki',
    'https://www.lonelyplanet.com/norway/oslo',
    'https://www.lonelyplanet.com/germany/hamburg',
    'https://www.lonelyplanet.com/germany/berlin-brandenburg',
    'https://www.lonelyplanet.com/spain/barcelona',
    'https://www.lonelyplanet.com/thailand/andaman-coast/ko-phi-phi-don',
    'https://www.lonelyplanet.com/spain/mallorca',
    'https://www.lonelyplanet.com/spain/ibiza',
    'https://www.lonelyplanet.com/spain/aragon-basque-country-and-navarra/bilbao',
    'https://www.lonelyplanet.com/croatia/dubrovnik',
    'https://www.lonelyplanet.com/mexico/mexico-city',
    'https://www.lonelyplanet.com/switzerland/zurich',
    'https://www.lonelyplanet.com/france/paris',
    'https://www.lonelyplanet.com/indonesia/nusa-tenggara/gili-islands',
    'https://www.lonelyplanet.com/indonesia/bali',
    'https://www.lonelyplanet.com/nigeria/lagos',
    'https://www.lonelyplanet.com/egypt/cairo',
    'https://www.lonelyplanet.com/greece/cyclades/mykonos',
    'https://www.lonelyplanet.com/greece/athens',
    'https://www.lonelyplanet.com/greece/cyclades/santorini-thira',
    'https://www.lonelyplanet.com/italy/rome',
    'https://www.lonelyplanet.com/italy/florence'
]


def search_lonely_planet(city_name, country_name):
    """ This function takes POST data when a new destination is added"""

    city_name = unidecode(city_name.lower())
    country_name = unidecode(country_name.lower())

    if requests.get(f'https://www.lonelyplanet.com/{country_name}/{city_name}').status_code == 200:
        city_url_to_scrape = f'https://www.lonelyplanet.com/{country_name}/{city_name}'
        return city_url_to_scrape

    # If city URL on lonely-planet isn't as straighforward, SEARCH the site:

    # Bypassing Response [403] with headers:
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        'referer': 'https://www.google.com/'
    }

    page = requests.get(
        f'https://www.lonelyplanet.com/search?q={city_name}', headers=header)
    soup = BeautifulSoup(page.content, 'html.parser')

    city_url_to_scrape = ''
    search_results = soup.find_all(
        'a', class_='jsx-1866906973 ListItemTitleLink')
    if len(search_results):
        for result in search_results:
            # check if BOTH city and country match user's POST request:
            if (city_name in (unidecode(result.text.lower())) and (unidecode(result['href'].split('/')[0]) == country_name)):
                city_url_to_scrape = f"https://www.lonelyplanet.com/{result['href']}"
                break

    return city_url_to_scrape


cities = []
for index, city_url in enumerate(URLs):
    # Parse page
    print(f'{index+1}/{len(URLs)}: {city_url}')
    page = requests.get(city_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # City
    city = soup.find_all(
        'h1', class_='text-3xl font-display md:text-6xl leading-tighter font-semibold font-bold text-blue mb-6 lg:mb-8')[0].text

    # Continent & Country:
    location = soup.find_all(
        'a', class_='link-underline transition-colors ease-out cursor-pointer text-black hover:text-blue')
    continent = location[0].text
    country = location[1].text
    # State or communidad. The US will be populated with states for example, Spain with communidades
    state = location[2].text if len(location) == 3 else ''

    # Description
    description = soup.find_all(
        'div', class_='readMore_content___5EuR relative overflow-hidden max-h-96 is-max wysiwyg')[0].p.text

    # Top 3 attractions (names):
    top_3_attractions = [x.text for x in soup.find_all(
        'a', class_='text-xl font-semibold')[:3]]

    # Cover image
    image = soup.find_all('meta')[10]['content']

    print(f'-------{city} scraped.')

    cities.append({
        'model': 'cities.city',
        'pk': index + 3,
        'fields': {
            'name': city,
            'country': country,
            'state': state,
            'continent': continent,
            'description': description,
            'top_3_attractions': top_3_attractions,
            'image': image
        }
    })

# print(cities)

with open("cities.json", "w") as outfile:
    json.dump(cities, outfile)
