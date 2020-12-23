import os
import sys
import time

import requests
from dotenv import load_dotenv
from twilio.rest import Client


load_dotenv()
API_VERSION = 5.92
API_URL = 'https://api.vk.com/method/'
METHODS = {'users.get': 'users.get'}
acc_sid = os.getenv('acc_sid')
access_token = os.getenv('access_token')
auth_token = os.getenv('auth_token')
number_from = os.getenv('NUMBER_FROM')
number_to = os.getenv('NUMBER_TO')


def get_status(user_id):
    params = {
        'user_ids': user_id,
        'access_token': access_token,
        'v': API_VERSION,
        'fields': 'online',
    }
    try:
        user_status_request = requests.post(f'{API_URL}{METHODS["users.get"]}', params=params).json()
    except requests.RequestException:
        print('Что-то пошло не так ((')
        raise sys.exit()
    user_status = user_status_request['response'][0]['online']
    return user_status


def sms_sender(sms_text, client):
    message = client.messages.create(
        to=number_to,
        from_=number_from,
        body=sms_text,
    )
    return message.sid


if __name__ == '__main__':
    msg_client = Client(acc_sid, auth_token)
    vk_id = input('Введите id ')
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'{vk_id} сейчас онлайн!', msg_client)
            break
        time.sleep(5)
