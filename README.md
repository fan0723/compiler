# LR0 parser
這是一個 LR0 parser 的實作，包含建立 parsing table, parsing 字串。
有關 LR0 parser 的詳細解析可見我的 hackmd。

# Dependencies
|Name|
|----|
|Pickle|
|Pandas|
|prettytable|

You can download by ```pip install pickle pandas prettytable```

## Shift Reduce Conflict
在 LR0 parsing 建表中一定會有 Shift/Reduce Conflict 的問題，在 LR0_parse_with_SRC.py 內使用 DFS 跑完全部可能性才停止，解決 SRC 問題。

## Exec
在 cmd 中下指令```python LR0.py```
如果輸入的文法具有 Shift Reduce Conflict，會詢問是否繼續並詢問是否使用 LR0_parse_with_SRC.py 執行。
二者檔案差異在是否有解決 Shift Reduce Conflict。
*執行過程中，會在執行資料夾下產生一個 table 資料夾儲存 parsing table 等資訊。*

### input
你可以將在 input 資料夾內修改你的 grammar, testdata。
並請在 LR0.py line:9 更改你選定的 grammar 比如 1_grammar 請輸入 ```input/1_```
修改 grammar 時請依照以下格式
```
1_grammer.txt
terminal: a, b        <- 定義 terminal
nonterminal: S, A     <- 定義 nonterminal
S->AA                 <- 此處開始定義 grammar
A->aA|b

1_testdata.txt
bb                    <- 直接輸入測試資料
ab
abab
```

Example:
![image](https://github.com/fan0723/Compiler-LR1-parser/assets/75062267/bc59f697-b698-4739-a7ae-fd10fc7c0f01)

![image](https://github.com/fan0723/Compiler-LR1-parser/assets/75062267/c16bdb8e-276b-48ea-bd7d-261779423d69)
