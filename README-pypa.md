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
pip install uvloop  # uvloop if you want

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

[Hello alice](https://github.com/surik00/aioalice/blob/master/examples/hello-alice.py)

```python
dp = Dispatcher()

@dp.request_handler()
async def handle_all_requests(alice_request):
    return alice_request.response('Hello world!')
```


### Cards

- [All examples](https://github.com/surik00/aioalice/blob/master/examples/README-en.md)

- [Upload image example](https://github.com/surik00/aioalice/blob/master/examples/upload_image.py)
- [Big Image Card example](https://github.com/surik00/aioalice/blob/master/examples/card_big_image.py)
- [Items List Card example](https://github.com/surik00/aioalice/blob/master/examples/card_items_list.py)


### JSON serializing

If you want to use a faster json library, install [rapidjson](https://github.com/python-rapidjson/python-rapidjson) or [ujson](https://github.com/esnme/ultrajson), it will be detected and used automatically
