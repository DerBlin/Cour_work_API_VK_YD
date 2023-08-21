from urllib.parse import urlencode
import requests
from tqdm import tqdm
import json

app_id = '51728525'
oauth_base_url = 'https://oauth.vk.com/authorize'
params = {
    'client_id': app_id,
    'redirect_uri': 'https://oauth.vk.com/blank.html',
    'display': 'page',
    'scope': 'photos',
    'response_type': 'token'
}
oauth_url = f'{oauth_base_url}?{urlencode(params)}'
TOKEN = 'vk1.a.lsoSb55QwucYyKD6fxjcE7nQERq4rnY2VTyHeTFzpUfFkE3HF5pkV18b18Jmn1fQWfN60SKMljOepUO8YVKW1HxFt488HMIh_' \
        'AfpDgMptehsOJN-EytTuLIPCnMaCPtwHzuZTlfumJdZ6WYGuAamQUhBYFiC606mJPx7Fon9eqPXOaO7o_ZE-a64Hq_' \
        '983N7XOCmXx6mRODscdXWSydLRw'
owner_id = input('Введите id пользователя ВК:')
version = '5.131'


class VK_api:
    api_base_url = 'https://api.vk.com/method'

    def get_photos(token, owner_id):
        size_dict = {'s': 1, 'm': 2, 'o': 3, 'p': 4, 'q': 5, 'r': 6, 'x': 7, 'y': 8, 'z': 9, 'w': 10}
        size_dict_second = {1: 's', 2: 'm', 3: 'o', 4: 'p', 5: 'q', 6: 'r', 7: 'x', 8: 'y', 9: 'z', 10: 'w'}
        url_photo_list = []
        likes_list = []
        letter_list = []
        url_photo_dict = {}
        photos_URL = 'https://api.vk.com/method/photos.get'
        params = {
            'access_token': TOKEN,
            'v': version,
            'count': 5,
            'owner_id': owner_id,
            'album_id': 'profile',
            'extended': 1
        }
        response = requests.get(f'{photos_URL}', params=params)
        for el in response.json()['response']['items']:
            new_dict_type_url = {}
            if el['likes']['count'] in likes_list:
                likes_list.append(f"{el['likes']['count']}_{el['date']}")
            else:
                likes_list.append(el['likes']['count'])
            for size in el['sizes']:
                new_dict_type_url[size['type']] = size['url']
            new_list_type = []
            for key in new_dict_type_url.keys():
                new_list_type.append(size_dict[key])
            url_photo_list.append(new_dict_type_url[size_dict_second[sorted(new_list_type)[-1]]])
            url_photo_dict = dict(zip(likes_list, url_photo_list))
            letter_list.append(size_dict_second[sorted(new_list_type)[-1]])
        data = dict(zip(likes_list, letter_list))
        new_dict = {}
        new_list = []
        for el in likes_list:
            new_list.append(str(el) + '.jpg')
        new_dict['file_name'] = new_list
        new_dict['size'] = letter_list
        # Запись информации о фото в json-файл
        json_list = []
        for key, value in data.items():
            json_list.append({'file_name': key, 'size': value})
        with open('Photo_info.json', 'w') as outfile:
            json.dump(json_list, outfile)
        return url_photo_dict


class yandex_disk:

    def upload_photo(url_photo_dict):
        token_yandex_disk = input('Введите токен с Полигона Яндекс.Диска:')
        base_url_for_folder = 'https://cloud-api.yandex.net'
        # Создание папки на Яндекс диске
        headers = {
            "Authorization": f'OAuth {token_yandex_disk}'
        }
        params = {'path': 'Image_VK'}
        response = requests.put(f'{base_url_for_folder}/v1/disk/resources',
                                params=params,
                                headers=headers)
        # Загрузка фото в папку на диск
        for item in tqdm(url_photo_dict.items(), desc='Upload photo to the disk'):
            base_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
            headers = {"Authorization": token_yandex_disk}
            params = {'path': f'Image_VK/{item[0]}', 'url': f'{item[1]}'}
            requests.post(base_url, headers=headers, params=params)


VK_api.get_photos(TOKEN, owner_id)
yandex_disk.upload_photo(VK_api.get_photos(TOKEN, owner_id))





