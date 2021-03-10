import os
import requests
import json
import random
from dotenv import load_dotenv


def getting_data_for_uploading_photos(access_token):
    url = 'https://api.vk.com/method/photos.getWallUploadServer?PARAMETERS'
    payload = {
            'access_token': access_token,
            'extended': 1,
            'v': '5.130'
    }
    response = requests.get(url, params=payload).json()
    data = {
        'upload_url': response['response']['upload_url'],
        'album_id': response['response']['album_id'],
        'user_id': response['response']['user_id']
    }
    return data


def getting_comic_book(data, filename, access_token):
    url = data['upload_url']

    with open(filename, 'rb') as file:
        files = {
            'photo': file
        }
        response = requests.post(url, files=files)
        result = json.loads(response.text)

    url = 'https://api.vk.com/method/photos.saveWallPhoto?PARAMETERS'
    params = {
        'server': result['server'],
        'photo': result['photo'],
        'hash': result['hash'],
        'access_token': access_token,
        'v':'5.130',
        'caption': 'тест'
    }
    request = requests.post(url, params=params)
    result = json.loads(request.text)
    return result


def uploading_an_image_to_group(result, access_token):
    group_id = '202809238'
    entrance = 0
    url = 'https://api.vk.com/method/wall.post?PARAMETERS'
    params = {
        'access_token': access_token,
        'group_id': group_id,
        'owner_id': '-{}'.format(group_id),
        'from_group': 1,
        'attachments': 'photo{}_{}'.format(result['response'][entrance]['owner_id'],\
        result['response'][entrance]['id']),
        'message': 'Комикс',
        'v':'5.130'
    }
    requests.post(url, params=params)


def getting_random_comic():
    num = random.randint(1, 2433)
    url = 'http://xkcd.com/{}/info.0.json'.format(num)
    filename = 'img/imq_{}.png'.format(num)
    response = requests.get(url)
    response = response.json()['img']
    response = requests.get(response)

    with open(filename, 'wb') as file:
       file.write(response.content)
    return filename


if __name__ == '__main__':
    load_dotenv()
    access_token = os.getenv('ACCESS_TOKEN')
    filename = getting_random_comic()
    data = getting_data_for_uploading_photos(access_token)
    result = getting_comic_book(data, filename, access_token)
    uploading_an_image_to_group(result, access_token)
    os.remove(filename) 
