from aiohttp import web
from aioalice import Dispatcher, get_new_configured_app
from aioalice.types import MediaButton

WEBHOOK_URL_PATH = '/my-alice-webhook/'  # webhook endpoint

WEBAPP_HOST = 'localhost'
WEBAPP_PORT = 3001

dp = Dispatcher()


# если в commands передать строку, то она автоматически
# будет превращена в список из одного элемента - строки
@dp.request_handler(commands='без кнопки')
async def handle_no_button_request(alice_request):
    return alice_request.response_big_image(
        'Показываю тебе картинку!',  # Текст
        '123456/efa943ab0c03767ce857',  # id изображения, загруженного через upload_image
        'Заголовок изображения',
        'Это описание изображения'
    )

# Если кнопка не передана, клик по изображению не даст ничего
# Если кнопка передана, в ней должен быть указан URL, который
# открывается по нажатию на изображение


@dp.request_handler()
async def handle_all_requests(alice_request):
    return alice_request.response_big_image(
        'Показываю тебе картинку с кнопкой!',  # Текст
        '123456/efa943ab0c03767ce857',  # id изображения, загруженного через upload_image
        'Заголовок изображения',
        'Это описание изображения',
        # вместо объекта класса MediaButton можно передать словарь
        # Поле payload может отсутствовать (третий агрумент)
        MediaButton('Текст кнопки', 'https://yandex.ru', {'some': 'payload'})
    )


if __name__ == '__main__':
    app = get_new_configured_app(dispatcher=dp, path=WEBHOOK_URL_PATH)
    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)
