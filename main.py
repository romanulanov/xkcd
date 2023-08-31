import os
import random
import requests
from dotenv import load_dotenv


def download_image(url, path):
    response = requests.get(f'{url}/info.0.json')
    response.raise_for_status()
    img_url = requests.get(response.json()['img'])
    img_url.raise_for_status()
    with open(path, 'wb') as file:
        file.write(img_url.content)
    return path
    

def get_comment(url):
    response = requests.get(f'{url}/info.0.json')
    response.raise_for_status()
    comment = response.json()['alt']
    return comment


def get_server_photo_and_hash(group_id, access_token, v, image_path):
    params = {'group_id': group_id, 'access_token': access_token, 'v': v}
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    response = requests.get(url, params=params)
    response.raise_for_status()
    upload_photo_url = response.json()['response']['upload_url']
    with open(image_path, 'rb') as file:
        files = {'photo': file, }
        response = requests.post(upload_photo_url, files=files)
        response.raise_for_status()
        photo_json = response.json()
    server, photo, hash = photo_json['server'], photo_json['photo'], photo_json['hash']
    return server, photo, hash


def save_photo(group_id, access_token, v, server, photo, hash):
    params = {'group_id': group_id, 'access_token': access_token, 'v': v, 'server': server, 'photo': photo, 'hash': hash}
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    response = requests.post(url, params=params)
    response.raise_for_status()
    for i in response.json()['response']:
        media_id = i['id']
        owner_id = i['owner_id']
    return media_id, owner_id


def post_photo(group_id, access_token, v, media_id, owner_id, comment):
    url = 'https://api.vk.com/method/wall.post'
    params = {'owner_id': f'-{group_id}', 'from_group':1, 'attachments':f'photo{owner_id}_{media_id}', 'access_token': access_token, 'v': v, 'message':comment}
    response = requests.get(url, params=params)
    response.raise_for_status()


def get_random_comix():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    count_comix = response.json()['num']
    num_comix = random.randint(1, count_comix)
    path = download_image(f'https://xkcd.com/{num_comix}/', f'{num_comix}.jpg')
    comment = get_comment(f'https://xkcd.com/{num_comix}/')
    return path, comment


def main():
    load_dotenv()
    group_id = os.environ["GROUP_ID"]
    access_token = os.environ["VK_TOKEN"]
    v = os.environ["V"]
    path, comment = get_random_comix()
    server, photo, hash = get_server_photo_and_hash(group_id, access_token, v, path)
    media_id, owner_id = save_photo(group_id, access_token, v, server, photo, hash)
    post_photo(group_id, access_token, v, media_id, owner_id, comment)
    os.remove(path)


if __name__=="__main__":
    main()
