import logging

from aiohttp import web
from aioalice import Dispatcher, get_new_configured_app


logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)


WEBHOOK_URL_PATH = '/my-alice-webhook/'  # webhook endpoint

WEBAPP_HOST = 'localhost'
WEBAPP_PORT = 3001

dp = Dispatcher()


@dp.request_handler()
async def handle_all_requests(alice_request):
    1 / 0  # some unexpected error
    return alice_request.response('Hello world!')


# if any error inside handler occur
@dp.errors_handler()
async def the_only_errors_handler(alice_request, e):
    # Log the error
    logging.error('An error!', exc_info=e)
    # Return answer so API doesn't consider your skill non-working
    return alice_request.response('Oops! There was an error!')


if __name__ == '__main__':
    app = get_new_configured_app(dispatcher=dp, path=WEBHOOK_URL_PATH)
    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)
