import os


def get_extention(filepath):
    """
    拡張子の取得
    """
    _, ext = os.path.splitext(filepath)
    if ext.startswith('.'):
        return ext[1:]
    else:
        return ext
