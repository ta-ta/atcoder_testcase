# テストケースの確認とサブミット
- テストケースを取得、保存する
- 作成したプログラムのテストを実行する
- サブミットする

## install
``` sh
cd
git clone https://github.com/tatakahashi35/atcoder_testcase.git

export ATCODER_TESTCASE="$HOME/.atcoder-testcase"
mkdir atcoder_testcase/testcases
```

## 実行方法
`python main.py 問題URL ファイル`  
```
$ python main.py --help
usage: main.py [-h] [-d] [-s] url file

positional arguments:
  url               problem URL
  file              program file

optional arguments:
  -h, --help        show this help message and exit
  -d, --redownload  re-download testcases
  -s, --submit      submit the file when all testcases pass
```

### 対象言語の設定
https://github.com/tatakahashi35/atcoder_testcase/blob/master/atcoder.py#L19-L26


### エイリアス設定
```
alias atc="python $HOME/atcoder_testcase/main.py"

atc https://atcoder.jp/contests/abc001/tasks/abc001_a A.c++ -s
```
