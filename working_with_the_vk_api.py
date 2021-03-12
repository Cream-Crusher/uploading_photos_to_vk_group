import os
import requests
import random
from dotenv import load_dotenv


def get_data_for_uploading_photos(access_token):
    url = 'https://api.vk.com/method/photos.getWallUploadServer?'
    payload = {
            'access_token': access_token,
            'extended': 1,
            'v': '5.130'
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    response = response.json()
    data = {
        'upload_url': response['response']['upload_url'],
        'album_id': response['response']['album_id'],
        'user_id': response['response']['user_id']
    }
    return data


def get_comic_book(data, information_about_the_comic, access_token):
    url = data['upload_url']

    with open(information_about_the_comic['filename'], 'rb') as file:
        files = {
            'photo': file
        }
        response = requests.post(url, files=files)
        response.raise_for_status()
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
    response.raise_for_status()
    result = response.json()
    return result


def send_an_image_to_group(result, access_token):
    group_id = '202809238'
    entrance = 0
    url = 'https://api.vk.com/method/wall.post?'
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


def get_information_about_the_comic():
    try:
        os.mkdir('img')
    except:
        print()

    request = requests.get('https://xkcd.com//info.0.json')
    request.raise_for_status()
    number_comics = request.json()['num']
    num = random.randint(1, number_comics)
    url = 'http://xkcd.com/{}/info.0.json'.format(num)
    filename = 'img/imq_{}.png'.format(num)
    information_about_the_comic = {
        'url': url,
        'filename': filename
    }
    return information_about_the_comic


def send_comic_to_group(information_about_the_comic):
    response = requests.get(information_about_the_comic['url'])
    response.raise_for_status()
    response = response.json()['img']
    response = requests.get(response)
    response.raise_for_status()

    with open(information_about_the_comic['filename'], 'wb') as file:
        file.write(response.content)


if __name__ == '__main__':
    load_dotenv()
    access_token = os.getenv('ACCESS_TOKEN')
    information_about_the_comic = get_information_about_the_comic()
    send_comic_to_group(information_about_the_comic)
    data = get_data_for_uploading_photos(access_token)
    result = get_comic_book(data, information_about_the_comic, access_token)
    send_an_image_to_group(result, access_token)
    os.remove(information_about_the_comic['filename'])
