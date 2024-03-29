# simple-assembly-compiler
SIMPLE のアセンブリを機械語に変換してくれるすごいやつだよ

## 使用方法

```
$ python3 compiler.py < path/to/assembly/file
```

## 使用例

`examples/` 以下のファイルなどで動作確認できます

## 注意

とりあえず `examples/` の中のコードは動作確認しています。

## アセンブラの仕様

1行は、次のいずれかの形式のみ許容されています。

* `命令 引数1 引数2`
* `命令 引数`
* `命令`

引数には、レジスタまたは定数を渡すことができます。
定数は10進数の符号なし整数です(そのうち符号付きに対応します)。
レジスタは `レジスタ番号` という形式です。

`;` 以降の文字列はコメントになります。

たとえば次のようなコードが valid です。

```
XOR 3 3
LD 0 20(3)
LD 1 21(3)
LD 2 22(3)
ADD 1 2
SUB 0 1
OUT 0
HLT
```

ラベルを使うことができます。

```
B 0 end
; NOT EXECUTED
LI 0 10
OUT 0

end:
HLT
```

適宜 SIMPLE の仕様書を確認してください。
だいたいその通りに書けるはずです
