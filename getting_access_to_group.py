import os
import requests
from dotenv import load_dotenv


def getting_access():
    client_id = os.getenv('CLIENT_ID')
    payload = {
            'client_id' : client_id,
            'display': 'page',
            'scope': ['wall,groups,offline,photos'],
            'response_type': 'token',
            'v': 5.124,
            'state': 123456
    }
    response = requests.get('https://oauth.vk.com/authorize?', params=payload) 
    print(response.url)


if __name__ == '__main__':
    load_dotenv()
    getting_access()
