import os
import requests
from dotenv import load_dotenv
from working_with_the_vk_api import get_request_status


def get_access(client_id):
    payload = {
            'client_id' : client_id,
            'display': 'page',
            'scope': ['wall,groups,offline,photos'],
            'response_type': 'token',
            'v': 5.124,
            'state': 123456
    }
    response = requests.get('https://oauth.vk.com/authorize?', params=payload)
    response_details = response.json()
    get_request_status(response_details)
    print(response.url)


if __name__ == '__main__':
    load_dotenv()
    client_id = os.getenv('CLIENT_ID')
    get_access(client_id)

