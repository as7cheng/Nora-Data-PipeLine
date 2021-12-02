"""
File to send message to Flask
"""
import json
import requests

with open('/var/task/security.json', 'rb') as f:
    DATA = json.load(f)
    SLACK_URL = DATA['SLACK_URL']

HEADERS = {'Content-Type': 'application/json'}

def send_log(message) -> None:
    """
    Function to create reqeust and send message to Flask
    """
    slack_data = json.dumps({'text': message}).encode('utf-8')
    try:
        response = requests.post(SLACK_URL, data=slack_data, headers=HEADERS)
        print('Slack connection', response.content.decode('utf-8'))
    except requests.exceptions.Timeout:
        print('Slack post timeout.')
    except requests.exceptions.RequestException as error:
        print(error)
