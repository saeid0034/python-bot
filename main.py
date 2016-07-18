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
class JsonSerializable:
    def to_json(self):
        raise NotImplementedError

def getUpdates(offset=None, limit=None, timeout=None):
    Params = {
        'offset': offset,
        'limit': limit,
        'timeout': timeout
    }
    return json.loads(requests.get(url + 'getUpdates', params=Params).content.decode('utf8'))

def send_msg(chat_id, text, parse_mode=None, disable_web=None, reply_to_message_id=None, reply_markup=None):
    param = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode':'HTML'
    }
    if disable_web:
        param['disable_web_page_preview'] = disable_web
    if reply_to_message_id:
        param['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        param['reply_markup'] = reply_markup
    return requests.get(url + 'sendMessage', params=param)
def edit_msg(chat_id,message_id,text,parse_mode):
    param = {
    'chat_id':chat_id,
    'message_id':message_id,
    'text':text,
    'parse_mode':parse_mode,
    }
    return requests.post(url + 'editMessageText', params=param)

def send_photo(chat_id, photo, caption=None, reply_markup=None):
    param = {
    'chat_id':chat_id,
    }
    if caption:
        param['caption'] = caption
    if reply_markup:
        param['reply_markup'] = reply_markup
    file = {'photo':photo}
    return requests.post(url + 'sendPhoto', params=param, files=file)

def send_photo_file_id(chat_id, photo, caption=None, reply_markup=None):
    param = {
    'chat_id':chat_id,
    }
    if caption:
        param['caption'] = caption
    if reply_markup:
        param['reply_markup'] = reply_markup
    if photo:
        param['photo'] = photo
    return requests.post(url + 'sendPhoto', params=param)

def send_action(chat_id, action):
    param = {
    'chat_id':chat_id,
    'action':action
    }
    return requests.post(url + 'sendchataction', params=param)

def answerCallbackQuery(callback_query_id,text,show_alert=None):
    param = {
    'callback_query_id':callback_query_id,
    'text':text,
    'show_alert':show_alert
    }
    return requests.post(url + 'answerCallbackQuery', params=param)

def getUserProfilePhotos(user_id):
    param = {
    'user_id':user_id
    }
    return json.loads(requests.post(url + 'getUserProfilePhotos', params=param).content.decode('utf8'))

def answerInlineQuery(inline_query_id,results,cache_time):
    param = {
    'inline_query_id':inline_query_id,
    'results':results,
    }
    if cache_time:
        param['cache_time'] = cache_time
    return requests.post(url + 'answerInlineQuery', params=param)

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
                if 'message' in update or 'text' in update:
                    try:
                        chat_id = update['message']['chat']['id']
                        text = update['message']['text']
                        message = update['message']
                        command = text
                        if(command == '/start' or command == '/help'):
                            getUpdates(last_update+1)
                            send_action(chat_id,'typing')
                            key = json.dumps(
                            {'inline_keyboard':[[
                            {'text':'Developer 👓','url':'https://telegram.me/negative'},
                            {'text':'Taylor Team 🔌','url':'https://telegram.me/taylor_team'}
                            ],
                            [
                            {'text':'Your Info 🕶','url':'https://telegram.me/Taylor_tmtmbot?start=info'}
                            ],
                            [
                            {'text':'Taylor Team Inline','switch_inline_query':'taylor-team'}
                            ]
                            ]
                            })
                            send_msg(chat_id,'<b>Taylor Team Development</b>\ncommands : \n/time\n/about',reply_markup=key)
                        if(command == '/time'):
                            getUpdates(last_update+1)
                            send_action(chat_id,'typing')
                            time = urllib.urlopen('http://api.gpmod.ir/time/').read()
                            data = json.loads(time)
                            en = data['ENtime']
                            msgg = '<b>Time Tehran :</b> {}'.format(en)
                            send_msg(chat_id,msgg,reply_to_message_id=update['message']['message_id'])
                        if(command == '/about'):
                            getUpdates(last_update+1)
                            send_action(chat_id,'upload_photo')
                            markup = json.dumps({
                            'inline_keyboard':[
                            [
                            {'text':'👇 Taylor Team 👇','callback_data':'1'}
                            ],
                            [
                            {'text':'Developer 🕶','url':'https://telegram.me/negative'},
                            {'text':'Channel','url':'https://telegram.me/taylor_team'}
                            ]
                            ]
                            })
                            send_photo(chat_id,open('photo-2016-06-09-01-09-41.jpg'),caption='@Taylor_Team',reply_markup=markup)
                        if(command == '/info' or command == '/start info'):
                            getUpdates(last_update+1)
                            send_action(chat_id,'typing')
                            user_id = update['message']['from']['id']
                            username = update['message']['from']['username']
                            s = getUserProfilePhotos(update['message']['from']['id'])
                            markup = json.dumps(
                            {
                            'inline_keyboard':[
                            [
                            {'text':'{}'.format(username),'url':'https://telegram.me/{}'.format(username)}
                            ]
                            ]
                            }
                            )
                            send_photo_file_id(chat_id,photo=s['result']['photos'][0][2]['file_id'],caption='ID : {}\nUsername : @{}\n@Taylor_Team'.format(user_id,username),reply_markup=markup)
                        if(command == '/type'):
                            if(update['message']['reply_to_message']['entities'][0]['type']):
                                msg = update['message']['reply_to_message']['entities'][0]['type']
                                send_msg(chat_id,'<b>{}</b>'.format(msg))
                    except KeyError:
                        print 'error'
                if 'callback_query' in update:
                    getUpdates(last_update+1)
                    data = update['callback_query']['data']
                    call_id = update['callback_query']['id']
                    message_idd = update['callback_query']['message']['message_id']
                    id_from = update['callback_query']['message']['chat']['id']
                    if(data == '1'):
                        answerCallbackQuery(call_id,text='👇👇👇\nDeveloper: Negative\nTeam : Taylor Team\ncommands :\n/time\n/about\n/help',show_alert=True)
                if 'inline_query' in update:
                    getUpdates(last_update+1)
                    inline_query_idd = update['inline_query']['id']
                    inline_query_query = update['inline_query']['query']
                    if inline_query_query == 'taylor-team':
                        jso = json.dumps([{'type':'photo','id':'1','photo_url':'http://vip.opload.ir/vipdl/95/3/negative23/photo-2016-06-09-01-09-41.jpg','thumb_url':'http://vip.opload.ir/vipdl/95/3/negative23/photo-2016-06-09-01-09-41.jpg','caption':'@Taylor_Team'}])
                        answerInlineQuery(inline_query_id=inline_query_idd,results=[jso],cache_time=1)

run()
