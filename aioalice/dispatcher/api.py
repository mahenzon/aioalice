import aiohttp
import logging
from http import HTTPStatus

from ..utils import json, exceptions
from ..utils.helper import Helper, HelperMode, Item

BASE_URL = 'https://dialogs.yandex.net/api/v1/'
API_URL = BASE_URL + 'skills/{skill_id}/{method}/'

log = logging.getLogger(__name__)


async def _check_result(response):
    body = await response.text()
    if response.content_type != 'application/json':
        log.error('Invalid response with content type %r: %r',
                  response.content_type, body)
        exceptions.DialogsAPIError.detect(body)

    try:
        result_json = await response.json(loads=json.loads)
    except ValueError:
        result_json = {}

    log.debug('Request result is %r', result_json)

    if HTTPStatus.OK <= response.status <= HTTPStatus.IM_USED:
        return result_json
    if result_json and 'message' in result_json:
        description = result_json['message']
    else:
        description = body

    log.warning('Response status %r with description %r',
                response.status, description)
    exceptions.DialogsAPIError.detect(description)


async def request(session, oauth_token, skill_id=None, method=None, json=None,
                  file=None, request_method='POST', custom_url=None, **kwargs):
    """
    Make a request to API

    :param session: HTTP Client session
    :type session: :obj:`aiohttp.ClientSession`
    :param oauth_token: oauth_token
    :type oauth_token: :obj:`str`
    :param skill_id: skill_id. Optional. Not used if custom_url is provided
    :type skill_id: :obj:`str`
    :param method: API method. Optional. Not used if custom_url is provided
    :type method: :obj:`str`
    :param json: request payload
    :type json: :obj: `dict`
    :param file: file
    :type file: :obj: `io.BytesIO`
    :param request_method: API request method
    :type request_method: :obj:`str`
    :param custom_url: Yandex has very developer UNfriendly API, so some endpoints cannot be achieved by standatd template.
    :type custom_url: :obj:`str`
    :return: result
    :rtype: ::obj:`dict`
    """
    log.debug("Making a `%s` request to %r with json `%r` or file `%r`",
              request_method, method, json, file)
    if custom_url is None:
        url = Methods.api_url(skill_id, method)
    else:
        url = custom_url
    headers = {'Authorization': oauth_token}
    data = None
    if file:
        data = aiohttp.FormData()
        data.add_field('file', file)
    try:
        async with session.request(request_method, url, json=json, data=data, headers=headers, **kwargs) as response:
            return await _check_result(response)
    except aiohttp.ClientError as e:
        raise exceptions.NetworkError(f"aiohttp client throws an error: {e.__class__.__name__}: {e}")


class Methods(Helper):

    mode = HelperMode.lowerCamelCase

    IMAGES = Item()  # images
    STATUS = Item()  # status

    @staticmethod
    def api_url(skill_id, method):
        """
        Generate API URL with skill_id and method

        :param skill_id:
        :param method:
        :return:
        """
        return API_URL.format(skill_id=skill_id, method=method)
