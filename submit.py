#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
`python ../scripts/submit.py https://atcoder.jp/contests/agc001/tasks/agc001_a A.c++`
'''

import argparse
import getpass
import json
import logging
import os
import sys

import bs4
import requests
import termcolor

import log
from config import *
from valid_file_ext import *

logger = logging.getLogger(LOGGER)

def logging_status_code(status_code):
    if status_code == 200:
        return termcolor.colored(str(status_code), 'green', attrs=['bold'])
    return termcolor.colored(str(status_code), 'red', attrs=['bold'])

def login(session):
    try:
        with open(COOKIE, mode='r') as f:
            cookie = json.load(f)
            for k, v in cookie.items():
                session.cookies.set(k, v)
    except Exception as err:
        logger.warning(err)
        username = input('username: ')
        password = getpass.getpass('password: ')

        response = session.get(LOGIN_URL)
        logger.info('GET login page status: ' + logging_status_code(response.status_code))
        response.raise_for_status()

        response_html = bs4.BeautifulSoup(response.text, 'html.parser')
        csrf_token = response_html.find('input', attrs={'name': 'csrf_token'})['value']
    
        login_data = {'username': username,
                        'password': password,
                        'csrf_token': csrf_token}
        response = session.post(LOGIN_URL, data=login_data)
        logger.info('POST login status: ' + logging_status_code(response.status_code))
        response.raise_for_status()

        with open(COOKIE, mode='w') as f:
            cookie = session.cookies.get_dict()
            f.write(json.dumps(cookie))
    return session

'''
def logout(session, csrf_token):
    logout_data={'csrf_token': csrf_token}
    response = session.post(LOGOUT_URL, data=logout_data)
    logger.info('POST logout status: ' + logging_status_code(response.status_code))
    response.raise_for_status()
'''

def submit(session, problem_URL, sourceCode, LanguageId):
    response = session.get(problem_URL)
    logger.info('GET problem page status: ' + logging_status_code(response.status_code))
    response.raise_for_status()

    response_html = bs4.BeautifulSoup(response.text, 'html.parser')
    TaskScreenName = response_html.find('input', attrs={'name': 'data.TaskScreenName'})['value']
    csrf_token = response_html.find('input', attrs={'name': 'csrf_token'})['value']
    submit_URL = ATCODER + response_html.find('form', attrs={'class': 'form-horizontal'})['action']

    submit_data={'data.TaskScreenName': TaskScreenName,
                'data.LanguageId': LanguageId,
                'sourceCode': sourceCode,
                'csrf_token': csrf_token}
    #response = session.post(submit_URL, data=submit_data)
    logger.info('POST submit status: ' + logging_status_code(response.status_code))
    response.raise_for_status()
    logger.info(WJ_MESSAGE)

    return csrf_token

def submit_sourcecode(problem_URL, program_file, file_ext):
    # ソースコード取得
    with open(program_file) as f:
        sourceCode = f.read()

    LanguageId = LANGUAGE_IDS.get(file_ext, None)
    if LanguageId == None:
        logger.warning('Invalid File extention')
        sys.exit(0)

    session = requests.session()
    session = login(session)
    csrf_token = submit(session, problem_URL, sourceCode, LanguageId)
    #logout(session, csrf_token)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='problem URL', type=str)
    parser.add_argument('file', help='program file', type=str)

    args = parser.parse_args()
    problem_URL = args.url
    program_file = args.file

    file_ext = get_file_extention(program_file)
    if file_ext not in VALID_EXT:
        logger.warning('Invalid File extention')
        sys.exit(0)

    submit_sourcecode(problem_URL, program_file, file_ext)
