import os
import requests
import random
from dotenv import load_dotenv


def get_comic_book(upload_url, filename, access_token):

    with open(filename, 'rb') as file:
        files = {
            'photo': file
        }
        response = requests.post(upload_url, files=files)
        response_details = response.json()
        get_request_status(response_details)

    url = 'https://api.vk.com/method/photos.saveWallPhoto?'
    params = {
        'server': response_details['server'],
        'photo': response_details['photo'],
        'hash': response_details['hash'],
        'access_token': access_token,
        'v':'5.130',
        'caption': 'тест'
    }
    response = requests.post(url, params=params)
    response_details = response.json()
    get_request_status(response_details)
    return response_details


def send_an_image_to_group(owner_id, id, access_token, group_id):
    url = 'https://api.vk.com/method/wall.post?'
    params = {
        'access_token': access_token,
        'group_id': group_id,
        'owner_id': '-{}'.format(group_id),
        'from_group': 1,
        'attachments': 'photo{}_{}'.format(
            owner_id,
            id),
        'message': 'Комикс',
        'v': '5.130'
    }
    requests.post(url, params=params)


def get_information_about_random_comics():
    response = requests.get('https://xkcd.com//info.0.json')
    response.raise_for_status()
    number_of_all_comics = response.json()['num']
    num = random.randint(1, number_of_all_comics)
    url = 'http://xkcd.com/{}/info.0.json'.format(num)
    filename = 'img/imq_{}.png'.format(num)
    return url, filename


def save_xkcd_comics(url, falename):
    response = requests.get(url)
    link_to_picture = response.json()['img']
    response = requests.get(link_to_picture)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(response.content)


def get_request_status(response_details):
    if response_details.get('error'):
        raise requests.HTTPError(response_details['error']['error_code'])


def get_information_for_uploading_photos(access_token):
    url = 'https://api.vk.com/method/photos.getWallUploadServer?'
    payload = {
            'access_token': access_token,
            'extended': 1,
            'v': '5.130'
    }
    response = requests.get(url, params=payload)
    response_details = response.json()
    get_request_status(response_details)
    return response_details['response']['upload_url']


if __name__ == '__main__':
    os.makedirs('img', exist_ok=True)
    load_dotenv()
    entrance = 0
    access_token_vk = os.getenv('ACCESS_TOKEN')
    group_id_vk = os.getenv('GROUP_ID')
    url, filename = get_information_about_random_comics()
    save_xkcd_comics(url, filename)

    try:
        upload_url = get_information_for_uploading_photos(access_token_vk)
        result = get_comic_book(upload_url, filename, access_token_vk)
        owner_id = result['response'][entrance]['owner_id']
        comic_id = result['response'][entrance]['id']
        send_an_image_to_group(owner_id, comic_id, access_token_vk, group_id_vk)

    finally:
        os.remove(filename)
