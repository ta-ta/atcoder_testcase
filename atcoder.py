# -*- coding: utf-8 -*-

import getpass
import json
import os

import bs4
import requests
import termcolor

import config as CONFIG
import log
import util

logger = log.get_logger(__name__)


class AtCoder:
    # submit できる言語
    CPP_1 = 'c++'
    CPP_2 = 'cpp'
    PY = 'py'
    GO = 'go'
    LANGUAGE_IDS = {CPP_1: 4003, CPP_2: 4003,
                    PY: 4006,
                    GO: 4026}


    def __init__(self):
        self.session = requests.session()


    def __logging_status_code(self, status_code):
        if status_code == 200:
            return termcolor.colored(str(status_code), 'green', attrs=['bold'])
        return termcolor.colored(str(status_code), 'red', attrs=['bold'])


    def login(self):
        """
        atcoder に login する
        """
        try:
            # cookieは定期的にrefreshする必要あり？
            with open(CONFIG.COOKIE, mode='r') as f:
                cookie = json.load(f)
                for k, v in cookie.items():
                    self.session.cookies.set(k, v)
        except Exception as err:
            logger.warning(err)
            username = input('username: ')
            password = getpass.getpass('password: ')

            response = self.session.get(CONFIG.LOGIN_URL)
            logger.info('GET login page status: ' + self.__logging_status_code(response.status_code))
            response.raise_for_status()

            response_html = bs4.BeautifulSoup(response.text, 'html.parser')
            csrf_token = response_html.find('input', attrs={'name': 'csrf_token'})['value']

            login_data = {'username': username,
                            'password': password,
                            'csrf_token': csrf_token}
            response = self.session.post(CONFIG.LOGIN_URL, data=login_data)
            logger.info('POST login status: ' + self.__logging_status_code(response.status_code))
            response.raise_for_status()

            with open(CONFIG.COOKIE, mode='w') as f:
                cookie = self.session.cookies.get_dict()
                f.write(json.dumps(cookie))


    def __submit(self, problem_URL, source_code, language_id):
        response = self.session.get(problem_URL)
        logger.info('GET problem page status: ' + self.__logging_status_code(response.status_code))
        response.raise_for_status()

        response_html = bs4.BeautifulSoup(response.text, 'html.parser')
        TaskScreenName = problem_URL.split('/')[-1]
        csrf_token = response_html.find('input', attrs={'name': 'csrf_token'})['value']
        submit_URL = CONFIG.ATCODER + '/' + '/'.join(problem_URL.split('/')[3:5]) + '/submit'

        submit_data={'data.TaskScreenName': TaskScreenName,
                    'data.LanguageId': language_id,
                    'sourceCode': source_code,
                    'csrf_token': csrf_token}
        response = self.session.post(submit_URL, data=submit_data)
        logger.info('POST submit status: ' + self.__logging_status_code(response.status_code))
        response.raise_for_status()
        logger.info(CONFIG.WJ_MESSAGE)


    def submit_sourcecode(self, problem_URL, program_filepath):
        # ソースコード取得
        with open(program_filepath) as f:
            source_code = f.read()

        extension = util.get_extention(program_filepath)
        language_id = AtCoder.LANGUAGE_IDS.get(extension, None)
        if language_id is None:
            logger.warning('Invalid File extention')
            return

        self.__submit(problem_URL, source_code, language_id)
