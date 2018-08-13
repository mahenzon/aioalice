import asyncio
import logging

from aioalice import Dispatcher

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)


# Provide your own skill_id and token!
SKILL_ID = '12a34567-c42d-9876-0e3f-123g55h12345'
OAUTH_TOKEN = 'OAuth AQAAAAABCDEFGHI_jklmnopqrstuvwxyz'

# You can create dp instance without auth: `dp = Dispatcher()`,
# but you'll have to provide it in request
dp = Dispatcher(skill_id=SKILL_ID, oauth_token=OAUTH_TOKEN)


async def check_quota_status_and_delete_image():
    try:
        # Use `await dp.get_images_quota(OAUTH_TOKEN)`
        # If token was not provided on dp's initialisation
        quota_before = await dp.get_images_quota()

        # Use `await dp.delete_image(image_id, SKILL_ID, OAUTH_TOKEN)`
        # If tokens were not provided on dp's initialisation
        success = await dp.delete_image('1234567/ff123f70e0e0cf70079a')

        # recheck to see the difference
        quota_after = await dp.get_images_quota()
    except Exception:
        logging.exception('Oops!')
    else:
        print(quota_before)
        print('Success?', success)
        print(quota_after)
        print('Freed up', quota_after.available - quota_before.available, 'bytes')

        ''' Output:
        Quota(total=104857600, used=10423667, available=94433933)
        Success? True
        Quota(total=104857600, used=10383100, available=94474500)
        Freed up 40567 bytes
        '''

    # You have to close session manually
    # if you called any request outside web app
    # Session close is added to on_shutdown list
    # in webhhok.configure_app
    await dp.close()


loop = asyncio.get_event_loop()
tasks = [
    loop.create_task(check_quota_status_and_delete_image()),
]
wait_tasks = asyncio.wait(tasks)
loop.run_until_complete(wait_tasks)
loop.close()
