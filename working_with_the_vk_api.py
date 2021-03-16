import os
import requests
import random
from dotenv import load_dotenv
from checking_the_status_request import get_request_status


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
    return {
        'upload_url': response['response']['upload_url'],
        'album_id': response['response']['album_id'],
        'user_id': response['response']['user_id']
        }


def get_comic_book(information_for_uploading_photos, information_about_the_comic, access_token):
    url = information_for_uploading_photos['upload_url']

    with open(information_about_the_comic['filename'], 'rb') as file:
        files = {
            'photo': file
        }
        response = requests.post(url, files=files)
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
    return result


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
    get_request_status(response)
    number_comics = response.json()['num']
    num = random.randint(1, number_comics)
    url = 'http://xkcd.com/{}/info.0.json'.format(num)
    filename = 'img/imq_{}.png'.format(num)
    return {
        'url': url,
        'filename': filename
    }


def save_image_the_catalog(information_about_the_comic):
    response = requests.get(information_about_the_comic['url'])
    link_to_picture = response.json()['img']
    url_pictures = requests.get(link_to_picture)
    response = url_pictures
    get_request_status(response)
    with open(information_about_the_comic['filename'], 'wb') as file:
        file.write(url_pictures.content)


if __name__ == '__main__':
    try:
        os.makedirs('img', exist_ok=True)
        load_dotenv()
        access_token = os.getenv('ACCESS_TOKEN')
        group_id = os.getenv('GROUP_ID')
        information_about_the_comic = get_information_about_random_comics()
        save_image_the_catalog(information_about_the_comic)
        information_for_uploading_photos = get_information_for_uploading_photos(access_token)
        result = get_comic_book(information_for_uploading_photos, information_about_the_comic, access_token)
        send_an_image_to_group(result, access_token, group_id)
    finally:
        os.remove(information_about_the_comic['filename'])
