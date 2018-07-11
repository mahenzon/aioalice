<p align="center">
    <a href="README.md">Русский</a> | English
</p>


# aioalice

## AsyncIO library for Yandex Alice (Yandex Dialogs) 


## Why?
- Work with classes, don't bother parsing JSON
- Auto answer to webhook even if you were not fast enough to create answer - there won't be a server error, but you'll get a log
> Auto response will not help if you are not using async IO. So consider not to use any long processing synchronous tasks inside handlers
- Handy handlers to match incoming commands
- Finite-State Machine


### Installation

```bash
# make sure you use virtual env and python 3.6+:
python3.6 -m venv aliceenv
source ./aliceenv/bin/activate

pip install pip -U
pip install setuptools -U
pip install uvloop  # uvloop recommended

pip install git+https://github.com/surik00/aioalice.git

# or if you don't have git installed:
# 1. download ZIP
# 2. unarchive and go to dir
# 3. run:
python setup.py install
```


### JSON serializing

If you want to use a faster json library, install [rapidjson](https://github.com/python-rapidjson/python-rapidjson) or [ujson](https://github.com/esnme/ultrajson), it will be detected and used automatically
