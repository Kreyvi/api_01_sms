import os
import time

import requests
from dotenv import load_dotenv
from twilio.rest import Client


load_dotenv()


def get_status(user_id):
    access_token = os.getenv('access_token')
    params = {
        'user_ids': user_id,
        'access_token': access_token,
        'v': 5.92,
        'fields': 'online',
    }
    user_status = requests.post('https://api.vk.com/method/users.get', params=params).json()['response'][0]['online']
    return user_status


def sms_sender(sms_text):
    acc_sid = os.getenv('acc_sid')
    auth_token = os.getenv('auth_token')
    number_from = os.getenv('NUMBER_FROM')
    number_to = os.getenv('NUMBER_TO')
    client = Client(acc_sid, auth_token)
    message = client.messages.create(
        to=number_to,
        from_=number_from,
        body=sms_text,
    )
    return message.sid


if __name__ == '__main__':
    vk_id = input('Введите id ')
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
