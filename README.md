# aioalice

## AsyncIO library for Yandex Alice (Yandex Dialogs) 


### Installation

```bash
# make sure you use virtual env and python 3.6+:
python3.6 -m venv aliceenv
source ./aliceenv/bin/activate


pip install git+https://github.com/surik00/aioalice.git

# or if you don't have git installed:
# 1. download ZIP
# 2. unarchive and go to dir
# 3. run:
python setup.py install
```


### JSON serializing

If you want to use a faster json library, install [rapidjson](https://github.com/python-rapidjson/python-rapidjson) or [ujson](https://github.com/esnme/ultrajson), it will be detected and used automatically
