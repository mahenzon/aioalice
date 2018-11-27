<p align="center">
    Русский | <a href="README-en.md">English</a>
</p>

# Яндекс Алиса. Диалоги (навыки)


**aioAlice** это асинхронная библиотека для взаимодействия с Алисой


## Зачем?
- Работайте с привычными классами, а не зайнимайтесь парсингом JSON'а
- Автоматический ответ в вебхук, даже если вы не успели подготовить ответ вовремя - навык не вернет ошибку сервера, но запишет вам лог
> Автоматический ответ сработает только при использовании async IO. Если затянется обработка в каком-то цикле или др. синхронное вычисление, это не поможет
- Удобные хэндлеры - будет вызван обработчик, соответствующий полученной команде
- Работа с состояниями
- Легко загрузить изображение, сформировать ответ


### Установка

```bash
# рекомендуется использовать virtual env и python 3.6+:
python3.6 -m venv aliceenv
source ./aliceenv/bin/activate

pip install pip -U
pip install setuptools -U
pip install uvloop  # uvloop при желании

pip install aioalice -U
# Or install from GitHub:
# pip install git+https://github.com/surik00/aioalice.git -U

# Если git не установлен:
# 1. скачайте ZIP
# 2. разархивируйте и перейдите в папку
# 3. выполните следующую команду:
python setup.py install
```


### Быстрый старт

[Пример простейшего навыка](examples/hello-alice.py)

```python
dp = Dispatcher()

@dp.request_handler()
async def handle_all_requests(alice_request):
    return alice_request.response('Привет этому миру!')
```


### Карточки

- [Пример загрузки изображения](examples/upload_image.py)
- [Пример карточки с одним большим изображением](examples/card_big_image.py)
- [Пример карточки с альбомом из нескольких изображений](examples/card_items_list.py)

- [Все примеры](examples/README.md)


### JSON serializing

Если вы хотите использовать более быструю библиотеку для работы с JSON, установите [rapidjson](https://github.com/python-rapidjson/python-rapidjson) или [ujson](https://github.com/esnme/ultrajson). Библиотека определится и будет использована автоматически.

___

### Навыки с использованием aioAlice

* [Игра в Ерундопель](https://github.com/Goodsmileduck/erundopel)


___

### Тестирование и деплой


В примерах используется следующая конфигурация:

```python
WEBHOOK_URL_PATH = '/my-alice-webhook/'  # webhook endpoint

WEBAPP_HOST = 'localhost'  # запускаем на локальной машине
WEBAPP_PORT = 3001  # испльзуем любой не занятый порт
```

Для тестирования можно использовать [ngrok](https://ngrok.com/), тогда вебхук нужно будет установить на `https://1a2b3c4d5e.ngrok.io/my-alice-webhook/` (endpoint должен быть `WEBHOOK_URL_PATH`, так как WebApp ожидает получать обновления именно там), порт в настройках нужно указать `WEBAPP_PORT` (в данном случае 3001)


Для продакшена можно использовать Nginx, тогда в конфигурации Nginx внутри блока `server` необходимо добавить:

```
location /my-alice-webhook/ {  # WEBHOOK_URL_PATH
    proxy_pass         http://127.0.0.1:3001/;  # адрес до запущенного WebApp, в нашем случае это localhost и порт 3001
    proxy_redirect     off;
    proxy_set_header   Host $host;
    proxy_set_header   X-Real-IP $remote_addr;
    proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header   X-Forwarded-Host $server_name;
}
```
