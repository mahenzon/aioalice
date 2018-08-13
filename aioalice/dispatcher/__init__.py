import aiohttp
import asyncio
# import logging

from . import api
from .handler import Handler, SkipHandler
from .storage import DisabledStorage, MemoryStorage, DEFAULT_STATE
from .filters import generate_default_filters, ExceptionsFilter
from ..utils import json, exceptions

from ..types import UploadedImage, Quota
# log = logging.getLogger(__name__)


class Dispatcher:

    def __init__(self, loop=None, storage=None, *, skill_id=None, oauth_token=None):
        # TODO: inculde default handler for 'test' commands
        # TODO: create default handler for exceptions handler
        self.loop = loop or asyncio.get_event_loop()
        self.storage = storage or DisabledStorage()
        self.requests_handlers = Handler()
        self.errors_handlers = Handler()

        self.skill_id = skill_id
        self.oauth_token = oauth_token

        self.__session = None  # Lazy initialize session

    @property
    def session(self):
        if self.__session is None:
            self.__session = aiohttp.ClientSession(
                loop=self.loop, json_serialize=json.dumps
            )
        return self.__session

    async def close(self):
        """
        Close all client sessions

        If doing any requests outside of web app don't forget
        to close session manually by calling `await dp.close`
        """
        if self.__session and not self.__session.closed:
            await self.__session.close()

    async def shutdown(self, webapp):
        await self.close()

    async def process_request(self, request):
        try:
            return await self.requests_handlers.notify(request)
        except Exception as e:
            result = await self.errors_handlers.notify(request, e)
            if result:
                return result
            raise

    def register_request_handler(self, callback, *, commands=None, contains=None, starts_with=None, request_type=None,
                                 func=None, state=DEFAULT_STATE, regexp=None, custom_filters=None, **kwargs):
        """
        Register handler for AliceRequest

        .. code-block:: python3
            dp = Dispatcher()

            async def handle_all_requests(alice_request):
                return alice_request.response('Hello world!')

            dp.register_request_handler(handle_all_requests)


        :param callback: function to process request
        :param commands: list of commands
        :param contains: list of lines to search in commands `any([line in command for line in contains])`
        :param starts_with: list of lines to check if command starts with any of them
        :param request_type: Type of the request can be 'SimpleUtterance' or 'ButtonPressed'
        :param func: any callable object (for custom checks)
        :param state: For FSM
        :param regexp: REGEXP
        :param custom_filters: list of custom filters
        :param kwargs:
        """
        if custom_filters is None:
            custom_filters = []

        prepared_filers = generate_default_filters(
            self, *custom_filters, commands=commands, contains=contains,
            starts_with=starts_with, request_type=request_type,
            func=func, state=state, regexp=regexp, **kwargs
        )
        self.requests_handlers.register(callback, prepared_filers)

    def request_handler(self, *custom_filters, commands=None, contains=None, starts_with=None,
                        request_type=None, func=None, state=DEFAULT_STATE, regexp=None, **kwargs):
        """
        Decorator AliceRequest handler

        .. code-block:: python3
            dp = Dispatcher()

            @dp.request_handler()
            async def handle_all_requests(alice_request):
                return alice_request.response('Hello world!')


        :param callback: function to process request
        :param commands: list of commands
        :param contains: list of lines to search in commands `any([line in command for line in contains])`
        :param starts_with: list of lines to check if command starts with any of them
        :param request_type: Type of the request can be 'SimpleUtterance' or 'ButtonPressed'
        :param func: any callable object (for custom checks)
        :param state: For FSM
        :param regexp: REGEXP
        :param custom_filters: list of custom filters
        :param kwargs:
        :return: decorated function
        """
        def decorator(callback):
            self.register_request_handler(
                callback, commands=commands, contains=contains, starts_with=starts_with, request_type=request_type,
                func=func, state=state, regexp=regexp, custom_filters=custom_filters, **kwargs
            )
            return callback

        return decorator

    def register_errors_handler(self, callback, *, exception=None, func=None):
        """
        Register handler for errors

        :param callback:
        :param exception: you can make handler for specific errors type
        :param func: any callable object (for custom checks)
        """
        filters_list = []
        if func is not None:
            filters_list.append(func)
        if exception is not None:
            filters_list.append(ExceptionsFilter(exception))
        self.errors_handlers.register(callback, filters_list)

    def errors_handler(self, exception=None, func=None):
        """
        Decorator for errors handler

        :param func:
        :param exception: you can make handler for specific errors type
        :param run_task: run callback in task (no wait results)
        :return: decorated function
        """

        def decorator(callback):
            self.register_errors_handler(callback, exception=exception, func=func)
            return callback

        return decorator

    def _check_auth(self, skill_id, oauth_token):
        skill_id = skill_id or self.skill_id
        oauth_token = oauth_token or self.oauth_token
        if not (skill_id and oauth_token):
            raise exceptions.AuthRequired('Please provide both skill_id and oauth_token')
        return skill_id, oauth_token

    async def get_images(self, skill_id=None, oauth_token=None):
        '''
        Get uploaded images

        :param skill_id: Provide if was not set at the Dispatcher init
        :type skill_id: :obj:`str`
        :param oauth_token: Provide if was not set at the Dispatcher init
        :type oauth_token: :obj:`str`

        :return: list of UploadedImage instances
        '''
        skill_id, oauth_token = self._check_auth(skill_id, oauth_token)
        result = await api.request(
            self.session, oauth_token, skill_id,
            api.Methods.IMAGES, request_method='GET'
        )
        if 'images' not in result:
            raise exceptions.ApiChanged(f'Expected "images" in result, got {result}')
        return [UploadedImage(**dct) for dct in result['images']]

    async def upload_image(self, image_url_or_bytes, skill_id=None, oauth_token=None):
        '''
        Upload image by either url or bytes

        :param image_url_or_bytes: Image URL or bytes
        :type image_url_or_bytes: :obj:`str` or `io.BytesIO`
        :param skill_id: Provide if was not set at the Dispatcher init
        :type skill_id: :obj:`str`
        :param oauth_token: Provide if was not set at the Dispatcher init
        :type oauth_token: :obj:`str`

        :return: UploadedImage
        '''
        skill_id, oauth_token = self._check_auth(skill_id, oauth_token)
        json = None
        file = None
        if isinstance(image_url_or_bytes, str):
            json = {'url': image_url_or_bytes}
        else:
            file = image_url_or_bytes
        result = await api.request(
            self.session, oauth_token, skill_id,
            api.Methods.IMAGES, json, file
        )
        if 'image' not in result:
            raise exceptions.ApiChanged(f'Expected "image" in result, got {result}')
        return UploadedImage(**result['image'])

    async def get_images_quota(self, oauth_token=None):
        '''
        Get images storage quota

        :param oauth_token: Provide if was not set at the Dispatcher init
        :type oauth_token: :obj:`str`

        :return: Quota
        '''
        oauth_token = oauth_token or self.oauth_token
        if oauth_token is None:
            raise exceptions.AuthRequired('Please provide oauth_token')

        result = await api.request(
            self.session, oauth_token, request_method='GET',
            custom_url=api.BASE_URL + api.Methods.STATUS
        )
        if 'images' not in result or 'quota' not in result['images']:
            raise exceptions.ApiChanged(f'Expected "images" "quota" in result, got {result}')
        return Quota(**result['images']['quota'])

    async def delete_image(self, image_id, skill_id=None, oauth_token=None):
        '''
        Delete image by id

        :param image_id: Image id to be deleted
        :type image_id: :obj:`str`
        :param skill_id: Provide if was not set at the Dispatcher init
        :type skill_id: :obj:`str`
        :param oauth_token: Provide if was not set at the Dispatcher init
        :type oauth_token: :obj:`str`

        :return: True if result is ok
        '''
        skill_id, oauth_token = self._check_auth(skill_id, oauth_token)
        url = api.Methods.api_url(skill_id, api.Methods.IMAGES) + image_id
        result = await api.request(
            self.session, oauth_token,
            request_method='DELETE', custom_url=url
        )
        return result['result'] == 'ok' if 'result' in result else False
