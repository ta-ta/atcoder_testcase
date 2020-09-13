# -*- coding: utf-8 -*-

CPP = 'c++'
PY = 'py'
GO = 'go'
VALID_EXT = [CPP, PY, GO]
LANGUAGE_IDS = {CPP: 4003,
                PY: 4006,
                GO: 4026}

def get_file_extention(filename):
    # 拡張子の取得
    if '.' not in filename:
        return None
    return filename.split('.')[-1]