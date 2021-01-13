import MeCab

import exmecab

# exmecabの変数名について
print(exmecab.morph_var_ja_dct)

# MeCabのインスタンス化
tagger = MeCab.Tagger()

# チェック用文
test_text = "ヴィッセル神戸が大好きなRakuichiの推し選手は、古橋選手と菊池選手です。"
# MeCabで形態素解析
parse_result = tagger.parse(test_text)

# parse2wakati：結果をリストで
result1 = exmecab.parse2list(parse_result)
print(f"【parse2list】\n{result1}")

print(f"【parse2list出力の扱い】")
for morph in result1:
    print(morph.pos, end=" ")
print()
    
# parse2wakati：形態素解析結果を色々な条件で分かち書き
result2 = exmecab.parse2wakati(parse_result)
print(f"【parse2wakati（デフォルト）】\n{result2}")

result3 = exmecab.parse2wakati(parse_result, form="surf")
print(f"【parse2wakati（表層形で）】\n{result3}")

result4 = exmecab.parse2wakati(parse_result, form="surf", pos="名詞")
print(f"【parse2wakati（名詞のみ表層形）】\n{result4}")

result5 = exmecab.parse2wakati(parse_result, form="surf", pos=["名詞", "助動詞"])
print(f"【parse2wakati（複数の品詞を指定して表層形）】\n{result5}")



