import requests
from bs4 import BeautifulSoup
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


def scrape_cities(urls=URLs, seed_data=False):
    cities = []
    for index, city_url in enumerate(urls):
        # Parse page
        print(f'{index+1}/{len(urls)}: {city_url}')
        page = requests.get(city_url)
        soup = BeautifulSoup(page.content, 'html.parser')

        # City
        city = soup.find_all(
            'h1', class_='text-3xl font-display md:text-6xl leading-tighter font-semibold font-bold text-blue mb-6 lg:mb-8')[0].text

        # Continent & Country:
        location = soup.find_all(
            # 'a', class_='link-underline transition-colors ease-out cursor-pointer text-black hover:text-blue')  # april 2022
            'a', class_='transition-colors ease-out cursor-pointer text-black hover:text-blue link-underline')  # june 2022
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

        fields = {
            'city': city,
            'country': country,
            'state': state,
            'continent': continent,
            'description': description,
            'top_3_attractions': top_3_attractions,
            'image': image
        }

        if seed_data:
            cities.append({
                'model': 'cities.city',
                'pk': index + 3,
                'fields': fields
            })
        else:
            cities.append(fields)

    return cities


# # Seed data
# cities = scrape_cities(seed_data=True)

# with open("cities.json", "w") as outfile:
#     json.dump(cities, outfile)
