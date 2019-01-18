#!/usr/bin/env python3
# coding: UTF-8

import sys, re, math, json  # 数字の抽出など
import requests  # urlにGETリクエストしてhtmlを取得できる
from fake_useragent import UserAgent  # User-Agentを生成
import lxml.html  # BeautifulSoupよりlxmlの方が速いらしい

def get_result_number(word):
    '''
    Yahooから検索結果数を取得する関数です
    '''

    url = 'https://search.yahoo.co.jp/search'
    xpath = '//*[@id="Sf2"]/div/p[1]/span/text()'
    search_params = {
                    #'aq': '-1',
                    #'oq': '',
                    #'ts': '2',
                    'ei': 'UTF-8',
                    'p' : word,
                    #'fr': 'top_ga1_sa',
                    #'x': 'wrt',
                    }

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
            html_content = html.content

            # 取得したhtmlテキストからXPath指定で検索結果数を取り出す
            dom = lxml.html.fromstring(html_content)
            content = str(dom.xpath(xpath)[0])

            # 数字だけ抜き出し(コンマ等も省略)、int型に直す
            number_list = re.findall('([0-9]+)', content)
            str_result_number = ''
            for str_number in number_list:
                str_result_number += str_number

            # int型に直す
            result_number = int(str_result_number)

        except Exception as e:  # 予期せぬエラーが起きた場合
            if i < 9:
                print(e)
                print('retrying...')
                
            else:  # 10回トライしてだめなら異常終了
                print('エラーにより終了しました')
                sys.exit(1)

        else:  # 成功した場合はforループから抜ける
            break

    return(result_number)


def calculate_webPMI(num1, num2, num1_num2):
    '''
    webPMIを計算する関数です
    '''
    numer = num1_num2 / 10 ** 10
    denom = (num1 / 10 ** 10) * (num2 / 10 ** 10)
    webPMI = math.log2(numer / denom)

    return(webPMI)


def main():

    #visitor_tag_list = ['文学', '映画', '歴史', '経済', 'アニメ', '恋愛', '旅行', '科学', 
    #                    'アート', '芸能', 'ビジネス', 'コンピュータ', '法律', '政治', '環境', 
    #                    '軍事', '音楽', 'テレビ', 'SNS', '住宅', '哲学', '宗教', 'グルメ', '美容', 
    #                    'ファッション', '医学', '生物', '数学', '鉄道', '車', '占い', '料理', 
    #                    '写真', '絵画', 'ゲーム', '教育', 'スポーツ', 'アウトドア', '外国語', '漫画']

    visitor_tag_list = ['文学', '映画']

    exhibit_data = [
        {'exhibit': '月の満ち欠け','exhibit_id': 518,'exhibit_tag': ['月食', '満ち欠け', 'かぐや', '衛星']},
        {'exhibit': '惑星の動きと引力','exhibit_id': 521,'exhibit_tag': ['ケプラー', '万有引力', 'ニュートン', 'ブラックホール']},
        {'exhibit': '惑星探査','exhibit_id': 522,'exhibit_tag': ['探査機', 'ミッション', '惑星', 'タイムラグ']},
        {'exhibit': '銀河系と天の川','exhibit_id': 527,'exhibit_tag': ['銀河系', '天の川', '円盤', '断面図']},
        {'exhibit': 'プラネタリウムの歴史','exhibit_id': 529,'exhibit_tag': ['プラネタリウム', '歴史', 'オルゴール', 'カールツァイス']},
        {'exhibit': 'デジタルタイムカプセル','exhibit_id': 534,'exhibit_tag': ['旧名古屋市科学館', '歴史', '思い出', 'タイムカプセル']},
        {'exhibit': '天動説から地動説へ','exhibit_id': 502,'exhibit_tag': ['天動説', '地動説', 'ガリレオ', 'コペルニクス']},
        {'exhibit': '古代人の宇宙','exhibit_id': 501,'exhibit_tag': ['宇宙観', '神話', '占星術', '遺跡']},
        {'exhibit': '江戸時代の天文学','exhibit_id': 503,'exhibit_tag': ['江戸', '歴史', '地動説', '和製']},
        {'exhibit': '光学望遠鏡のしくみ','exhibit_id': 504,'exhibit_tag': ['レンズ', '屈折', '反射', '望遠鏡']},
        {'exhibit': '望遠鏡をのぞいてみよう','exhibit_id': 505,'exhibit_tag': ['倍率', '視野', '望遠鏡', '口径']},
        {'exhibit': 'さまざまな波長','exhibit_id': 508,'exhibit_tag': ['X線', '紫外線', '赤外線', '電波']},
        {'exhibit': '分光観測とスペクトル','exhibit_id': 509,'exhibit_tag': ['スペクトル', 'プリズム', '波長', '回折格子']},
        {'exhibit': '電波天文学','exhibit_id': 510,'exhibit_tag': ['電波', 'パラボラアンテナ', '宇宙背景放射', '無線']},
        {'exhibit': 'X線天文学','exhibit_id': 512,'exhibit_tag': ['X線', '超高温', '高エネルギー', 'レントゲン']},
        {'exhibit': '市街光と星空','exhibit_id': 513,'exhibit_tag': ['光害', '夜景', '環境', '都会']},
        {'exhibit': '宇宙線をみる','exhibit_id': 515,'exhibit_tag': ['宇宙線', '霧箱', '放射線', 'イオン']}
    ]

    recommend_list = []
    vtag_number_dict = {}
    etag_number_dict = {}
    vtag_etag_number_dict = {}

    for vtag_index, vtag in enumerate(visitor_tag_list):
        etag_index = 1
        if vtag in vtag_number_dict:
            vtag_number = vtag_number_dict[vtag]
        else:
            vtag_number = get_result_number(vtag)
            vtag_number_dict[vtag] = vtag_number

        for exhibit in exhibit_data:
            name = exhibit['exhibit']
            id = exhibit['exhibit_id']

            for etag in exhibit['exhibit_tag']:
                if etag in etag_number_dict:
                    etag_number = etag_number_dict[etag]
                else:
                    etag_number = get_result_number(etag)
                    etag_number_dict[etag] = etag_number
                
                vtag_etag = vtag + ' ' + etag
                if vtag_etag in vtag_etag_number_dict:
                    vtag_etag_number = vtag_etag_number_dict[vtag_etag]
                else:
                    vtag_etag_number = get_result_number(vtag_etag)
                    vtag_etag_number_dict[vtag_etag] = vtag_etag_number
                
                webPMI = calculate_webPMI(vtag_number, etag_number, vtag_etag_number)
                
                dict = {
                    "exhibit": name,"exhibit_id": id,"exhibit_tag": vtag,"exhibit_tag_id": vtag_index + 1,
                    "visitor_tag": etag,"visitor_tag_id": etag_index,"pmi_diff_from_med": webPMI
                }
                etag_index += 1
                recommend_list.append(dict)
                print(etag_index)

    with open('../json/WebPMI_iwata2.json', mode='w') as json_file:
        json.dump(recommend_list, json_file, indent=4, ensure_ascii=False)

if __name__=='__main__':
    main()
    sys.exit(0)