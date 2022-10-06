import requests
from app.config import MAP_API_TOKEN
from io import BytesIO
from PIL import Image
from app.common import bot_db
from app.config import DEBUG_map_api
# import urllib

#функция для получения адреса по координатам
def get_address_from_coords(coords):
    PARAMS = {
        "apikey": MAP_API_TOKEN,
        "format": "json",
        "lang": "ru_RU",
        "kind": "house",
        "geocode": coords
    }

    try:
        r = requests.get(url="https://geocode-maps.yandex.ru/1.x/", params=PARAMS)
        json_data = r.json()
        coords = json_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]['Point']['pos']
        coords = coords.replace(' ', ',')
        
        # парсим адрес
        data = json_data["response"]["GeoObjectCollection"]["featureMember"][0][
            "GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"]['Components'][:]
        parsed_data = {}
        for i in data:
            parsed_data[i['kind']] = i['name']
        # print(parsed_data)

        # проверяем корректность
        if parsed_data['country'] == 'Россия' and parsed_data['locality'] == 'Калининград' and ('street' in parsed_data) and ('house' in parsed_data):
            address_str = json_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"][
                "GeocoderMetaData"]["AddressDetails"]["Country"]["AddressLine"]
            # print(address_str)
            return address_str, True, coords
        else:
            return "Не могу определить адрес по этой локации/координатам.\n\
        Отправьте мне адрес, локацию или координаты (долгота, широта):", False, 0

    except Exception as e:
        #единственное что тут изменилось, так это сообщение об ошибке.
        return "Не могу определить адрес по этой локации/координатам.\n\
            Отправьте мне адрес, локацию или координаты (долгота, широта):", False, 0
            
# конвертируем из PIL в Buffer
def pil_image_to_file(image, extension='JPEG', quality='web_low'):
    photoBuffer = BytesIO()
    image.convert('RGB').save(photoBuffer, extension, quality=quality)
    photoBuffer.seek(0)
    return photoBuffer

def get_url_complete_dynamic_map(poll_id):
    if DEBUG_map_api: print('get_url_complete_dynamic_map')
    # ll-центр можно не задавать
    # pt-метки
    # l=map - тип карты
    # z=1..19 масштаб карты
    locs = bot_db.get_poll_results_data(poll_id=poll_id)
    # print(r)
    if DEBUG_map_api: print('locs:', locs)
    pt = ''
    ll = ''
    if locs:
        l0=0
        l1=0
        for loc in locs:
            pt += loc+'~'
            l0 += float(loc.split(',')[0])
            l1 += float(loc.split(',')[1])
        pt = pt[:-1]
        l0=l0/len(locs)
        l1=l1/len(locs)
        ll=str(l0)+','+str(l1)
    
    url = f'yandex.ru/maps/?ll={ll}&pt={pt}&z=12&l=map'
    # url = urllib.parse.quote_plus(url)
    return url

# получаем изображение карты
def get_static_map_img(coords):
    if DEBUG_map_api: print('get_static_map_img')
    URL = f"https://static-maps.yandex.ru/1.x/?l=map&ll={coords}&pt={coords},pm2rdm&spn=0.004,0.004"
    response = requests.get(URL)
    
    # image = Image.open(BytesIO(response.content))
    # img_buffer = pil_image_to_file(image)
    
    # image.save('map_point.png')
    # from IPython.display import display
    # from IPython.display import Image as Img
    # display(Img('map_point.png'))
    # Image(image)
    
    return response.content
