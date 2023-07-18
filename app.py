# ----------------
# 基本設定
# ----------------
# ライブラリ読み込み
import streamlit as st
import numpy as np
from pandas import Series, DataFrame
import pandas as pd
import re
df = pd.read_csv('invoice_output.csv', usecols=lambda column: column not in ['Unnamed: 0'])
df = df.loc[~df['name'].isnull()]
st.set_page_config(layout="wide")
# ----------------
# サイドバー
# ----------------
# 関数記述
# サイドバーを作成する関数
def sidebar_select(df,col_name,help_text=None): # 引数（データフレーム, 項目名） 返り値（データフレーム, サイドバー）
    """
    単一選択の項目（事務区分など）の絞込を行うサイドバーを作成する。
    サイドバーでの選択は複数選択が可能とする。
    引数；
    df -> 元データのデータフレーム
    col_name -> サイドバーを作りたい項目名（列名） 
    返り値：
    df -> 絞込処理がされたデータフレーム
    side_multiselect -> st.sidebarオブジェクト
    """
    side_multiselect = st.sidebar.multiselect(col_name,set(df[col_name]),help=help_text)
    if len(side_multiselect)==0:
        pass
    elif set(side_multiselect) != set(df[col_name]):
        df = df.loc[df[col_name].isin(side_multiselect)]
    return df, side_multiselect

# sidebar.expanderの中に入れる場合はこちら
@st.cache_data
def expand_select(df,col_name): # 引数（データフレーム, 項目名） 返り値（データフレーム, サイドバー）
    """
    単一選択の項目（事務区分など）の絞込を行うサイドバーを作成する。
    サイドバーでの選択は複数選択が可能とする。
    引数；
    df -> 元データのデータフレーム
    col_name -> サイドバーを作りたい項目名（列名） 
    返り値：
    df -> 絞込処理がされたデータフレーム
    multiselect -> st.sidebarオブジェクト
    """
    multiselect = st.multiselect(col_name,set(df[col_name]),)
    if len(multiselect)==0:
        pass
    elif set(multiselect) != set(df[col_name]):
        df = df.loc[df[col_name].isin(multiselect)]
    return df, multiselect

def sidebar_select_multi(df,col_name,cols,help_text=None):
    """
    複数選択項目の絞込（手続対象など）を行うサイドバーを作成する
    引数；
    df -> 元データのデータフレーム
    col_name -> サイドバーを作りたい項目名（列名） 
    cols -> 選択項目として設置したい項目のリスト
    or_select -> Trueの場合、or検索となる
    返り値：
    df -> 絞込処理がされたデータフレーム
    side_multiselect -> st.sidebarオブジェクト
    """
    ## サイドバーの作成
    sidebar_obj = st.sidebar.multiselect(col_name,cols,help=help_text)
   
    or_select = st.sidebar.checkbox('or検索',key=col_name)
    # or検索がTrueの場合
    if or_select:
        if len(sidebar_obj) > 0:
            condition = False
            for col in sidebar_obj:
                condition = condition | df[col].isin(['対象', '対応'])
            df = df[condition]
        else:
            df = df
    # or検索がFalseの場合
    else:
        if len(sidebar_obj) > 0:
            condition = df[sidebar_obj[0]].isin(['対象', '対応'])
            df = df[condition]
            for col in sidebar_obj[1:]:
                condition = df[col].isin(['対象', '対応'])
                df = df[condition]
        else:
            df = df


    return df, sidebar_obj
# df, cp_name = sidebar_select_multi(df,"団体名",df['name'].unique(),)
def text_input_side(df,label,column):
    sidebar_obj = st.sidebar.text_input(label)
    # 検索文字列をスペースで分割して正規表現パターンを作成
    search_keywords = re.split(r'\s+', sidebar_obj)
    pattern = r'(?=.*' + ')(?=.*'.join(search_keywords) + ')'
    df = df.loc[df[column].str.contains(pattern, na=False,regex=True)]
    st.write(f"{label}：{sidebar_obj}")
    return df, sidebar_obj
# dantai = st.sidebar.text_input('会社/団体名')
# df = df.loc[df['name'].str.contains(dantai)]

#メイン画面
st.write('最終データ：2023-6-30')
st.info('🍆＜左のサイドバーから絞り込んでね。')

df, dantai = text_input_side(df,'会社/団体名','name')
# df, kana = text_input_side(df,'ふりがな','kana')
df, jusho = text_input_side(df,'住所','address')
print_df = df[['registratedNumber','name','kana','address']]
# st.write('団体名：',dantai)
st.write('該当のデータ数：',len(print_df))
index_num = st.number_input('表示する行数', value=10)
st.table(print_df.head(index_num))
# st.write(df.columns)