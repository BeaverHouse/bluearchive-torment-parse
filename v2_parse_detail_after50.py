import csv
import json

# 빈 셀 확인하는 함수
def is_cell_blank(value) -> bool:
    return value is None or len(str(value).strip()) <= 0

# 파티가 존재하는지 확인하는 함수
# 스트라이커만 있어도 유효 파티
def party_exists(row, i:int) -> bool:
    if (i+1)*44 + 2 > len(row): return False
    return not (
        is_cell_blank(row[i*44+4]) and \
        is_cell_blank(row[i*44+11]) and \
        is_cell_blank(row[i*44+18]) and \
        is_cell_blank(row[i*44+25])
    )

def get_char_name(id) -> str:
    return char_json[str(id)] if not is_cell_blank(id) else ""

seasons = [
    # "B1",
    # "S50", "S51", "S52", "S53", "S54",
    # "S55", "S56", "S57",
    # "3S1-T"
    "3S2-T"
]

with open('character.json', encoding='utf-8') as f:
    char_json = json.load(f)

for season in seasons:
    f_csv = open("rawdetail/{}D.csv".format(season),'r')
    reader = csv.reader(f_csv)

    # 캐릭터 필터 저장용
    filters = []
    assist_filters = []
    under3_filters = []
    under4_filters = []

    # 전체 파티 저장용
    total_partys = []
    max_party_cnt = -1
    min_party_cnt = 1000

    # 이전 점수 저장용
    prev_score = 500000000
    
    for idx, row in enumerate(reader):
        if idx == 0 : continue

        dic = {}

        # 위에서부터 자르기
        if idx > 1500: break

        if is_cell_blank(row[0]): break
        
        score = int(row[1])
        
        # 점수차가 100만 이상 나면 insane 경계로 판단 : 확실X
        if prev_score < 100000000 and prev_score - score > 1000000 : break
        prev_score = score

        # 점수 순위 저장
        dic["rank"] = int(row[0])
        dic["score"] = int(row[1])

        i = 0
        partys = []
        
        under3_list = []
        under4_list = []

        # 전체 캐릭명 저장할 임시 array
        temp_char_array = []
            
        # 파티가 존재하면 파티 추가
        while party_exists(row, i):
            party = {}
            strikers = []
            for st_slot in range(4):
                begin_idx = i*44 + st_slot*7 + 4
                end_idx = i*44 + st_slot*7 + 11
                _, id, star, _, _, _, is_assist = row[begin_idx:end_idx]
                name = get_char_name(id)
                if is_assist.upper() == "TRUE":
                    dic["assist"] = name
                    assist_filters.append(name)
                if not is_cell_blank(star) and int(star) <= 4:
                    under4_list.append(name)
                    under4_filters.append(name)
                if not is_cell_blank(star) and int(star) <= 3:
                    under3_list.append(name)
                    under3_filters.append(name)
                strikers.append({
                    "name": name,
                    "star": int(star) if not is_cell_blank(star) else -1,
                    "assist": True if is_assist.upper() == "TRUE" else False
                })
                if len(name) > 0 and is_assist.upper() != "TRUE": 
                    temp_char_array.append(name)

            specials = []
            for sp_slot in range(2):
                begin_idx = i*44 + sp_slot*7 + 32
                end_idx = i*44 + sp_slot*7 + 39
                _, id, star, _, _, _, is_assist = row[begin_idx:end_idx]
                name = get_char_name(id)
                if is_assist.upper() == "TRUE":
                    dic["assist"] = name
                    assist_filters.append(name)
                if not is_cell_blank(star) and int(star) <= 4:
                    under4_list.append(name)
                    under4_filters.append(name)
                if not is_cell_blank(star) and int(star) <= 3:
                    under3_list.append(name)
                    under3_filters.append(name)
                specials.append({
                    "name": name,
                    "star": int(star) if not is_cell_blank(star) else -1,
                    "assist": True if is_assist.upper() == "TRUE" else False
                })
                if len(name) > 0 and is_assist.upper() != "TRUE": 
                    temp_char_array.append(name)

            party["strikers"] = strikers
            party["specials"] = specials

            partys.append(party)
               
            i += 1

        dic["partys"] = partys
        dic["party_count"] = len(partys)
        dic["under3"] = sorted(list(set(under3_list)))
        dic["under4"] = sorted(list(set(under4_list)))
        if len(partys) > max_party_cnt: max_party_cnt = len(partys)
        if len(partys) < min_party_cnt: min_party_cnt = len(partys)

        # 캐릭터 사용현황 dict에 정리
        total_char_dic = {}
        for char in temp_char_array:
            total_char_dic[char] = total_char_dic.get(char, 0) + 1
            
        dic["characters"] = sorted(list(total_char_dic.keys()))
        filters =           sorted(list(set(filters + dic["characters"])))

        print(".", end="")
        total_partys.append(dic)
        
    total_json = {
        "filter": filters,
        "assist_filter": sorted(list(set(assist_filters))),
        "under4_filter": sorted(list(set(under4_filters))),
        "under3_filter": sorted(list(set(under3_filters))),
        "partys": total_partys,
        "min_party": min_party_cnt,
        "max_party": max_party_cnt
    }

    # JSON 저장
    with open("result_detail/{}.json".format(season), "w", encoding='utf-8') as f:
        json.dump(total_json, f, indent=2, ensure_ascii=False)



