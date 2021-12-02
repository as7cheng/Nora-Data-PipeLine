"""
File to modify the fetched data and create new entris in qualified format
"""

from datetime import datetime
import fetch_data
from model import Business
import data_log

# Prompt message for data log sent to Slack
START_PROMPT = '------Start TRANSFORMING data items------'
END_PROMPT = '------Ended TRANSFORMING data items, '

def create(new_item) -> Business:
    """
    Helper function to create a new Business data entry
    """
    try:
        data_entry = Business(
            id=new_item['id'],
            name=new_item['name'],
            image=new_item['image'],
            url=new_item['url'],
            tags=new_item['tags'],
            rating=new_item['rating'],
            transaction=new_item['transaction'],
            price=new_item['price'],
            addr=new_item['addr'],
            city=new_item['city'],
            state=new_item['state'],
            zip_code=new_item['zip_code'],
            phone=new_item['phone'],
            timestamp=new_item['timestamp'],
            metropolitan=new_item['metropolitan'],
            term=new_item['term'],
            city_population=new_item['city_population']
        )
        return data_entry
    except KeyError as error:
        print(error)
    return None

def reformat(item) -> dict:
    """
    Helper function to process, orgnize and reformat the data item, return
    a formated data item that matches the Business' schema
    """
    # Formated data item
    new_item = {}
    # Business id
    new_item['id'] = item['id']
    # Business name
    new_item['name'] = item['name']
    # Business image_url
    new_item['image'] = item['image_url'] if 'image_url' in item else ''
    # Business url
    new_item['url'] = item['url'] if 'url' in item else ''
    # Business tags
    new_item['tags'] = [i['title'] for i in item['categories'][0:3]]
    # Business transaction
    new_item['transaction'] = item['transactions'] if 'transactions' in item else 'dine-in'
    # Business price
    new_item['price'] = item['price'] if 'price' in item else '$$'
    # Business rating
    new_item['rating'] = item['rating'] if 'rating' in item else 4
    # Business adress
    new_item['addr'] = ' '.join(item['location']['display_address'])
    # Business city
    new_item['city'] = item['location']['city']
    # Business state
    new_item['state'] = item['location']['state']
    # Business zip_code
    new_item['zip_code'] = item['location']['zip_code']
    # Business phone number
    new_item['phone'] = item['display_phone']
    # Business inserted time stamp
    new_item['timestamp'] = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    # Business metropolitan
    new_item['metropolitan'] = item['metropolitan']
    # Business cuisine
    new_item['term'] = item['term']
    # Population of the city where the business located
    new_item['city_population'] = item['city_population']
    return new_item


def transform() -> list:
    """
    Function to unpack, reformat fetched data items, and create a list of
    Business data entries
    """
    data_items = fetch_data.fetch()
    response = []
    data_log.send_log(START_PROMPT)
    for item in data_items:
        new_item = reformat(item)
        data_entry = create(new_item)
        if data_entry:
            response.append(data_entry)
        else:
            print(f"Data item {item['id']} cannot be transformed")
    data_log.send_log(f"{END_PROMPT}{len(response)} data entries are done------")
    return response
