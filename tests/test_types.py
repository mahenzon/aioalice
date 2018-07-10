import unittest

from aioalice import types


class TestAliceTypes(unittest.TestCase):

    def _test_meta(self, meta, dct):
        self.assertEqual(meta.locale, dct['locale'])
        self.assertEqual(meta.timezone, dct['timezone'])
        self.assertEqual(meta.client_id, dct['client_id'])

    def test_meta(self):
        meta_json = {
            "locale": "ru-RU",
            "timezone": "Europe/Moscow",
            "client_id": "ru.yandex.searchplugin/5.80 (Samsung Galaxy; Android 4.4)"
        }
        meta = types.Meta(**meta_json)
        self._test_meta(meta, meta_json)

    def _test_markup(self, markup, dct):
        self.assertEqual(markup.dangerous_context, dct['dangerous_context'])

    def test_markup(self):
        markup_json = {
            "dangerous_context": True
        }
        markup = types.Markup(**markup_json)
        self._test_markup(markup, markup_json)

    def _test_request(self, req, dct):
        self.assertEqual(req.command, dct['command'])
        self.assertEqual(req.original_utterance, dct['original_utterance'])
        self.assertEqual(req.type, dct['type'])
        self._test_markup(req.markup, dct['markup'])
        self.assertEqual(req.payload, dct['payload'])

    def test_request(self):
        request_json = {
            "command": "где поесть",
            "original_utterance": "Алиса где поесть",
            "type": "SimpleUtterance",
            "markup": {
                "dangerous_context": True
            },
            "payload": {}
        }
        request = types.Request(**request_json)
        self._test_request(request, request_json)

    def _test_base_session(self, bs, dct):
        self.assertEqual(bs.user_id, dct['user_id'])
        self.assertEqual(bs.message_id, dct['message_id'])
        self.assertEqual(bs.session_id, dct['session_id'])

    def test_base_session(self):
        base_session_json = {
            "message_id": 4,
            "session_id": "2eac4854-fce721f3-b845abba-20d60",
            "user_id": "AC9WC3DF6FCE052E45A4566A48E6B7193774B84814CE49A922E163B8B29881DC"
        }
        base_session = types.BaseSession(**base_session_json)
        self._test_base_session(base_session, base_session_json)

    def _test_session(self, sess, dct):
        self.assertEqual(sess.new, dct['new'])
        self.assertEqual(sess.skill_id, dct['skill_id'])
        self._test_base_session(sess, dct)

    def test_session(self):
        session_json = {
            "new": True,
            "message_id": 4,
            "session_id": "2eac4854-fce721f3-b845abba-20d60",
            "skill_id": "3ad36498-f5rd-4079-a14b-788652932056",
            "user_id": "AC9WC3DF6FCE052E45A4566A48E6B7193774B84814CE49A922E163B8B29881DC"
        }
        session = types.Session(**session_json)
        self._test_session(session, session_json)

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

    def test_response(self):
        response_json = {
            "text": "Здравствуйте! Это мы, хороводоведы.",
            "tts": "Здравствуйте! Это мы, хоров+одо в+еды.",
            "buttons": [
                {
                    "title": "Надпись на кнопке",
                    "payload": {},
                    "url": "https://responseexample.com/",
                    "hide": True
                }
            ],
            "end_session": False
        }
        response = types.Response(**response_json)
        self._test_response(response, response_json)

    def _test_alice_request(self, arq, dct):
        self.assertEqual(arq.version, dct['version'])
        self._test_session(arq.session, dct['session'])
        self._test_request(arq.request, dct['request'])
        self._test_meta(arq.meta, dct['meta'])

    def test_alice_request(self):
        alice_request_json = {
            "meta": {
                "locale": "ru-RU",
                "timezone": "Europe/Moscow",
                "client_id": "ru.yandex.searchplugin/5.80 (Samsung Galaxy; Android 4.4)"
            },
            "request": {
                "command": "где ближайшее отделение",
                "original_utterance": "Алиса спроси у Сбербанка где ближайшее отделение",
                "type": "SimpleUtterance",
                "markup": {
                    "dangerous_context": True
                },
                "payload": {}
            },
            "session": {
                "new": True,
                "message_id": 4,
                "session_id": "2eac4854-fce721f3-b845abba-20d60",
                "skill_id": "3ad36498-f5rd-4079-a14b-788652932056",
                "user_id": "AC9WC3DF6FCE052E45A4566A48E6B7193774B84814CE49A922E163B8B29881DC"
            },
            "version": "1.0"
        }
        alice_request = types.AliceRequest(**alice_request_json)
        self.assertEqual(alice_request.to_json(), alice_request_json)
        self._test_alice_request(alice_request, alice_request_json)

    def _test_alice_response(self, arp, dct):
        self.assertEqual(arp.version, dct['version'])

    def test_alice_response(self):
        alice_response_json = {
            "response": {
                "text": "Здравствуйте! Это мы, хороводоведы.",
                "tts": "Здравствуйте! Это мы, хоров+одо в+еды.",
                "end_session": False
            },
            "session": {
                "session_id": "2eac4854-fce721f3-b845abba-20d60",
                "message_id": 4,
                "user_id": "AC9WC3DF6FCE052E45A4566A48E6B7193774B84814CE49A922E163B8B29881DC"
            },
            "version": "1.0"
        }
        alice_response = types.AliceResponse(**alice_response_json)
        self._test_alice_response(alice_response, alice_response_json)
        alice_response_json["response"]["buttons"] = [
            {
                "title": "Надпись на кнопке",
                "payload": {},
                "url": "https://example.com/",
                "hide": True
            },
            {
                "title": "Надпись на кнопке1",
                "payload": {'key': 'value'},
                "url": "https://ya.com/",
                "hide": False
            },
        ]
        alice_response = types.AliceResponse(**alice_response_json)
        self.assertEqual(alice_response.to_json(), alice_response_json)
        self._test_alice_response(alice_response, alice_response_json)

    def test_response_from_request(self):
        alice_request_json = {
            "meta": {
                "locale": "ru-RU",
                "timezone": "Europe/Moscow",
                "client_id": "ru.yandex.searchplugin/5.80 (Samsung Galaxy; Android 4.4)"
            },
            "request": {
                "command": "где ближайшее отделение",
                "original_utterance": "Алиса спроси у Сбербанка где ближайшее отделение",
                "type": "SimpleUtterance",
                "markup": {
                    "dangerous_context": True
                },
                "payload": None
            },
            "session": {
                "new": True,
                "message_id": 4,
                "session_id": "2eac4854-fce721f3-b845abba-20d60",
                "skill_id": "3ad36498-f5rd-4079-a14b-788652932056",
                "user_id": "AC9WC3DF6FCE052E45A4566A48E6B7193774B84814CE49A922E163B8B29881DC"
            },
            "version": "1.0"
        }
        alice_request = types.AliceRequest(**alice_request_json)

        resp_text = 'Здравствуйте! Это мы, хороводоведы.'
        alice_response = alice_request.response(resp_text)
        expected_response = {
            "response": {
                "text": resp_text,
                'tts': None,
                'buttons': None,
                "end_session": False
            },
            "session": {
                "session_id": "2eac4854-fce721f3-b845abba-20d60",
                "message_id": 4,
                "user_id": "AC9WC3DF6FCE052E45A4566A48E6B7193774B84814CE49A922E163B8B29881DC"
            },
            "version": "1.0"
        }
        self.assertEqual(alice_response.to_json(), expected_response)
        new_tts = "Здравствуйте! Это мы, хоров+одо в+еды."
        btn_title = "Надпись на кнопке"
        btn_url = "https://example.com/"
        new_btn = types.Button(btn_title, url=btn_url)
        expected_response["response"].update({
            "tts": new_tts,
            "buttons": [
                {
                    "title": btn_title,
                    "payload": None,
                    "url": btn_url,
                    "hide": True
                }
            ],
        })
        alice_response.response.tts = new_tts
        alice_response.response.buttons = [new_btn]
        self.assertEqual(alice_response.to_json(), expected_response)

        alice_response = alice_request.response(resp_text, tts=new_tts, buttons=[new_btn])
        self.assertEqual(alice_response.to_json(), expected_response)


if __name__ == '__main__':
    unittest.main()
