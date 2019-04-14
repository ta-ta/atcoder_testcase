#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
python testcases.py https://atcoder.jp/contests/agc001/tasks/agc001_a A.c++
'''

import argparse
import json
import logging
import os
import re
import subprocess
import sys
import time

import bs4
import requests

import log
from submit import login, submit_sourcecode
from config import *
from valid_file_ext import *

PATH = os.path.dirname(os.path.abspath('__file__'))
logger = logging.getLogger(LOGGER)

def get_localfile(testcase_preffix):
    # ローカルに保存されているテストケースファイルを取得する
    # testcaseは、testcase_preffix-NUMBER.inの形で保存されている
    # return {'.in': '.out', ...}
    files = os.listdir(PATH)
    testcase_files = {}
    for file in files:
        if file.split('-')[0] == testcase_preffix and get_file_extention(file) == IN:
            testcase_files[file] = ''
    for file in files:
        if file.split('-')[0] == testcase_preffix and get_file_extention(file) == OUT:
            file_in = file.split('.')[0] + '.' + IN
            if file_in in testcase_files.keys():
                testcase_files[file_in] = file
    return sorted(testcase_files.items())

def get_samples(problem_URL, testcase_preffix):
    # テストケースを取得し、ファイルに保存
    # testcaseは、testcase_preffix-N.inの形で保存する
    session = requests.session()
    session = login(session)
    response = session.get(problem_URL)
    response_html = bs4.BeautifulSoup(response.text, "html.parser")

    sections = response_html.find_all('section')
    for sec in sections:
        sample_message = sec.find('h3').string
        if re.match(r'^Sample ((In)|(Out))put [0-9]+', sample_message):
            testcase_number = sample_message.split()[-1]
            testcase = sec.find('pre').string
            if 'Input' in sample_message:
                filename = testcase_preffix + '-' + str(testcase_number) + '.' + IN
            if 'Output' in sample_message:
                filename = testcase_preffix + '-' + str(testcase_number) + '.' +OUT
            with open(filename, mode='w') as f:
                f.write(testcase)


def make_compile_command(program_file, file_ext):
    # compile command 作成
    if file_ext == CPP:
        return ["g++", program_file, '-o', program_file.split('.')[0]]
    return None

def compile(compile_command):
    # コンパイルする
    p = subprocess.Popen(compile_command,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    _, p_err = p.communicate()
    if p.returncode != 0:
        logger.error('Compile Error')
        if len(p_err) > 0:
            logger.error(p_err)
        sys.exit(0)

def make_test_command(program_file, file_ext):
    # 実行コマンド作成
    if file_ext == CPP:
        return ['./'+program_file.split('.')[0]]
    if file_ext == PY:
        return ['python', program_file]
    if file_ext == GO:
        return ['go', 'run', program_file]
    return None

def sample_test(test_command, in_file):
    # テスト実行
    testcase_in = open(in_file, 'r')
    result = open(RESULT_FILE, 'w', encoding='utf-8')
    start = time.time()
    p = subprocess.Popen(test_command,
                            stdin=testcase_in,
                            stdout=result,
                            stderr=subprocess.PIPE)
    try:
        _, p_err = p.communicate(timeout=TEST_TIMEOUT)
        end = time.time()
    except subprocess.TimeoutExpired:
        p.kill()
        _, p_err = p.communicate()
        end = time.time()
    if p.returncode != 0 and len(p_err) > 0:
        logger.error(p_err)

    testcase_in.close()
    result.close()

    return end-start

def check(testcase_out, result):
    # 結果の比較
    if len(testcase_out) != len(result):
        return False
    for testcase_out_row, result_row in zip(testcase_out, result):
        testcase_out_row = testcase_out_row.split()
        result_row = result_row.split()
        if len(testcase_out_row) != len(result_row):
            return False
        for testcase_out_row_col, result_row_col in zip(testcase_out_row, result_row):
            if testcase_out_row_col != result_row_col:
                return False
    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='problem URL', type=str)
    parser.add_argument('file', help='program file', type=str)
    parser.add_argument('-d', '--redownload', help='re-download testcases', action='store_true')
    parser.add_argument('-s', '--submit', help='submit the file when all testcases pass', action='store_true')

    args = parser.parse_args()
    problem_URL = args.url
    program_file = args.file
    redownload = args.redownload
    submit = args.submit

    testcase_preffix = problem_URL.split('/')[-1]
    file_ext = get_file_extention(program_file)
    if file_ext not in VALID_EXT:
        logger.warning('Invalid File extention')
        sys.exit(0)

    # testcase 取得
    testcase_files = get_localfile(testcase_preffix)
    if len(testcase_files) == 0 or redownload:
        get_samples(problem_URL, testcase_preffix)
        testcase_files = get_localfile(testcase_preffix)

    # compile
    compile_command = make_compile_command(program_file, file_ext)
    if compile_command != None:
        compile(compile_command)

    # testコマンド作成
    test_command = make_test_command(program_file, file_ext)
    if test_command == None:
        logger.warning('Invalid File extention')
        sys.exit(0)

    not_AC_count = 0
    testcases = 0
    for in_file, out_file in testcase_files:
        if out_file == '':
            continue
        # test
        testcases += 1
        print(in_file, '->', out_file, end=' ')
        result_time_sec = sample_test(test_command, in_file)
        result_time_msec = int(result_time_sec * 1000)

        # 比較
        with open(out_file) as f:
            testcase_out = f.readlines()
        with open(RESULT_FILE) as f:
            result = f.readlines()
        if check(testcase_out, result):
            print(AC_MESSAGE, end=' ')
            if result_time_sec > AC_TIMEOUT:
                not_AC_count += 1
                print(TLE_MESSAGE, end=' ')
            print(str(result_time_msec) + 'ms')
        else:
            not_AC_count += 1
            print(WA_MESSAGE, end=' ')
            print(str(result_time_msec) + 'ms')

            print('[want]')
            for line in testcase_out:
                print(line, end='')

            print('[result]')
            for line in result:
                print(line, end='')
            print('-'*42)

    if not_AC_count == 0:
        logger.info('all ' + str(testcases) + ' testcases: '+ AC_MESSAGE)
        if submit:
            submit_sourcecode(problem_URL, program_file, file_ext)
    else:
        logger.info('at least one of ' + str(testcases) + ' testcases: '+ WA_MESSAGE)
