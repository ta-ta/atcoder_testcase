# -*- coding: utf-8 -*-

'''
python main.py https://atcoder.jp/contests/agc001/tasks/agc001_a A.c++ -s
'''

import argparse
import logging
import os
import sys

import config as CONFIG
import log
from atcoder import AtCoder
from program import Program
from testcase import TestCase

PATH = os.path.dirname(os.path.abspath('__file__'))
logger = log.get_logger(__name__)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='problem URL', type=str)
    parser.add_argument('file', help='program file', type=str)
    parser.add_argument('-d', '--redownload', help='re-download testcases', action='store_true')
    parser.add_argument('-s', '--submit', help='submit the file when all testcases pass', action='store_true')

    args = parser.parse_args()
    problem_URL = args.url
    program_filepath = args.file
    redownload = args.redownload
    submit = args.submit

    # 準備
    problem_URL_splitted = problem_URL.split('/')
    contest_name = problem_URL_splitted[-3]

    problem_dir = os.path.join(CONFIG.TESTCASES, contest_name)
    testcase_preffix = problem_URL_splitted[-1]
    program_file_abspath = os.path.join(PATH, program_filepath)

    # ファイルのフォーマットチェック
    program = Program(program_file_abspath)
    if program.check_invalid_extension():
        logger.warning('Invalid File extention')
        sys.exit(0)

    # testcase 取得
    testcase = TestCase(problem_URL, problem_dir, testcase_preffix)
    testcase.get_local_testcases()
    if len(testcase.testcase_files) == 0 or redownload:
        testcase.get_samples()
        testcase.get_local_testcases()
    if len(testcase.testcase_files) == 0:
        logger.warning('no testcases')
        sys.exit(0)

    # コンパイル、実行コマンドの準備
    program.compile()
    program.make_test_command()

    # 全テストケースチェック
    testcase.test_all_testcase(program.execute_command)
    testcase.display()

    # submit
    if testcase.all_status == CONFIG.AC and submit:
        atcoder = AtCoder()
        atcoder.login()
        atcoder.submit_sourcecode(problem_URL, program_filepath)
