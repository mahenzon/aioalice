from attr import attrs, attrib
from aioalice.utils import ensure_cls
from . import AliceObject, Meta, Session, \
    Card, Request, Response, AliceResponse


@attrs
class AliceRequest(AliceObject):
    """AliceRequest is a request from Alice API"""

    meta = attrib(convert=ensure_cls(Meta))
    request = attrib(convert=ensure_cls(Request))
    session = attrib(convert=ensure_cls(Session))
    version = attrib(type=str)

    def _response(self, response):
        return AliceResponse(
            response=response,
            session=self.session.base,
            version=self.version
        )

    def response(self, responose_or_text, **kwargs):
        """
        Generate response

        :param responose_or_text: Response or Response's text:
            if responose_or_text is not an instance of Response,
            it is passed to the Response initialisator with kwargs.
            Otherwise it is used as a Response

        :param kwargs: tts, card, buttons, end_session for Response
            NOTE: if you want to pass card, concider using one of
              these methods: response_big_image, response_items_list
        :return: AliceResponse
        """
        if not isinstance(responose_or_text, Response):
            responose_or_text = Response(responose_or_text, **kwargs)
        return self._response(responose_or_text)

    def response_big_image(self, text, image_id, title, description, button=None, **kwargs):
        """
        Generate response with Big Image card

        :param text: Response's text
        :param image_id: Image's id for BigImage Card
        :param title: Image's title for BigImage Card
        :param description: Image's description for BigImage Card
        :param button: Image's button for BigImage Card
        :param kwargs: tts, buttons, end_session for Response
        :return: AliceResponse
        """
        return self._response(
            Response(
                text, **kwargs,
                card=Card.big_image(image_id, title, description, button),
            )
        )

    def response_items_list(self, text, header, items, footer=None, **kwargs):
        """
        Generate response with Items List card

        :param text: Response's text
        :param header: Card's header
        :param items: Card's items - list of `Image` objects
        :param footer: Card's footer
        :param kwargs: tts, buttons, end_session for Response
        :return: AliceResponse
        """
        return self._response(
            Response(
                text, **kwargs,
                card=Card.items_list(header, items, footer)
            )
        )
