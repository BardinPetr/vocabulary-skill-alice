# coding: utf-8
from __future__ import unicode_literals
from pprint import pprint
import requests


class SERVER_EXCEPTION(Exception):
    pass


api_home = 'https://developers.lingvolive.com/api/'
api_key = 'MmI3MWMyYzQtZGE0YS00OWJhLTllYmEtYWQ5OTI0YzlhMjA2OmFjZTA3OGQ3MzNlZTRkYmI5ZTk2NmEwZThiOGRmMGRl'


def get_token():
    token = requests.post(api_home + "v1.1/authenticate", headers={"Authorization": "Basic {}".format(api_key)},
                          verify=False)
    return token.text


tk = get_token()


def run(word, ttl=1):
    if ttl == -1:
        return "Нет толкования слова в словаре"
    search_params = {"text": word,
                     "srcLang": 1049,
                     "dstLang": 1049
                     }
    try:
        response = requests.get(api_home + "v1/Translation", params=search_params,
                                headers={"Authorization": "Bearer {}".format(tk)}, verify=False)
        data = response.json()
        text = ""
        for el in data[0].get('Body', []):
            items = el.get('Items')
            if items:
                for item in items:
                    for mrk in item.get('Markup', []):
                        for node in mrk.get('Markup', []):
                            if node.get('Node') != 'Text':
                                continue
                            if node.get('IsOptional'):
                                continue
                            text = node.get('Text')
                            return '{} - это {}'.format(word, text)
            else:
                for node in el.get('Markup', []):
                    if node.get('Node') != 'Text':
                        continue
                    text = node.get('Text')
                    return '{} - это {}'.format(word, text)
        if response.status_code != 200:
            raise SERVER_EXCEPTION
        if len(text.strip()) == 0:
            raise Exception
        return '{} - это {}'.format(word, text)
    except SERVER_EXCEPTION:
        return "Ошибка сервера"
    except Exception:
        if len(word.split()) > 1:
            return "Нет толкования слова в словаре"
        else:
            return run(correct(word), ttl - 1)


def correct(word):
    search_params = {"text": word,
                     "srcLang": 1049,
                     "dstLang": 1049
                     }
    try:
        response = requests.get(api_home + "v1/Suggests", params=search_params,
                                headers={"Authorization": "Bearer {}".format(tk)}, verify=False)
        if response.status_code != 200:
            raise SERVER_EXCEPTION
        response_json = response.json()[0]
        return response_json
    except Exception as e:
        print(e)
        return word
