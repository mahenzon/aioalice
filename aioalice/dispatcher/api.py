import aiohttp
import logging
from http import HTTPStatus

from ..utils import json, exceptions
from ..utils.helper import Helper, HelperMode, Item

API_URL = 'https://dialogs.yandex.net/api/v1/skills/{skill_id}/{method}'


async def _check_result(response):
    body = await response.text()
    if response.content_type != 'application/json':
        logging.error(f'Invalid response with content type {response.content_type}: \"{body}\"')
        exceptions.DialogsAPIError.detect(body)

    try:
        result_json = await response.json(loads=json.loads)
    except ValueError:
        result_json = {}

    logging.debug(f'Request result is {result_json}')

    if HTTPStatus.OK <= response.status <= HTTPStatus.IM_USED:
        return result_json
    if result_json and 'message' in result_json:
        description = result_json['message']
    else:
        description = body

    logging.warning(f'Response status {response.status} with description {description}')
    exceptions.DialogsAPIError.detect(description)


async def request(session, skill_id, oauth_token, method, json=None, file=None, request_method='POST', **kwargs):
    """
    Make a request to API

    :param session: HTTP Client session
    :type session: :obj:`aiohttp.ClientSession`
    :param skill_id: skill_id
    :type skill_id: :obj:`str`
    :param oauth_token: oauth_token
    :type oauth_token: :obj:`str`
    :param method: API method
    :type method: :obj:`str`
    :param json: request payload
    :type json: :obj: `dict`
    :param file: file
    :type file: :obj: `io.BytesIO`
    :return: result
    :rtype: ::obj:`dict`
    """
    logging.debug(f"Making a `{request_method}` request to '{method}' with json `{json}` or file `{file}`")
    url = Methods.api_url(skill_id, method)
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

    @staticmethod
    def api_url(skill_id, method):
        """
        Generate API URL with skill_id and method

        :param skill_id:
        :param method:
        :return:
        """
        return API_URL.format(skill_id=skill_id, method=method)
