# -*- coding: utf-8 -*-

import os
import re
import subprocess
import time

import bs4
import requests

import config as CONFIG
import log
import util
from atcoder import AtCoder

logger = log.get_logger(__name__)


class TestCase:
    def __init__(self, problem_URL, problem_dir, testcase_preffix):
        self.problem_URL = problem_URL
        self.problem_dir = problem_dir
        self.testcase_preffix = testcase_preffix

        self.testcase_files = [] # [{'in': XXX.in, 'out': XXX.out, 'result': XXX.result, 'execution_time': None, 'status': ''}, ...]
        self.all_status = CONFIG.AC


    def get_local_testcases(self):
        """
        ローカルに保存されているテストケースファイルを取得する
        """
        os.makedirs(self.problem_dir, exist_ok=True)
        files = os.listdir(self.problem_dir) # 相対パス
        testcase_files_dict = {} # {'XXX.in': 'XXX.out', ...}
        # *.in
        for _file in files:
            if _file.split('-')[0] == self.testcase_preffix and util.get_extention(_file) == CONFIG.IN:
                testcase_files_dict[_file] = ''
        # *.out
        for _file in files:
            if _file.split('-')[0] == self.testcase_preffix and util.get_extention(_file) == CONFIG.OUT:
                file_in = _file.replace(f'.{CONFIG.OUT}', f'.{CONFIG.IN}')
                if file_in in testcase_files_dict:
                    testcase_files_dict[file_in] = _file

        for _in, _out in testcase_files_dict.items():
            testcase_number = os.path.basename(_in).split('-')[-1]
            _result = f'{self.testcase_preffix}-{testcase_number}.{CONFIG.RESULT}'

            in_filepath = os.path.join(self.problem_dir, _in)
            out_filepath = os.path.join(self.problem_dir, _out)
            result_filepath = os.path.join(self.problem_dir, _result)
            self.testcase_files.append({'in': in_filepath, 'out': out_filepath, 'result': result_filepath, 'execution_time': None, 'status': ''})
        self.testcase_files = sorted(self.testcase_files, key=lambda x:x['in'])


    def get_samples(self):
        """
        テストケースを取得し、ファイルに保存
        testcaseは、{problem_dir}/{testcase_preffix}-{number}.in の形で保存する
        """
        atcoder = AtCoder()
        atcoder.login()
        response = atcoder.session.get(self.problem_URL)
        response_html = bs4.BeautifulSoup(response.text, "html.parser")

        sections = response_html.find_all('section')
        for sec in sections:
            sample_message = sec.find('h3').string
            if re.match(r'^Sample ((In)|(Out))put [0-9]+', sample_message):
                testcase_number = sample_message.split()[-1]
                testcase = sec.find('pre').string
                if 'Input' in sample_message:
                    filename = f'{self.testcase_preffix}-{testcase_number}.{CONFIG.IN}'
                elif 'Output' in sample_message:
                    filename = f'{self.testcase_preffix}-{testcase_number}.{CONFIG.OUT}'
                else:
                    continue
                filepath = os.path.join(self.problem_dir, filename)
                with open(filepath, mode='w') as f:
                    f.write(testcase.strip())
        #####
        # 旧版?
        for sec in sections:
            sample_message = sec.find('h3').string
            if re.match(r'^(入力例|出力例)[0-9]+', sample_message):
                testcase_number = sample_message[3:]
                testcase = sec.find('pre').string
                if '入力例' in sample_message:
                    filename = f'{self.testcase_preffix}-{testcase_number}.{CONFIG.IN}'
                elif '出力例' in sample_message:
                    filename = f'{self.testcase_preffix}-{testcase_number}.{CONFIG.OUT}'
                else:
                    continue
                filepath = os.path.join(self.problem_dir, filename)
                with open(filepath, mode='w') as f:
                    f.write(testcase.strip())
        #####


    def test_all_testcase(self, execute_command):
        """
        全テストケース実行
        """
        for testcase in self.testcase_files:
            in_filepath = testcase['in']
            out_filepath = testcase['out']
            result_filepath = testcase['result']
            if out_filepath == '':
                continue

            execution_time = self.__test_testcase(in_filepath, result_filepath, execute_command)
            testcase['execution_time'] = execution_time
            result_status = self.__check_result(out_filepath, result_filepath, execution_time)
            testcase['status'] = result_status


    def __test_testcase(self, in_filepath, result_filepath, execute_command):
        """
        テスト実行
        """
        with open(in_filepath, 'r') as in_file, open(result_filepath, 'w', encoding='utf-8') as result_file:
            start = time.time()
            p = subprocess.Popen(execute_command,
                                    stdin=in_file,
                                    stdout=result_file,
                                    stderr=subprocess.PIPE)
            try:
                _, p_err = p.communicate(timeout=CONFIG.TEST_TIMEOUT)
            except subprocess.TimeoutExpired:
                p.kill()
                _, p_err = p.communicate()
            finally:
                end = time.time()

            if p.returncode != 0 and len(p_err) > 0:
                logger.error(p_err)
            return end - start


    def __check_result(self, out_filepath, result_filepath, execution_time):
        """
        実行結果を比較し、結果を出力する
        """
        with open(out_filepath, 'r') as out_file:
            out_lines = out_file.readlines()
        with open(result_filepath, 'r', encoding='utf-8') as result_file:
            result_lines = result_file.readlines()

        # 中身の比較
        # 行数
        if len(out_lines) != len(result_lines):
            self.all_status = CONFIG.WA
            return CONFIG.WA
        # 1行ずつ比較
        for out_line, result_line in zip(out_lines, result_lines):
            out_row = out_line.split()
            result_row = result_line.split()
            # 1行の文字数
            if len(out_row) != len(result_row):
                self.all_status = CONFIG.WA
                return CONFIG.WA
            # 1文字ずつ比較
            for out_row_col, result_row_col in zip(out_row, result_row):
                if out_row_col != result_row_col:
                    self.all_status = CONFIG.WA
                    return CONFIG.WA

        if execution_time < CONFIG.AC_TIMEOUT:
            return CONFIG.AC
        else:
            self.all_status = CONFIG.WA # TLE も WA 扱い
            return CONFIG.TLE


    def display(self):
        not_AC_count = 0
        testcases = 0
        for testcase in self.testcase_files:
            in_filepath = testcase['in']
            out_filepath = testcase['out']
            result_filepath = testcase['result']
            execution_time = testcase['execution_time']
            status = testcase['status']
            if out_filepath == '':
                continue

            # 各テストケースについて
            testcases += 1
            in_filename = os.path.basename(in_filepath)
            out_filename = os.path.basename(out_filepath)
            print(in_filename, '->', out_filename, end=' ')
            execution_time_msec = int(execution_time * 1000)

            if status == CONFIG.AC:
                print(CONFIG.AC_MESSAGE, end=' ')
            elif status == CONFIG.WA:
                not_AC_count += 1
                print(CONFIG.WA_MESSAGE, end=' ')
            elif status == CONFIG.TLE:
                not_AC_count += 1
                print(CONFIG.TLE_MESSAGE, end=' ')
            print(f'{execution_time_msec}ms')

            # WA のみ詳細表示
            if status == CONFIG.WA:
                # 正しい結果の出力
                with open(out_filepath) as out_file:
                    lines = out_file.readlines()
                    print('[want]')
                    for line in lines:
                        print(line, end='')
                    print()

                # 実行結果の出力
                with open(result_filepath) as result_file:
                    lines = result_file.readlines()
                    print('[result]')
                    for line in lines:
                        print(line, end='')
                    print('-'*42)

        if not_AC_count == 0:
            logger.info(f'all {testcases} testcases: {CONFIG.AC_MESSAGE}')
        else:
            logger.info(f'{not_AC_count} testcases: {CONFIG.WA_MESSAGE}')
