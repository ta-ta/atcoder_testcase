# -*- coding: utf-8 -*-

CPP = 'c++'
PY = 'py'
GO = 'go'
VALID_EXT = [CPP, PY, GO]
LANGUAGE_IDS = {CPP: 3003,
                PY: 3023,
                GO: 3013}

def get_file_extention(filename):
    # 拡張子の取得
    if '.' not in filename:
        return None
    return filename.split('.')[-1]