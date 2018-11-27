<p align="center">
    <a href="README.md">Русский</a> | English
</p>


# aioAlice

## AsyncIO library for Yandex Alice (Yandex Dialogs) 


## Why?
- Work with classes, don't bother parsing JSON
- Auto answer to webhook even if you were not fast enough to create answer - there won't be a server error, but you'll get a log
> Auto response will not help if you are not using async IO. So consider not to use any long processing synchronous tasks inside handlers
- Handy handlers to match incoming commands
- Finite-State Machine
- Easy images upload, easy answers generation


### Installation

```bash
# make sure you use virtual env and python 3.6+:
python3.6 -m venv aliceenv
source ./aliceenv/bin/activate

pip install pip -U
pip install setuptools -U
pip install uvloop  # uvloop if you want, but it can cause some problems

pip install aioalice -U
# Or install from GitHub:
# pip install git+https://github.com/surik00/aioalice.git -U

# or if you don't have git installed:
# 1. download ZIP
# 2. unarchive and go to dir
# 3. run:
python setup.py install
```


### Quick start

[Hello alice](examples/hello-alice.py)

```python
dp = Dispatcher()

@dp.request_handler()
async def handle_all_requests(alice_request):
    return alice_request.response('Hello world!')
```


### Cards

- [Upload image example](examples/upload_image.py)
- [Big Image Card example](examples/card_big_image.py)
- [Items List Card example](examples/card_items_list.py)

- [All examples](examples/README-en.md)


### JSON serializing

If you want to use a faster json library, install [rapidjson](https://github.com/python-rapidjson/python-rapidjson) or [ujson](https://github.com/esnme/ultrajson), it will be detected and used automatically

___

### Skills using aioAlice

* [The Erundopel game](https://github.com/Goodsmileduck/erundopel)


___

### Testing and deployment


In all examples the next configuration is used:

```python
WEBHOOK_URL_PATH = '/my-alice-webhook/'  # webhook endpoint

WEBAPP_HOST = 'localhost'  # running on local machine
WEBAPP_PORT = 3001  # we can use any port that is not use by other apps
```

For testing purposes you can use [ngrok](https://ngrok.com/), so set webhook to `https://1a2b3c4d5e.ngrok.io/my-alice-webhook/` (endpoint has to be `WEBHOOK_URL_PATH`, because WebApp expects to get updates only there), post has to be `WEBAPP_PORT` (in this example it is 3001)


For production you can use Nginx, then edit Nginx configuration and add these lines inside the `server` block:

```
location /my-alice-webhook/ {  # WEBHOOK_URL_PATH
    proxy_pass         http://127.0.0.1:3001/;  # addr to reach WebApp, in this case it is localhost and port is 3001
    proxy_redirect     off;
    proxy_set_header   Host $host;
    proxy_set_header   X-Real-IP $remote_addr;
    proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header   X-Forwarded-Host $server_name;
}
```
