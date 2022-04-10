from aiohttp.web import Request as WebRequest
from attr import attrs, attrib

from aioalice.types import (
    AliceObject,
    Meta,
    Session,
    Card,
    Request,
    Response,
    AliceResponse,
)
from aioalice.utils import ensure_cls, safe_kwargs


@safe_kwargs
@attrs
class AliceRequest(AliceObject):
    """AliceRequest is a request from Alice API"""
    original_request = attrib(type=WebRequest)
    meta = attrib(converter=ensure_cls(Meta))
    request = attrib(converter=ensure_cls(Request))
    session = attrib(converter=ensure_cls(Session))
    version = attrib(type=str)

    def _response(self, response, session_state=None, user_state_update=None, application_state=None):
        return AliceResponse(
            response=response,
            session=self.session.base,
            session_state=session_state or {},
            user_state_update=user_state_update or {},
            application_state=application_state or {},
            version=self.version,
        )

    def response(self, response_or_text, session_state=None, user_state_update=None, application_state=None, **kwargs):
        """
        Generate response

        :param response_or_text: Response or Response's text:
            if response_or_text is not an instance of Response,
            it is passed to the Response initialisator with kwargs.
            Otherwise it is used as a Response

        :param kwargs: tts, card, buttons, end_session for Response
            NOTE: if you want to pass card, consider using one of
              these methods: response_big_image, response_items_list

        :param session_state: Session's state
        :param user_state_update: User's state
        :param application_state: Application's state
            Allows to store data on Yandex's side
            Read more: https://yandex.ru/dev/dialogs/alice/doc/session-persistence.html

        :return: AliceResponse
        """
        if not isinstance(response_or_text, Response):
            response_or_text = Response(response_or_text, **kwargs)
        return self._response(response_or_text, session_state, user_state_update, application_state)

    def response_big_image(self, text, image_id, title, description, button=None,
                           session_state=None, user_state_update=None, application_state=None, **kwargs):
        """
        Generate response with Big Image card

        :param text: Response's text
        :param image_id: Image's id for BigImage Card
        :param title: Image's title for BigImage Card
        :param description: Image's description for BigImage Card
        :param button: Image's button for BigImage Card
        :param session_state: Session's state
        :param user_state_update: User's state
        :param application_state: Application's state
            Allows to store data on Yandex's side
            Read more: https://yandex.ru/dev/dialogs/alice/doc/session-persistence.html
        :param kwargs: tts, buttons, end_session for Response
        :return: AliceResponse
        """
        return self._response(
            Response(
                text,
                card=Card.big_image(image_id, title, description, button),
                **kwargs,
            ),
            session_state, user_state_update, application_state
        )

    def response_items_list(self, text, header, items, footer=None,
                            session_state=None, user_state_update=None, application_state=None, **kwargs):
        """
        Generate response with Items List card

        :param text: Response's text
        :param header: Card's header
        :param items: Card's items - list of `Image` objects
        :param footer: Card's footer
        :param session_state: Session's state
        :param user_state_update: User's state
        :param application_state: Application's state
            Allows to store data on Yandex's side
            Read more: https://yandex.ru/dev/dialogs/alice/doc/session-persistence.html
        :param kwargs: tts, buttons, end_session for Response
        :return: AliceResponse
        """
        return self._response(
            Response(
                text,
                card=Card.items_list(header, items, footer),
                **kwargs,
            ),
            session_state, user_state_update, application_state
        )
