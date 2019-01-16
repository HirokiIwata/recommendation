import sys, json, itertools

with open('../json/WebPMI_iwata.json',encoding='utf-8') as json_file:
    rcm_data = json.load(json_file)

def decide_recommended_exhibit(*vtags):
    '''
    来館者タグのリストを渡すとおすすめの展示物を3つ返す関数です
    '''
    exhibit_score = []

    for vtag in vtags:

        # jsonファイルから展示物タグがvtagのディクショナリを抽出してリストに格納
        sorted_rcm_data = [item for item in rcm_data if item['exhibit_tag'] == vtag]
        # pmiの大きい順に並び替え
        sorted_rcm_data.sort(key=lambda x: x['pmi_diff_from_med'],reverse=True)

        for data in sorted_rcm_data:  # sorted_rcm_dataの上位から要素(ディクショナリ)を1つずつ取り出してdataへ
            if len(exhibit_score) >= 3:
                break
            flag = 0
            for criteria in exhibit_score:  # exhibit_scoreから要素(ディクショナリ)を1つずつ取り出しcriteriaへ
                if criteria['exhibit'] == data['exhibit']:  # criteriaにすでにdataの展示物が入っている場合
                    pmi_avg_numerator = (criteria['score'] * criteria['pmi_avg'] + data['pmi_diff_from_med'])
                    criteria['score'] += 1
                    criteria['pmi_avg'] = pmi_avg_numerator / criteria['score']
                    flag = 1
                    break
            if flag == 0:  # フラグが立たなければ
                exhibit_score.append({'exhibit': data['exhibit'], 'score': 1, 'pmi_avg': data['pmi_diff_from_med']})
            
        exhibit_score.sort(key=lambda x:(x['score'],x['pmi_avg']), reverse=True)
        print(exhibit_score)
        recommended_exhibit = []
        for exhibit in exhibit_score[:3]:
            recommended_exhibit.append(exhibit['exhibit'])

    return(recommended_exhibit)

def main():
    visitor_tag = ['文学', '映画', '歴史', '経済', 'アニメ', '恋愛', '旅行', '科学', 
                   'アート', '芸能', 'ビジネス', 'コンピュータ', '法律', '政治', '環境', 
                   '軍事', '音楽', 'テレビ', 'SNS', '住宅', '哲学', '宗教', 'グルメ', '美容', 
                   'ファッション', '医学', '生物', '数学', '鉄道', '車', '占い', '料理', 
                   '写真', '絵画', 'ゲーム', '教育', 'スポーツ', 'アウトドア', '外国語', '漫画']

    exhibit_recommended_times = {'月の満ち欠け': 0, '惑星の動きと引力': 0, '惑星探査': 0,
                                 '銀河系と天の川': 0, 'プラネタリウムの歴史': 0,
                                 'デジタルタイムカプセル': 0, '天動説から地動説へ': 0,
                                 '古代人の宇宙': 0, '江戸時代の天文学': 0,
                                 '光学望遠鏡のしくみ': 0, '望遠鏡をのぞいてみよう': 0,
                                 'さまざまな波長': 0, '分光観測とスペクトル': 0,
                                 '電波天文学': 0, 'X線天文学': 0, '市街光と星空': 0,
                                 '宇宙線をみる': 0}

    check_visitor_tag = []
    for i in range(1):
        for word in itertools.permutations(visitor_tag, i+1):
            word_list = list(word)
            check_visitor_tag.append(word_list[0])
            #print(decide_recommended_exhibit(*word_list))
            for exhibit in decide_recommended_exhibit(*word_list):
                exhibit_recommended_times[exhibit] += 1

    times_list = exhibit_recommended_times.values()
    print(exhibit_recommended_times)
    print(times_list)
    for exhibit_name, times in exhibit_recommended_times.items():
        ratio = int((times / sum(times_list)) * 100)
        graph = int(ratio / 3)
        print(exhibit_name,'■'*graph,str(ratio)+'%')
    print(sum(times_list))



if __name__=='__main__':
    main()
    sys.exit(0)
