# coding: utf-8
from __future__ import unicode_literals
from libs.abbyy_lingvo import run
from libs.apiai import *
import pymorphy2

apiai = ApiAI('b18d2a71bcd3409d851654c3b868af45')
morph = pymorphy2.MorphAnalyzer()


def handle_dialog(request, response, user_storage):
    if request.is_new_session:
        response.set_text('Привет! Назови слово, чтобы найти его определение')
        return response, user_storage
    else:
        txt = request.command.lower()
        req = extract_request(txt, request.session['session_id'])
        if req is None:
            response.set_text('Прости, у нас проблемы на сервере')
        else:
            response.set_text(run(req))
    return response, user_storage


def norm(x):
    return ' '.join(map(lambda y: morph.parse(y)[0].normal_form, x.split()))


def extract_request(x, s):
    if len(x.split()) == 1:
        return norm(x)
    try:
        res = apiai.run(x, s)
        if not is_incomplete(res):
            if get_action(res) == 'search':
                return norm(get_params(res)['text'])
            else:
                return get_fulfillment(res)
        else:
            return -1
    except Exception as e:
        print(e)
        return None
