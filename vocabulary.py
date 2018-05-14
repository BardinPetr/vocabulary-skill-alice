# coding: utf-8
from __future__ import unicode_literals
from libs.abbyy_lingvo import run


def handle_dialog(request, response, user_storage):
    if request.is_new_session:
        response.set_text('Привет! Ты открыл словарь русского языка!')
        return response, user_storage
    else:
        txt = request.command.lower()
        response.set_text('{} означает: {}'.format(txt, run(txt)))
    return response, user_storage
