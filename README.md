# ex-mecab

MeCabを（個人的に）利用しやすくするためのPythonモジュールです。
主な機能は以下の2つです。

- **MeCabの形態素解析結果をリストで受け取る**
- **条件付きで分かち書きする**

## 準備

作成者はWindowsの開発で64bit版を利用しているので、
[池上 有希乃](com/ikegami-yukino/mecab)さんが作成してくださった64bit版MeCabを利用しています。
また、以下コマンドにてPythonからMeCabを叩けるようにしておきます。

```shell
pip install mecab-python-windows
```

## 使い方

exmecabの使い方としては、基本以下の2ステップになります。

1. MeCabでの形態素解析
2. 解析結果を引数に与えることでほしい形で結果を得る

### MeCabでの形態素解析

基本的に上記でインストールするPython用のMeCabラッパーは、形態素解析結果を文字列で出力します。実行するためのプログラムと出力を以下に示します。ここで得られた文字列をexmecabを使って扱いやすい形に変形するという流れになります。

```python
# MeCabの実行
import MeCab

# MeCabのインスタンス化
tagger = MeCab.Tagger()
# チェック用文
test_text = "ヴィッセル神戸が大好きなRakuichiの推し選手は、古橋選手と菊池選手です。"
# MeCabで形態素解析
parse_result = tagger.parse(test_text)
print(parse_result)
```

```text
ヴィッセル      名詞,一般,*,*,*,*,*
神戸    名詞,固有名詞,地域,一般,*,*,神戸,コウベ,コーベ
が      助詞,格助詞,一般,*,*,*,が,ガ,ガ
大好き  名詞,形容動詞語幹,*,*,*,*,大好き,ダイスキ,ダイスキ
な      助動詞,*,*,*,特殊・ダ,体言接続,だ,ナ,ナ
Rakuichi        名詞,一般,*,*,*,*,*
の      助詞,連体化,*,*,*,*,の,ノ,ノ
推し    動詞,自立,*,*,五段・サ行,連用形,推す,オシ,オシ
選手    名詞,一般,*,*,*,*,選手,センシュ,センシュ
は      助詞,係助詞,*,*,*,*,は,ハ,ワ
、      記号,読点,*,*,*,*,、,、,、
古橋    名詞,固有名詞,人名,姓,*,*,古橋,フルハシ,フルハシ
選手    名詞,一般,*,*,*,*,選手,センシュ,センシュ
と      助詞,並立助詞,*,*,*,*,と,ト,ト
菊池    名詞,固有名詞,人名,姓,*,*,菊池,キクチ,キクチ
選手    名詞,一般,*,*,*,*,選手,センシュ,センシュ
です    助動詞,*,*,*,特殊・デス,基本形,です,デス,デス
。      記号,句点,*,*,*,*,。,。,。
EOS
```

### parse2list(mecab_parse_result)

上記の形態素解析結果を1単語ずつ要素に持つリストに変形する関数です。また、1単語の情報がnamedtupleで表現されます。引数にはMeCabでの解析結果を与えます。

```python
# parse2wakati：結果をリストで
result = exmecab.parse2list(parse_result)
print(result)
```

出力は以下のようになります。

```text
[Morpheme(surf='ヴィッセル', pos='名詞', posd1='一般', posd2='*', posd3='*', type_conj='*', conj='*', base='*', read='*', pron='*'), Morpheme(surf='神戸', pos='名詞', posd1='固有名詞', posd2='地域', posd3='一般', type_conj='*', conj='*', base='神戸', read='コウベ', pron='コーベ'), Morpheme(surf='が', pos='助詞', posd1='格助詞', posd2='一般', posd3='*', type_conj='*', conj='*', base='が', read='ガ', pron='ガ'), Morpheme(surf='大好き', pos='名詞', posd1='形容動詞語幹', posd2='*', posd3='*', type_conj='*', conj='*', base='大好き', read='ダイ
スキ', pron='ダイスキ'), Morpheme(surf='な', pos='助動詞', posd1='*', posd2='*', posd3='*', type_conj='特殊・ダ', conj='体言接続', base='だ', read='ナ', pron='ナ'), Morpheme(surf='Rakuichi', pos='名詞', posd1='一般', posd2='*', posd3='*', type_conj='*', conj='*', base='*', read='*', pron='*'), Morpheme(surf='の', pos='助詞', posd1='連体化', posd2='*', posd3='*', type_conj='*', conj='*', base='の', read='ノ', pron='ノ'), Morpheme(surf='推し', pos='動詞', posd1='自立', posd2='*', posd3='*', type_conj='五段・サ行', conj='連用形', base='推す', read='オシ', pron='オシ'), Morpheme(surf='選手', pos='名詞', posd1='一般', posd2='*', posd3='*', type_conj='*', conj='*', base='選手', read='センシュ', pron='センシュ'), Morpheme(surf='は', pos='助詞', posd1='係助詞', posd2='*', posd3='*', type_conj='*', conj='*', base='は', read='ハ', pron='ワ'), Morpheme(surf='、', pos='記号', posd1='読点', posd2='*', posd3='*', type_conj='*', conj='*', base='、', read='、', pron='、'), Morpheme(surf='古橋', pos='名詞', posd1='固有名詞', posd2='人名', posd3='姓', type_conj='*', conj='*', base='古橋', 
read='フルハシ', pron='フルハシ'), Morpheme(surf='選手', pos='名詞', posd1='一般', posd2='*', posd3='*', type_conj='*', conj='*', base='選手', read='センシュ', pron='センシュ'), Morpheme(surf='と', pos='助詞', posd1='並立助詞', posd2='*', posd3='*', type_conj='*', conj='*', base='と', read='ト', pron='ト'), Morpheme(surf='菊池', pos='名詞', posd1='固有名詞', posd2='人名', posd3='姓', type_conj='*', conj='*', base='菊池', read='キクチ', pron='キクチ'), Morpheme(surf='選手', pos='名詞', posd1='一般', posd2='*', posd3='*', type_conj='*', conj='*', base='選手', read='センシュ', pron='センシュ'), Morpheme(surf='です', pos='助動詞', posd1='*', posd2='*', posd3='*', type_conj='特殊・デス', conj='基本形', base='です', read='デス', pron='デス'), Morpheme(surf='。', pos='記号', posd1='句点', posd2='*', posd3='*', type_conj='*', conj='*', base='。', read='。', pron='。')]
```

このとき、各形態素の品詞のみを確認したい場合は以下のようにします。

```python
# 各形態素の品詞を確認
for morph in result1:
    print(morph.pos, end=" ")
```

出力

```text
名詞 名詞 助詞 名詞 助動詞 名詞 助詞 動詞 名詞 助詞 記号 名詞 名詞 助詞 名詞 名詞 助動詞 記号
```

MeCabの1形態素あたりの出力フォーマットとexmecab上での表現の対応を以下の表に示しておきます。
| Mecab       | exmecab   |
| ----------- | --------- |
| 表層形      | surf      |
| 品詞        | pos       |
| 品詞細分類1 | posd1     |
| 品詞細分類3 | posd2     |
| 品詞細分類3 | posd3     |
| 活用型      | type_conj |
| 活用形      | conj      |
| 原形        | base      |
| 読み        | read      |
| 発音        | pron      |

### parse2wakati(mecab_parse_result, form="base", pos="all")

parse2wakatiはいくつかの条件をつけて分かち書きを行う関数になります。
普通のMeCabでも分かち書きを行うことができます。exmecabでは「基本形で分かち書きをしたい」場合や「特定の品詞のみを残したい」といった条件付きの分かち書きを行うことができます。今対応している条件は以下の2つです。

- 表層形か基本形での出力
  - 基本形が「*」の場合は表層系で出力
- 残す形態素を決められる
  - 現在は品詞によるフィルターのみ対応

基本的には`parse2list`と同様にMeCabで形態素解析した結果を引数に受け取ることで、分かち書きされた状態に変換します。2つにパラメータに関して以下にまとめます。

- form
  - 説明：基本形で出力するなら`base`、表層形で出力するなら`surf`
- pos
  - 説明：残す品詞を選択する。複数残す場合はlist型で指定。すべて使う場合はdefaultのまま。
  - 入力例：`pos="名詞"`, `pos=["名詞", "助動詞"]`

これらを実際に使うと以下のようになります。

```python
result2 = exmecab.parse2wakati(parse_result)
result3 = exmecab.parse2wakati(parse_result, form="surf")
result4 = exmecab.parse2wakati(parse_result, form="surf", pos="名詞")
result5 = exmecab.parse2wakati(parse_result, form="surf", pos=["名詞", "助動詞"])

print(f"【parse2wakati（表層形で）】\n{result3}")
print(f"【parse2wakati（名詞のみ表層形）】\n{result4}")
print(f"【parse2wakati（デフォルト）】\n{result2}")
print(f"【parse2wakati（複数の品詞を指定して表層形）】\n{result5}")
```

出力

```text
【parse2wakati（デフォルト）】
ヴィッセル 神戸 が 大好き だ Rakuichi の 推す 選手 は 、 古橋 選手 と 菊池 選手 です 。
【parse2wakati（表層形で）】
ヴィッセル 神戸 が 大好き な Rakuichi の 推し 選手 は 、 古橋 選手 と 菊池 選手 です 。
【parse2wakati（名詞のみ表層形）】
ヴィッセル 神戸 大好き Rakuichi 選手 古橋 選手 菊池 選手
【parse2wakati（複数の品詞を指定して表層形）】
ヴィッセル 神戸 大好き な Rakuichi 選手 古橋 選手 菊池 選手 です
```