from copy import deepcopy


META = {
    "locale": "ru-RU",
    "timezone": "Europe/Moscow",
    "client_id": "ru.yandex.searchplugin/5.80 (Samsung Galaxy; Android 4.4)"
}

MARKUP = {
    "dangerous_context": True
}

REQUEST = {
    "command": "где поесть",
    "original_utterance": "Алиса где поесть",
    "type": "SimpleUtterance",
    "payload": {}
}

REQUEST_DANGEROUS = deepcopy(REQUEST)
REQUEST_DANGEROUS["markup"] = {
    "dangerous_context": True
}

BASE_SESSION = {
    "message_id": 4,
    "session_id": "2eac4854-fce721f3-b845abba-20d60",
    "user_id": "AC9WC3DF6FCE052E45A4566A48E6B7193774B84814CE49A922E163B8B29881DC"
}

SESSION = deepcopy(BASE_SESSION)
SESSION.update({
    "new": True,
    "skill_id": "3ad36498-f5rd-4079-a14b-788652932056",
})

TTS = "Здравствуйте! Это мы, хоров+одо в+еды."

RESPONSE_BUTTON = {
    "title": "Надпись на кнопке",
    "payload": {},
    "url": "https://responseexample.com/",
    "hide": True
}

RESPONSE = {
    "text": "Здравствуйте! Это мы, хороводоведы.",
    "tts": TTS,
    "buttons": [RESPONSE_BUTTON],
    "end_session": False
}

RESPONSE2 = {
    'text': 'Response Text',
    'buttons': [
        {
            'title': 'Hi!',
            'hide': True
        }
    ],
    'end_session': False
}

ALICE_REQUEST = {
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
    "session": SESSION,
    "version": "1.0"
}

ALICE_RESPONSE = {
    "response": {
        "text": "Здравствуйте! Это мы, хороводоведы.",
        "tts": TTS,
        "end_session": False
    },
    "session": BASE_SESSION,
    "version": "1.0"
}

ALICE_RESPONSE_WITH_BUTTONS = deepcopy(ALICE_RESPONSE)
ALICE_RESPONSE_WITH_BUTTONS["response"]["buttons"] = [
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

RESPONSE_TEXT = 'Здравствуйте! Это мы, хороводоведы.'
EXPECTED_RESPONSE = {
    "response": {
        "text": RESPONSE_TEXT,
        "end_session": False
    },
    "session": BASE_SESSION,
    "version": "1.0"
}

BUTTON_TEXT = "Надпись на кнопке 3"
URL = 'https://example.com/'
EXPECTED_RESPONSE_WITH_BUTTONS = deepcopy(EXPECTED_RESPONSE)
EXPECTED_RESPONSE_WITH_BUTTONS['response'].update({
    'tts': TTS,
    'buttons': [
        {
            'title': BUTTON_TEXT,
            'url': URL,
            'hide': True
        }
    ]
})

UPLOADED_IMAGE = {
    "id": '1234567890/qwerty',
    "origUrl": 'http://example.com'
}

MB_PAYLOAD = {'mediabutton': True, 'key': 'smth'}
MEDIA_BUTTON = {
    "text": BUTTON_TEXT,
    "url": URL,
    "payload": deepcopy(MB_PAYLOAD)
}

IMAGE_ID = '1027858/46r960da47f60207e924'

IMAGE = {
    "image_id": IMAGE_ID,
    "title": "Заголовок",
    "description": "Описание",
    "button": deepcopy(MEDIA_BUTTON)
}

CARD_HEADER_TEXT = 'Click here to see more'
FOOTER_TEXT = 'Click here to see more'
FOOTER = {
    'text': FOOTER_TEXT,
    'button': deepcopy(MEDIA_BUTTON)
}

CARD_TITLE = 'Заголовок'
CARD_DESCR = 'Описание'


EXPECTED_CARD_BIG_IMAGE_JSON = {
    "type": "BigImage",
    "image_id": IMAGE_ID,
    "title": CARD_TITLE,
    "description": CARD_DESCR,
    "button": deepcopy(MEDIA_BUTTON),
}


EXPECTED_CARD_ITEMS_LIST_JSON = {
    "type": "ItemsList",
    "header": {"text": CARD_HEADER_TEXT},
    "items": [deepcopy(IMAGE)],
    "footer": deepcopy(FOOTER),
}


EXPECTED_ALICE_RESPONSE_BIG_IMAGE_WITH_BUTTON = {
    "response": {
        "text": RESPONSE_TEXT,
        "card": deepcopy(EXPECTED_CARD_BIG_IMAGE_JSON),
        "buttons": [RESPONSE_BUTTON],
        "end_session": False
    },
    "session": BASE_SESSION,
    "version": "1.0"
}

EXPECTED_ALICE_RESPONSE_ITEMS_LIST_WITH_BUTTON = {
    "response": {
        "text": RESPONSE_TEXT,
        "card": deepcopy(EXPECTED_CARD_ITEMS_LIST_JSON),
        "buttons": [RESPONSE_BUTTON],
        "end_session": False
    },
    "session": BASE_SESSION,
    "version": "1.0"
}


DATA_FROM_STATION = {
    'meta': {
        'client_id': 'ru.yandex.quasar.services/1.0 (Yandex Station; android 6.0.1)',
        'flags': [
            'no_cards_support'
        ],
        'locale': 'ru-RU',
        'timezone': 'Europe/Moscow'
    },
    'request': {
        'command': '',
        'original_utterance': 'запусти навык qwerty',
        'type': 'SimpleUtterance'
    },
    'session': {
        'message_id': 0,
        'new': True,
        'session_id': '618709-bb99dd92-82c4f626-442a4',
        'skill_id': '94d16-a32f-4932-9f5e-354d31f71998',
        'user_id': 'CFC516B0EC123B86C78532BCEC1C33CBF05D54EF15C8001B52628EF49F580'
    },
    'version': '1.0'
}
