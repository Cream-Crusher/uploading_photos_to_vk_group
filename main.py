import os
import requests
import json
import random
import time


def комент():
    url = 'http://xkcd.com/353/info.0.json'
    response = requests.get(url)
    response = response.json()['alt']


def скачка_url(url):
    filename = 'img/imq.png'
    response = requests.get(url)

    with open(filename, 'wb') as file:
        file.write(response.content)


def группы():
    access_token = os.getenv('ACCESS_TOKEN')
    payload = {
            'access_token': access_token,
            'extended': 1,
            'v': '5.130'
    }
    response = requests.get('https://api.vk.com/method/groups.get?PARAMETERS', params=payload)
    print(response.url)


def доступ():#
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


def адрес_для_загрузки():
    url = 'https://api.vk.com/method/photos.getWallUploadServer?PARAMETERS'
    access_token = os.getenv('ACCESS_TOKEN')
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


def загрузка_фото(data, filename):
    entrance = 0
    url = data['upload_url']
    group_id = '202809238'
    access_token = os.getenv('ACCESS_TOKEN')

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
    url = 'https://api.vk.com/method/wall.post?PARAMETERS'
    params = {
        'access_token': access_token,
        'group_id': group_id,
        'owner_id': '-{}'.format(group_id),
        'from_group': 1,
        'attachments': 'photo{}_{}'.format(result['response'][0]['owner_id'], result['response'][0]['id']),
        'message': 'тест',
        'v':'5.130'
    }
    request = requests.post(url, params=params)
    print(request.url)


def скачивание_рандомного_комикса():
    num = random.randint(1, 2433)
    url = 'http://xkcd.com/{}/info.0.json'.format(num)
    filename = 'img/imq_{}.png'.format(num)
    response = requests.get(url)
    response = response.json()['img']
    response = requests.get(response)

    with open(filename, 'wb') as file:
       file.write(response.content)
    return filename


def удаление_картинки(filename):
    time.sleep(1)
    os.remove(filename) 


if __name__ == '__main__':
    access_token = os.getenv('ACCESS_TOKEN')
    filename = скачивание_рандомного_комикса()
    #скачка_url(url)
    #комент()
    #доступ()
    #группы()
    data = адрес_для_загрузки()
    загрузка_фото(data, filename)
    удаление_картинки(filename)
