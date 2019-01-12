#!/usr/bin/env python3
# coding: UTF-8

import sys, re  # 数字の抽出など
import argparse  # 引数設定
import requests  # urlにGETリクエストしてhtmlを取得できる
from collections import OrderedDict  # 順序付きディクショナリ
from fake_useragent import UserAgent  # User-Agentを生成
import lxml.html  # BeautifulSoupよりlxmlの方が速いらしい

def get_result_number(engine,*words):
    '''
    検索結果数を取得する関数です(Yahoo, Googleから選択)
    '''
    result_dict = OrderedDict()  # 順序付きディクショナリを作成

    # Googleの場合のURL, xpath, クエリを設定
    if engine == 'google':
        url = 'https://www.google.co.jp/search'
        xpath = '//*[@id="resultStats"]/text()'
        search_params = {
                        'hl': 'ja',  # 日本語検索
                        'ie': 'UTF-8',  # クエリの文字コードをUTF-8に設定
                        'num': '1',  # 1ページあたり1件のみ表示
                        }

    # Yahooの場合のURL, xpath, クエリを設定
    elif engine == 'yahoo':
        url = 'https://search.yahoo.co.jp/search'
        xpath = '//*[@id="Sf2"]/div/p[1]/span/text()'
        search_params = {
                        #'aq': '-1',
                        #'oq': '',
                        #'ts': '2',
                        'ei': 'UTF-8',
                        #'fr': 'top_ga1_sa',
                        #'x': 'wrt',
                        }
    else:
        print('検索エンジン名を正しく選択してください')
        sys.exit(1)

    for search_word in words:  # (*)wordsの要素を1つずつ読み込み

        # Googleの場合{'q': search_word}をクエリに追加
        if engine == 'google':
            search_params['q'] = search_word

        # Yahooの場合{'p': search_word}をクエリに追加
        elif engine == 'yahoo':
            search_params['p'] = search_word

        else:
            print('検索エンジン名を正しく選択してください')

        # 以下スクレイピング部分
        # 原因不明のエラーが起きた場合は10回までリトライ
        for i in range(10):

            try:
                # user側の情報(OSやブラウザの種類など)をランダムで生成
                # pythonで機械的にアクセスしていることを隠す
                ua = UserAgent()
                random_headers = {'User-Agent': ua.random}

                # requestsを使ってhtmlの内容を取得
                html = requests.get(url, headers=random_headers, params=search_params)
                #print(html.url)
                html_content = html.content

                # 取得したhtmlテキストからXPath指定で検索結果数を取り出す
                dom = lxml.html.fromstring(html_content)
                content = str(dom.xpath(xpath)[0])

                # 数字だけ抜き出し(コンマ等も省略)、int型に直す
                number_list = re.findall('([0-9]+)', content)
                str_result_number = ''
                for str_number in number_list:
                    str_result_number += str_number

                # int型に直し、最初に作ったディクショナリに検索結果数を格納
                result_number = int(str_result_number)
                result_dict[search_word] = result_number

            except Exception as e:  # 予期せぬエラーが起きた場合
                if i < 9:
                    print(e)
                    print('retrying...')
                
                else:  # 10回トライしてだめなら異常終了
                    print('エラーにより終了しました')
                    sys.exit(1)

            else:  # 成功した場合はforループから抜ける
                break

    return(result_dict)

def main():
    '''
    来館者タグ・展示物タグから1つずつ取り出してwebPMIを計算するプログラムです(未完成)
    '''
    vtag_result_number = OrderedDict()
    stag_result_number = OrderedDict()
    stag_vtag_result_number = OrderedDict()

    # 引数設定
    argparser = argparse.ArgumentParser(
            description='Get number of result from search engine',  # プログラムの説明
            add_help=True, # -h/–help オプションの追加
            )
    argparser.add_argument('-e', '--engine',
            required=False, default = 'yahoo',  # 引数指定なしでもOK、デフォルトはYahoo
            help='type of search engine (yahoo or google)', type=str)  # helpを作成
    args = argparser.parse_args()  # 引数を解析
    engine_type = args.engine  # 受け取った引数を変数に代入


    # 受け取った引数がGoogleかYahooならプログラム開始
    if (engine_type == 'google') or (engine_type == 'yahoo'):

        # 来館者タグのテキストファイルを開いて1行ずつ読み込み
        # テキストファイルはBOMなしUTF-8のみ
        with open('../tag_collection/visitor_tag.txt','r',encoding='utf-8') as vtag_file:
            vtag_line = vtag_file.readline()
            
            while vtag_line:
                vtag = vtag_line.strip()  # 改行コードがあれば取り除く

                # 展示物タグのテキストファイルを開いて1行ずつ読み込み
                # テキストファイルはBOMなしUTF-8のみ
                with open('../tag_collection/showpiece_tag.txt','r',encoding='utf-8') as stag_file:
                    stag_line = stag_file.readline()

                    while stag_line:
                        stag = stag_line.strip()  # 改行コードがあれば取り除く

                        vtag_stag = vtag + ' ' + stag  # and検索用の文字列を生成
                        print(vtag_stag)
                        print(get_result_number(engine_type,*[vtag_stag]))  # 関数を使用

                        stag_line = stag_file.readline()  # 展示物タグの次の行を読み込み
            
                vtag_line = vtag_file.readline()  # 来館者タグの次の行を読み込み

    else:  # 受け取った検索エンジン名が適切でない場合
        print('検索エンジン名を正しく選択してください')
        sys.exit(1)

if __name__=='__main__':
    main()
    sys.exit(0)