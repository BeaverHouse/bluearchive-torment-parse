import csv
import json

# 빈 셀 확인하는 함수
def is_cell_blank(value) -> bool:
    return value is None or len(str(value).strip()) <= 0

# 파티가 존재하는지 확인하는 함수
# 스트라이커만 있어도 유효 파티
def party_exists(row, i:int) -> bool:
    if i*8 + 10 > len(row): return False
    return not (
        row[i*8+4] == -1 and \
        row[i*8+5] == -1 and \
        row[i*8+6] == -1 and \
        row[i*8+7] == -1
    )

seasons = [
    # "B1",
    # "S47", "S48", "S49", "S50", "S51", "S52", "S53", "S54",
    "S55", "S56"
]

with open('character.json', encoding='utf-8') as f:
    char_json = json.load(f)

for season in seasons:
    f_csv = open("rawdata/{}.csv".format(season),'r')
    reader = csv.reader(f_csv)

    # 캐릭터 필터 저장용
    filters = []
    assist_filters = []

    # 전체 파티 저장용
    total_partys = []
    max_party_cnt = -1
    min_party_cnt = 1000

    # 이전 점수 저장용
    prev_score = 500000000
    
    for idx, row in enumerate(reader):
        if idx == 0 : continue

        dic = {}

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

        # 전체 캐릭명 저장할 임시 array
        temp_char_array = []
            
        # 파티가 존재하면 파티 추가
        while party_exists(row, i):
            party = {}
            strikers = list(filter(
                lambda x1: x1 is not None and len(x1) > 0,
                list(map(lambda x2: char_json[str(x2)] if int(x2) != -1 else "", row[i*8+4:i*8+8]))
            ))
            specials = list(filter(
                lambda x1: x1 is not None and len(x1) > 0,
                list(map(lambda x2: char_json[str(x2)] if int(x2) != -1 else "", row[i*8+8:i*8+10]))
            ))
            party["strikers"] = strikers
            party["specials"] = specials

            # 임시 array에 캐릭터들 추가
            temp_char_array += strikers + specials

            partys.append(party)
               
            i += 1

        dic["partys"] = partys
        dic["party_count"] = len(partys)
        if len(partys) > max_party_cnt: max_party_cnt = len(partys)
        if len(partys) < min_party_cnt: min_party_cnt = len(partys)

        # 캐릭터 사용현황 dict에 정리
        total_char_dic = {}
        for char in temp_char_array:
            total_char_dic[char] = total_char_dic.get(char, 0) + 1
            
        dic["characters"] = list(total_char_dic.keys())
        filters = list(set(filters + dic["characters"]))
            
        # 2번쓰면 무조건 조력자
        for char in total_char_dic.keys():
            if total_char_dic.get(char, 0) == 2:
                dic["assist"] = char
                if char not in assist_filters:
                    assist_filters.append(char)
                break

        print(".", end="")
        total_partys.append(dic)
        
    total_json = {
        "filter": filters,
        "assist_filter": assist_filters,
        "partys": total_partys,
        "min_party": min_party_cnt,
        "max_party": max_party_cnt
    }

    # JSON 저장
    with open("result/{}.json".format(season), "w", encoding='utf-8') as f:
        json.dump(total_json, f, indent=2, ensure_ascii=False)



