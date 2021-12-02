"""
File to fetch data from Yelp API through HTTP request
"""

import json
from urllib.error import HTTPError
import requests
import data_log
import get_update_offset


# Open the json file to get all info we need
with open('/var/task/security.json', 'rb') as f:
    DATA = json.load(f)
    YELP_API_HOST = DATA['YELP_API_HOST']
    YELP_API_KEY = DATA['YELP_API_KEY']
    CITY_API_HOST = DATA['CITY_API_HOST']
    CITY_API_KEY = DATA['CITY_API_KEY']

# Create the request header and request terms
YELP_HEADERS = {'Authorization': 'bearer %s' % YELP_API_KEY}
CITY_HEADERS = {'X-Api-Key': CITY_API_KEY}
TERMS = ['American', 'Chinese', 'French', 'German', 'Indian', 'Italian',
         'Japanese', 'Korean', 'Mexican', 'Portuguese']
CITIES = ['New York', 'Los Angeles', 'Seattle', 'Chicago', 'Philadelphia']

# Prompt message for data log sent to Slack
START_PROMPT = '------Start FETCHING data------'
END_PROMPT = '------Ended FETCHING data, '


def build_params(term, city, offset) -> dict:
    """
    Helper function to build parameters for api reqeust
    """
    return {
        'term': term,
        'location': city,
        'radius': 40000,
        'categories': 'Restaurants',
        'limit': 1,
        'offset': offset
    }


def request(url, param=None, headers=None) -> list:
    """
    Helper function to request data from api source
    """
    return requests.get(url, params=param, headers=headers).json()

def get_city_info(city) -> list:
    """
    Function to request city information
    """
    url = f'{CITY_API_HOST}{city}'
    return request(url, None, CITY_HEADERS)

def fetch() -> list:
    """
    Fuction to request data from data source
    """
    data_log.send_log(START_PROMPT)
    # Get current offset for API request
    offset = get_update_offset.handle_offset()
    response = []

    for term in TERMS:
        for city in CITIES:
            try:
                param = build_params(term, city, offset)
                res = request(YELP_API_HOST, param, YELP_HEADERS)
                if 'businesses' in res:
                    for business in res['businesses']:
                        business['metropolitan'] = city
                        business['term'] = term
                        population = get_city_info(city)[0]['population']
                        business['city_population'] = population
                        response.append(business)
            except HTTPError as error:
                print(error)
    data_log.send_log(f"{END_PROMPT}{len(response)} data items are done------")
    return response
