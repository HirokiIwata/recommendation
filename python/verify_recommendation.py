import json

exhibit_score = []

with open('../json/WebPMI.json',encoding='utf-8') as json_file:
    rcm_data = json.load(json_file)

def decide_recommended_exhibit(*vtags):
    for vtag in vtags:
        sorted_rcm_data = [item for item in rcm_data if item['visitor_tag'] == vtag]  # jsonファイルから展示物タグが月食のディクショナリを抽出してリストに格納
        sorted_rcm_data.sort(key=lambda x: x['pmi_diff_from_med'],reverse=True)  # pmiの大きい順に並び替え

        for data in sorted_rcm_data[:3]:  # sorted_rcm_dataの上位3つから要素(ディクショナリ)を1つずつ取り出してdataへ
            flag = 0
            for criteria in exhibit_score:  # exhibit_scoreから要素(ディクショナリ)を1つずつ取り出しcriteriaへ
                if criteria['exhibit'] == data['exhibit']:  # criteriaにすでにdataの展示物が入っている場合
                    criteria['score'] += 1
                    flag = 1
                    break
            if flag == 0:  # フラグが立たなければ
                exhibit_score.append({'exhibit': data['exhibit'], 'score': 1, 'avg_pmi': data['pmi_diff_from_med']})
            
        print(exhibit_score)
