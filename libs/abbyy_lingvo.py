# coding: utf-8
from __future__ import unicode_literals
from pprint import pprint
import requests


class SERVER_EXCEPTION(Exception):
    pass


api_home = 'https://developers.lingvolive.com/api/'
api_key = 'MmI3MWMyYzQtZGE0YS00OWJhLTllYmEtYWQ5OTI0YzlhMjA2OmFjZTA3OGQ3MzNlZTRkYmI5ZTk2NmEwZThiOGRmMGRl'


def run(word):
    search_params = {"text": word,
                     "srcLang": 1049,
                     "dstLang": 1049
                     }
    try:
        response = requests.get(api_home + "v1/Translation", params=search_params,
                                headers={"Authorization": "Bearer {}".format(get_token())}, verify=False)
        if response.status_code != 200:
            raise SERVER_EXCEPTION
        response_json = response.json()
        pprint(response_json)
        text = response_json[0]["Body"][1]["Items"][0]["Markup"][0]["Markup"][0]["Text"]
        return text
    except SERVER_EXCEPTION:
        return "Ошибка сервера"
    except Exception:
        return "Нет толкования слова в словаре"


def get_token():
    token = requests.post(api_home + "v1.1/authenticate", headers={"Authorization": "Basic {}".format(api_key)},
                          verify=False)
    return token.text
print(run("куст"))

