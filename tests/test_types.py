import unittest

from aioalice import types
from aioalice.utils import generate_json_payload

from _dataset import META, MARKUP, SESSION, \
    REQUEST, REQUEST_DANGEROUS, BASE_SESSION, \
    RESPONSE, RESPONSE2, ALICE_REQUEST, \
    ALICE_RESPONSE, ALICE_RESPONSE_WITH_BUTTONS, \
    EXPECTED_RESPONSE, TTS, BUTTON_TEXT, URL, \
    EXPECTED_RESPONSE_WITH_BUTTONS, UPLOADED_IMAGE, \
    MEDIA_BUTTON, IMAGE, FOOTER, IMAGE_ID, \
    CARD_TITLE, CARD_DESCR, MB_PAYLOAD, FOOTER_TEXT, \
    EXPECTED_CARD_BIG_IMAGE_JSON, CARD_HEADER_TEXT, \
    EXPECTED_CARD_ITEMS_LIST_JSON, RESPONSE_TEXT, \
    RESPONSE_BUTTON, \
    EXPECTED_ALICE_RESPONSE_BIG_IMAGE_WITH_BUTTON, \
    EXPECTED_ALICE_RESPONSE_ITEMS_LIST_WITH_BUTTON


class TestAliceTypes(unittest.TestCase):

    def _assert_payload(self, alice_obj, expected_json):
        json_payload = generate_json_payload(**alice_obj.to_json())
        self.assertEqual(json_payload, expected_json)

    def _test_meta(self, meta, dct):
        self.assertEqual(meta.locale, dct['locale'])
        self.assertEqual(meta.timezone, dct['timezone'])
        self.assertEqual(meta.client_id, dct['client_id'])

    def test_meta(self):
        meta = types.Meta(**META)
        self._test_meta(meta, META)

    def _test_markup(self, markup, dct):
        self.assertEqual(markup.dangerous_context, dct['dangerous_context'])

    def test_markup(self):
        markup = types.Markup(**MARKUP)
        self._test_markup(markup, MARKUP)

    def _test_request(self, req, dct):
        self.assertEqual(req.command, dct['command'])
        self.assertEqual(req.original_utterance, dct['original_utterance'])
        self.assertEqual(req.type, dct['type'])
        self.assertEqual(req.payload, dct['payload'])
        if 'markup' in dct:
            self._test_markup(req.markup, dct['markup'])

    def test_request(self):
        request = types.Request(**REQUEST)
        self._test_request(request, REQUEST)
        request_dang = types.Request(**REQUEST_DANGEROUS)
        self._test_request(request_dang, REQUEST_DANGEROUS)

    def _test_base_session(self, bs, dct):
        self.assertEqual(bs.user_id, dct['user_id'])
        self.assertEqual(bs.message_id, dct['message_id'])
        self.assertEqual(bs.session_id, dct['session_id'])

    def test_base_session(self):
        base_session = types.BaseSession(**BASE_SESSION)
        self._test_base_session(base_session, BASE_SESSION)

    def _test_session(self, sess, dct):
        self.assertEqual(sess.new, dct['new'])
        self.assertEqual(sess.skill_id, dct['skill_id'])
        self._test_base_session(sess, dct)

    def test_session(self):
        session = types.Session(**SESSION)
        self._test_session(session, SESSION)

    def _test_button(self, btn, title, url=None, payload=None, hide=True):
        self.assertEqual(btn.title, title)
        self.assertEqual(btn.url, url)
        self.assertEqual(btn.payload, payload)
        self.assertEqual(btn.hide, hide)

    def _tst_buttons(self, btn, dct):
        self._test_button(
            btn,
            dct.get('title'),
            dct.get('url'),
            dct.get('payload'),
            dct.get('hide')
        )

    def test_buttons(self):
        title = 'Title'

        btn1 = types.Button(title)
        self._test_button(btn1, title)
        btn2 = types.Button(title, url='yandex.ru')
        self._test_button(btn2, title, 'yandex.ru')
        btn3 = types.Button(title, payload={'key': 'value'})
        self._test_button(btn3, title, payload={'key': 'value'})
        btn4 = types.Button(title, payload={'json': {'key': 'value'}}, hide=False)
        self._test_button(btn4, title, payload={'json': {'key': 'value'}}, hide=False)
        btn5 = types.Button(title, url='github.com', payload={'json': {'key': 'value'}}, hide=False)
        self._test_button(btn5, title, url='github.com', payload={'json': {'key': 'value'}}, hide=False)

    def _test_response(self, resp, dct):
        self.assertEqual(resp.text, dct['text'])
        self.assertEqual(resp.tts, dct['tts'])
        self.assertEqual(resp.end_session, dct['end_session'])
        if resp.buttons is not None:
            for btn, btn_dct in zip(resp.buttons, dct['buttons']):
                self._tst_buttons(btn, btn_dct)

    def test_response1(self):
        response = types.Response(**RESPONSE)
        self._test_response(response, RESPONSE)

    def test_response2(self):
        response = types.Response(RESPONSE2['text'], buttons=['Hi!'])
        self._assert_payload(response, RESPONSE2)

    def _test_alice_request(self, arq, dct):
        self.assertEqual(arq.version, dct['version'])
        self._test_session(arq.session, dct['session'])
        self._test_request(arq.request, dct['request'])
        self._test_meta(arq.meta, dct['meta'])

    def test_alice_request(self):
        alice_request = types.AliceRequest(**ALICE_REQUEST)
        self.assertEqual(alice_request.to_json(), ALICE_REQUEST)
        self._test_alice_request(alice_request, ALICE_REQUEST)

    def _test_alice_response(self, arp, dct):
        self.assertEqual(arp.version, dct['version'])

    def test_alice_response(self):
        alice_response = types.AliceResponse(**ALICE_RESPONSE)
        self._test_alice_response(alice_response, ALICE_RESPONSE)
        alice_response = types.AliceResponse(**ALICE_RESPONSE_WITH_BUTTONS)
        self._assert_payload(alice_response, ALICE_RESPONSE_WITH_BUTTONS)
        self._test_alice_response(alice_response, ALICE_RESPONSE_WITH_BUTTONS)

    def test_response_from_request(self):
        alice_request = types.AliceRequest(**ALICE_REQUEST)

        alice_response = alice_request.response(
            EXPECTED_RESPONSE['response']['text']
        )
        self._assert_payload(alice_response, EXPECTED_RESPONSE)

    def test_response_from_request2(self):
        alice_request = types.AliceRequest(**ALICE_REQUEST)
        alice_response = alice_request.response(
            RESPONSE_TEXT, tts=TTS,
            buttons=[types.Button(BUTTON_TEXT, url=URL)]
        )
        self._assert_payload(alice_response, EXPECTED_RESPONSE_WITH_BUTTONS)

    def test_response_big_image_from_request(self):
        alice_request = types.AliceRequest(**ALICE_REQUEST)
        alice_response = alice_request.response_big_image(
            RESPONSE_TEXT, IMAGE_ID, CARD_TITLE, CARD_DESCR,
            types.MediaButton(BUTTON_TEXT, URL, MB_PAYLOAD),
            types.CardFooter(FOOTER_TEXT, MEDIA_BUTTON),
            buttons=[RESPONSE_BUTTON]
        )
        self._assert_payload(alice_response, EXPECTED_ALICE_RESPONSE_BIG_IMAGE_WITH_BUTTON)

    def test_response_items_list_from_request(self):
        alice_request = types.AliceRequest(**ALICE_REQUEST)
        alice_response = alice_request.response_items_list(
            RESPONSE_TEXT, CARD_HEADER_TEXT,
            [types.Image(**IMAGE)],
            types.CardFooter(**FOOTER),
            buttons=[RESPONSE_BUTTON]
        )
        self._assert_payload(alice_response, EXPECTED_ALICE_RESPONSE_ITEMS_LIST_WITH_BUTTON)

    def _test_uploaded_image(self, uimg, dct):
        self.assertEqual(uimg.id, dct['id'])
        self.assertEqual(uimg.origUrl, dct['origUrl'])
        self.assertEqual(uimg.orig_url, dct['origUrl'])

    def test_uploaded_image(self):
        uimg = types.UploadedImage(**UPLOADED_IMAGE)
        self._test_uploaded_image(uimg, UPLOADED_IMAGE)

    def _test_media_button(self, mb, mb_dct):
        self.assertEqual(mb.text, mb_dct['text'])
        self.assertEqual(mb.url, mb_dct['url'])
        self.assertEqual(mb.payload, mb_dct['payload'])

    def test_media_button(self):
        mb = types.MediaButton(**MEDIA_BUTTON)
        self._test_media_button(mb, MEDIA_BUTTON)

    def _test_image_with_button(self, img, dct):
        self.assertEqual(img.image_id, dct['image_id'])
        self.assertEqual(img.title, dct['title'])
        self.assertEqual(img.description, dct['description'])
        self._test_media_button(img.button, dct['button'])

    def test_image_with_button(self):
        img = types.Image(**IMAGE)
        self._test_image_with_button(img, IMAGE)

    def _test_card_header(self, cheader, dct):
        self.assertEqual(cheader.text, dct['text'])

    def test_card_header(self):
        header = types.CardHeader(CARD_HEADER_TEXT)
        self._test_card_header(header, {'text': CARD_HEADER_TEXT})

    def _test_card_footer(self, cfooter, dct):
        self.assertEqual(cfooter.text, dct['text'])
        self._test_media_button(cfooter.button, dct['button'])
        self.assertEqual(cfooter.to_json(), dct)

    def test_card_footer(self):
        card_footer = types.CardFooter(FOOTER_TEXT, FOOTER['button'])
        self._test_card_footer(card_footer, FOOTER)

    def test_card_big_image(self):
        card_big_image = types.Card(
            types.CardType.BIG_IMAGE,
            image_id=IMAGE_ID,
            title=CARD_TITLE,
            description=CARD_DESCR,
            button=types.MediaButton(BUTTON_TEXT, URL, MB_PAYLOAD),
            footer=types.CardFooter(FOOTER_TEXT, MEDIA_BUTTON)
        )
        self._assert_payload(card_big_image, EXPECTED_CARD_BIG_IMAGE_JSON)

    def test_card_big_image_card_method(self):
        card_big_image = types.Card.big_image(
            IMAGE_ID, CARD_TITLE, CARD_DESCR,
            types.MediaButton(BUTTON_TEXT, URL, MB_PAYLOAD),
            types.CardFooter(FOOTER_TEXT, MEDIA_BUTTON)
        )
        self._assert_payload(card_big_image, EXPECTED_CARD_BIG_IMAGE_JSON)

    def test_card_items_list(self):
        card_items_list = types.Card(
            types.CardType.ITEMS_LIST,
            header=CARD_HEADER_TEXT,
            items=[types.Image(**IMAGE)],
            footer=dict(text=FOOTER_TEXT, button=MEDIA_BUTTON)
        )
        self._assert_payload(card_items_list, EXPECTED_CARD_ITEMS_LIST_JSON)

    def test_card_items_list_card_method(self):
        card_items_list = types.Card.items_list(
            CARD_HEADER_TEXT,
            [types.Image(**IMAGE)],
            dict(text=FOOTER_TEXT, button=MEDIA_BUTTON)
        )
        self._assert_payload(card_items_list, EXPECTED_CARD_ITEMS_LIST_JSON)


if __name__ == '__main__':
    unittest.main()
