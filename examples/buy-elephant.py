import logging

from aiohttp import web
from aioalice import Dispatcher, get_new_configured_app, types
from aioalice.dispatcher import MemoryStorage


WEBHOOK_URL_PATH = '/my-alice-webhook/'  # webhook endpoint

WEBAPP_HOST = 'localhost'
WEBAPP_PORT = 3001


logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)

# Создаем экземпляр диспетчера и подключаем хранилище в памяти
dp = Dispatcher(storage=MemoryStorage())


ele_link = 'https://market.yandex.ru/search?text=слон'
# Заготавливаем кнопку на всякий случай
OK_Button = types.Button('Ладно', url=ele_link)


# Функция возвращает две подсказки для ответа.
async def get_suggests(user_id):
    # Получаем хранимые в памяти данные
    data = await dp.storage.get_data(user_id)
    # Не исключаем, что данные могут оказаться пустыми, получаем список подсказок
    user_suggests = data.get('suggests', [])
    # Выбираем две первые подсказки из массива.
    suggests = [text for text in user_suggests[:2]]
    # Если осталась только одна подсказка, предлагаем
    # подсказку (кнопку) со ссылкой на Яндекс.Маркет.
    if len(suggests) < 2:
        suggests.append(OK_Button)
    # Обновляем данные в хранилище, убираем первую подсказку, чтобы подсказки менялись
    await dp.storage.update_data(user_id, suggests=user_suggests[1:])
    return suggests


# Новая сессия. Приветствуем пользователя и предлагаем купить слона
# В этот хэндлер будут попадать только новые сессии
@dp.request_handler(func=lambda areq: areq.session.new)
async def handle_new_session(alice_request):
    user_id = alice_request.session.user_id
    await dp.storage.update_data(
        user_id, suggests=[
            "Не хочу..",
            "Не буду...",
            "Отстань!!",
        ]
    )
    logging.info(f'Initialized suggests for new session!\nuser_id is {user_id!r}')

    # В кнопки нужно передать список из строк или готовых кнопок
    # Строки будут преобразованы в кнопки автоматически
    suggests = await get_suggests(user_id)
    return alice_request.response('Привет! Купи слона!', buttons=suggests)


# Пользователь соглашается - команда соответствует одному из слов:
@dp.request_handler(commands=['ладно', 'куплю', 'покупаю', 'хорошо', 'окей'])
async def handle_user_agrees(alice_request):
    # Отвечаем пользователю, что слона можно купить на Яндекс.Маркете
    # Ответ генерируется автоматически на основе запроса,
    # туда подставляются сессия и версия апи.
    # Текст ответа - единственный необходимый параметр
    # Кнопки передаем по ключевому слову.
    return alice_request.response(f'Слона можно найти на Яндекс.Маркете!\n{ele_link}')


# Все остальные запросы попадают в этот хэндлер, так как у него не настроены фильтры
@dp.request_handler()
async def handle_all_other_requests(alice_request):
    # Всеми силами убеждаем пользователя купить слона,
    # предлагаем варианты ответа на основе текста запроса
    requst_text = alice_request.request.original_utterance
    suggests = await get_suggests(alice_request.session.user_id)
    return alice_request.response(
        f'Все говорят "{requst_text}", а ты купи слона!',
        buttons=suggests
    )


if __name__ == '__main__':
    app = get_new_configured_app(dispatcher=dp, path=WEBHOOK_URL_PATH)
    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)
