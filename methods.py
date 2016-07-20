#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json, os
from time import sleep
import sys
import re
import config
import urllib
token_api = config.token
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

def download(url=None,name=None):
    urllib.urlretrieve(url,name)

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
    return requests.post(url + 'sendPhoto', params=param, files=file) # POST photo file no file_id

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
    return requests.post(url + 'sendPhoto', params=param) ## POST photo file_id no file

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
