import re
from collections import namedtuple

# 変数名と日本語の対応辞書
morph_var_ja_dct = {
    "surf": "表層形",
    "pos": "品詞",
    "posd1": "品詞細分類1",
    "posd2": "品詞細分類2",
    "posd3": "品詞細分類3",
    "type_conj": "活用型",
    "conj": "活用形",
    "base": "原形",
    "read": "読み",
    "pron": "発音",
}

# namedtupleで形態素の情報を扱いやすくする
Morpheme = namedtuple(
    "Morpheme", "surf pos posd1 posd2 posd3 type_conj conj base read pron")


def _split_line(mecab_parse_result):
    """MeCabの形態素解析結果を1行ごとかつ、\tと,で分けた形にする

    Args:
        mecab_parse_result (str):  MeCabによる形態素解析の出力文字列

    Returns:
        list: MeCabの出力結果を1行ずつ、さらに列ごとに分けたリストを要素に持つリスト
    """
    # 形態素解析の結果を形態素単位に分解
    morpheme_info_str_lst = mecab_parse_result.rstrip("EOS\n").split("\n")

    result = []  # 出力結果用

    for morpheme_info_str in morpheme_info_str_lst:
        # 出力を分解
        morpheme_info_lst = re.split("[\t,]", morpheme_info_str)

        # いくつかの場合で出力フォーマットが揃っていないので*埋めする
        if len(morpheme_info_lst) != len(morph_var_ja_dct):
            num = len(morph_var_ja_dct) - len(morpheme_info_lst)
            morpheme_info_lst.extend(["*"]*num)

        result.append(morpheme_info_lst)

    return result


def _get_base_surf(morpheme_info, form):
    """指定された基本形か表層形のどちらかを取得する

    Args:
        morpheme_info (namedtuple:Morpheme): 形態素解析された1形態素情報
        form (str): "base" or "surf" 取得したい形を選ぶ

    Returns:
        str: 基本形or表層形
    """
    if form == "surf":
        return morpheme_info.surf

    if form == "base":
        base_morpheme = morpheme_info.base
        if base_morpheme == "*" or re.match("[a-xA-Z]+", base_morpheme):
            return morpheme_info.surf
        else:
            return base_morpheme


def parse2list(mecab_parse_result):
    """MeCabの形態素解析結果をリスト化する

    Args:
        mecab_parse_result (str): MeCabによる形態素解析の出力文字列

    Returns:
        list: 形態素を1要素に持つ、リスト化された形態素解析結果。
        要素はnamedtupleにより管理している。
    """
    # 前処理
    morpheme_info_lsts = _split_line(mecab_parse_result)
    # 形態素単位が要素となるリスト
    morpheme_lst = []

    for morpheme_info_lst in morpheme_info_lsts:
        # namedtupleを活用して形態素情報の保持
        morpheme_info = Morpheme(*morpheme_info_lst)
        morpheme_lst.append(morpheme_info)

    return morpheme_lst


def parse2wakati(mecab_parse_result, form="base", pos="all"):
    """いくつかの条件が付けられる分かち書き

    Args:
        mecab_parse_result (str): MeCabによる形態素解析の出力文字列。
        form (str, optional): 表層形(surf)か基本形(base)を選択。 Defaults to "base".
        pos (str or list, optional): 出力する品詞を指定。リストにすることで複数指定できる。Defaults to "all".

    Returns:
        str: 分かち書きされた結果。なにもない場合はNoneを返す。
    """

    # 前処理
    morpheme_info_lsts = _split_line(mecab_parse_result)
    # 最終的な出力に用いる形態素集合
    wkt_lst = []

    for morpheme_info_lst in morpheme_info_lsts:
        # namedtupleを活用して形態素情報の保持
        morpheme_info = Morpheme(*morpheme_info_lst)
        if pos == "all":
            # 品詞をすべて使う場合
            wkt_lst.append(_get_base_surf(morpheme_info, form))

        else:
            if isinstance(pos, list):
                # 品詞が複数存在している場合
                if morpheme_info.pos in pos:
                    wkt_lst.append(_get_base_surf(morpheme_info, form))

            else:
                # 一つのみ指定の場合
                if morpheme_info.pos == pos:
                    wkt_lst.append(_get_base_surf(morpheme_info, form))

    if len(wkt_lst) != 0:
        return " ".join(wkt_lst)
