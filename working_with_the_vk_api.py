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
        get_request_status(response)
        result = response.json()

    url = 'https://api.vk.com/method/photos.saveWallPhoto?'
    params = {
        'server': result['server'],
        'photo': result['photo'],
        'hash': result['hash'],
        'access_token': access_token,
        'v':'5.130',
        'caption': 'тест'
    }
    response = requests.post(url, params=params)
    get_request_status(response)
    result = response.json()
    return response, result


def send_an_image_to_group(result, access_token, group_id):
    entrance = 0
    url = 'https://api.vk.com/method/wall.post?'
    params = {
        'access_token': access_token,
        'group_id': group_id,
        'owner_id': '-{}'.format(group_id),
        'from_group': 1,
        'attachments': 'photo{}_{}'.format(
            result['response'][entrance]['owner_id'],
            result['response'][entrance]['id']),
        'message': 'Комикс',
        'v': '5.130'
    }
    requests.post(url, params=params)


def get_information_about_random_comics():
    response = requests.get('https://xkcd.com//info.0.json')
    response.raise_for_status()
    number_comics = response.json()['num']
    num = random.randint(1, number_comics)
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


def get_request_status(response):
    response_details = response.json()
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
    get_request_status(response)
    response = response.json()
    return response, response['response']['upload_url']


if __name__ == '__main__':
    os.makedirs('img', exist_ok=True)
    load_dotenv()
    access_token = os.getenv('ACCESS_TOKEN')
    group_id = os.getenv('GROUP_ID')
    url, filename = get_information_about_random_comics()
    save_xkcd_comics(url, filename)

    try:
        response, upload_url = get_information_for_uploading_photos(access_token)
        response, result = get_comic_book(upload_url, filename, access_token)
        send_an_image_to_group(result, access_token, group_id)

    except KeyError:
        get_request_status(response)

    finally:
        os.remove(filename)
