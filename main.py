#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json, os
from time import sleep
import sys
import re
import urllib
reload(sys)
sys.setdefaultencoding("utf-8")
token_api = 'Your Token'
url = 'https://api.telegram.org/bot'+token_api+'/'
def getUpdates(offset=None, limit=None, timeout=None):
    Params = {
        'offset': offset,
        'limit': limit,
        'timeout': timeout
    }
    return json.loads(requests.get(url + 'getUpdates', params=Params).content.decode('utf8'))

def send_msg(chat_id, text, disable_web=None, reply_to_message_id=None, reply_markup=None):
    Params = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode':'HTML',
        'disable_web_page_preview': disable_web,
        'reply_to_message_id': reply_to_message_id,
        'reply_markup': reply_markup
    }
    return requests.get(url + 'sendMessage', params=Params)

def answerCallbackQuery(callback_query_id,text,show_alert=None):
    param = {
    'callback_query_id':callback_query_id,
    'text':text,
    'show_alert':show_alert
    }
    return requests.request(url + 'answerCallbackQuery', params=param, method='post')


"""
handler message              _____'_____
start & copy right negative /Taylor Team\ MIT
                           |______'______|
"""
def run ():
    last_update = 0
    while True:
        get_updates = getUpdates()
        for update in get_updates['result']:
            if last_update < update['update_id']:
                last_update = update['update_id']
                if 'message' in update:
                    chat_id = update['message']['chat']['id']
                    text = update['message']['text']
                    command = text
                    if(command == '/start' or command == '/help'):
                        getUpdates(last_update+1)
                        key = json.dumps({'inline_keyboard':[[{'text':'Developer 👓','url':'https://telegram.me/negative'},{'text':'Taylor Team 🔌','url':'https://telegram.me/taylor_team'}]]})
                        send_msg(chat_id,'<b>Taylor Team Development</b>',reply_markup=key)
                    if(command == '/time'):
                        getUpdates(last_update+1)
                        time = urllib.urlopen('http://api.gpmod.ir/time/').read()
                        data = json.loads(time)
                        en = data['ENtime']
                        msgg = '<b>Time Tehran :</b> {}'.format(en)
                        send_msg(chat_id,msgg,reply_to_message_id=update['message']['message_id'])

run()

