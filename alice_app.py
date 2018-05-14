# coding: utf-8
from __future__ import unicode_literals
import logging

from libs.alice_sdk import AliceRequest, AliceResponse
from vocabulary import handle_dialog
from flask import Flask, request

application = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

session_storage = {}


@application.route("/", methods=['POST'])
def main():
    alice_request = AliceRequest(request.json)
    logging.info('Request: {}'.format(alice_request))

    alice_response = AliceResponse(alice_request)

    user_id = alice_request.user_id

    alice_response, session_storage[user_id] = handle_dialog(
        alice_request, alice_response, session_storage.get(user_id)
    )

    logging.info('Response: {}'.format(alice_response))

    return alice_response.dumps()


alice_app = application

if __name__ == '__main__':
    application.run()
