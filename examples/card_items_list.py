from aiohttp import web
from aioalice import Dispatcher, get_new_configured_app
from aioalice.types import Image, MediaButton, CardFooter

WEBHOOK_URL_PATH = '/my-alice-webhook/'  # webhook endpoint

WEBAPP_HOST = 'localhost'
WEBAPP_PORT = 3001

dp = Dispatcher()


# Если кнопка не передана, клик по изображению не даст ничего
# Если кнопка передана, в ней должен быть указан URL, который
# открывается по нажатию на изображение
# (каждому изображению в списке может быть присвоена кнопка)


@dp.request_handler()
async def handle_all_requests(alice_request):
    return alice_request.response_items_list(
        'Вот альбом изображений',
        'Это текст заголовка, который будет над списком изображений',
        [  # Список картинок Image или словарей
            {
                # Пример полностью из словаря
                "image_id": '987654/efa943ab0c03767ce857',
                "title": None,  # Не обязательно передавать текст в заголовок
                "description": "Описание картинки, которое тоже не обязательно",
                # Поле button можно вообще не передавать.
                # Но если его не передать, то нажатие на картинку не будет ничего делать
                "button": {
                    'text': 'Текст кнопки',
                    'url': 'https://github.com',
                    # payload передавать не обязательно
                    'payload': {'some': 'payload'}
                }
            },
            {
                # Пример, когда кнопка передается объектом
                "image_id": '908173/efa943ab0c03767ce857',
                "title": 'Заголовок картинки',
                "description": None,
                "button": MediaButton('Текст кнопки', 'https://google.ru', {'this_is': 'payload'})
            },
            # Image(image_id, title, description, button), где button можно опустить
            Image('123456/efa943ab0c03767ce857',
                  'Заголовок изображения',
                  'Описание изображения',
                  # Опускаем передачу третьего агрумента - никакого payload
                  # Можно вообще не передавать кнопку
                  MediaButton('Текст кнопки', 'https://yandex.ru'))
        ],
        # Футер можно не передавать вообще
        # Можно передать словарем {'text': 'текст футера', 'button': None} (кнопка MediaButton по желанию)
        # А можно передать просто текстом - тогда он не будет нажиматься
        CardFooter(
            'Текст футера (под списком изображений)',
            # Снова пропускаем payload
            MediaButton('Текст кнопки', 'https://example.com')
        )
    )


if __name__ == '__main__':
    app = get_new_configured_app(dispatcher=dp, path=WEBHOOK_URL_PATH)
    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)
