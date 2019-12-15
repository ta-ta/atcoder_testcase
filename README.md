# テストケースの確認とサブミット
- テストケースを取得、保存する
- 作成したプログラムのテストを実行する
- サブミットする

## 事前準備
環境変数を設定する
```sh
export ATCODER_TESTCASE="$HOME/.atcoder-testcase"
```

## 使用方法
### テストケースの確認
`python testcase.py 問題URL ファイル`  
問題ページから`*-NUMBER.in`, `*-NUMBER.out`の形式で保存  
テストケースの確認をする  

オプション
- `-d`: テストケースの再取得
- `-s`: 全てのテストケースに通ったとき、サブミットする

### サブミット
`python submit.py 問題URL ファイル`  


### 対象言語
- C++14(GCC 5.4.1)
- Python3(3.4.3)
- Go(1.6)

`valid_file_ext.py` に追加することで他の言語にも対応可.  

---
alias atcoder-testcases="python XXX/atcoder_testcase/testcases.py"
