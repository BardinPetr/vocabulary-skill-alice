# coding: utf-8
from __future__ import unicode_literals


def handle_dialog(request, response, user_storage):
    if request.is_new_session:
        response.set_text('Привет! Ты открыл словарь русского языка!')
        return response, user_storage

    if request.command.lower() in ['ладно', 'куплю', 'покупаю', 'хорошо']:
        response.set_text('Слона можно найти на Яндекс.Маркете!')
        return response, user_storage

    response.set_text('Все говорят "{}", а ты купи слона!'.format(request.command))

    return response, user_storage
