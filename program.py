# -*- coding: utf-8 -*-

import os
import subprocess

import config as CONFIG
import log
import util
from atcoder import AtCoder

logger = log.get_logger(__name__)


class Program:
    def __init__(self, problem_filepath):
        self.problem_filepath = problem_filepath
        self.extension = util.get_extention(self.problem_filepath)
        self.compile_command = []
        self.execute_command = []

        # コンパイルする場合
        problem_exe_filepath, _ = os.path.splitext(self.problem_filepath)
        self.problem_exe_filepath = problem_exe_filepath


    def check_invalid_extension(self):
        """
        拡張子の確認
        invalid なら True
        それ以外なら False
        """
        if self.extension not in AtCoder.LANGUAGE_IDS.keys():
            return True
        else:
            return False


    def __make_compile_command(self):
        """
        compile command 作成
        """
        if self.extension == AtCoder.CPP_1 or self.extension == AtCoder.CPP_2:
            self.compile_command = ["g++", self.problem_filepath, '-O2', '-o', self.problem_exe_filepath]


    def compile(self):
        """
        コンパイルする
        """
        self.__make_compile_command()
        if self.compile_command == []:
            return

        p = subprocess.Popen(self.compile_command,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        _, p_err = p.communicate()
        if p.returncode != 0:
            logger.error('Compile Error')
            if len(p_err) > 0:
                logger.error(p_err)
            return


    def make_test_command(self):
        # 実行コマンド作成
        if self.extension == AtCoder.CPP_1 or self.extension == AtCoder.CPP_2:
            self.execute_command = [self.problem_exe_filepath]
        elif self.extension == AtCoder.PY:
            self.execute_command = ['python', self.problem_exe_filepath]
        elif self.extension == AtCoder.GO:
            self.execute_command = ['go', 'run', self.problem_exe_filepath]
