import logging
from aiohttp import web
from aioalice import Dispatcher, get_new_configured_app
from aioalice.dispatcher import SkipHandler


logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)

WEBHOOK_URL_PATH = '/my-alice-webhook/'  # webhook endpoint

WEBAPP_HOST = 'localhost'
WEBAPP_PORT = 3001

dp = Dispatcher()


# Это обычный хэндлер. Через него мы будем пропускать
# все входящие запросы, чтобы записать их в лог / БД.
# Поэтому если вы используете FSM, не забудьте
# указать "все состояния" (звёздочка), чтобы хэндлер
# отрабатывал при любом состоянии (получать все запросы).
# Вот так: `@dp.request_handler(state='*')`
# SkipHandler можно использовать в любых хэндлерах запросов.

# Этот хэндлер регистрируем первым,
# чтобы он получал все входящие запросы
@dp.request_handler()
async def take_all_requests(alice_request):
    # Логгируем запрос. Можно записывать в БД и тд
    logging.debug('New request! %r', alice_request)
    # Поднимаем исключение, по которому обработка перейдёт
    # к следующему хэндлеру, у которого подойдут фильтры
    raise SkipHandler


# Если передать не список, а строчку, она будет
# автоматически преобразована в список из одного элемента
@dp.request_handler(commands='привет')
async def reply_hi(alice_request):
    logging.debug('Now processing Hi')
    return alice_request.response('И тебе не хворать!')


# Отрабатываем все остальные запросы
@dp.request_handler()
async def handle_all_requests(alice_request):
    logging.debug('Now processing any request')
    return alice_request.response('Hello some request!')


if __name__ == '__main__':
    app = get_new_configured_app(dispatcher=dp, path=WEBHOOK_URL_PATH)
    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)
