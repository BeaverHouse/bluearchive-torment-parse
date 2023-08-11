import json
import sys

seasons = [
    "B1",
    "S48", "S49", "S50", "S51", "S52", "S53", "S54",
    "S55", "S56"
]

for season in seasons:
    with open('result/{}.json'.format(season), encoding='utf-8') as f:
        old_json = json.load(f)
    with open('result_detail/{}.json'.format(season), encoding='utf-8') as f:
        new_json = json.load(f)

    if set(old_json["filter"]) != set(new_json["filter"]):
        print("{} : 필터가 다릅니다.".format(season))
        sys.exit()
    elif old_json["min_party"] != new_json["min_party"]:
        print("{} : 최소 파티가 다릅니다.".format(season))
        sys.exit()
    elif old_json["max_party"] != new_json["max_party"]:
        print("{} : 최소 파티가 다릅니다.".format(season))
        sys.exit()

    old_partys = old_json["partys"]
    new_partys = new_json["partys"]

    if len(old_partys) != len(new_partys):
        print("{} : 토먼트 파티 수가 다릅니다.".format(season))
        sys.exit()
    
    for idx, old_pt in enumerate(old_partys):
        new_pt = new_partys[idx]
        if old_pt["score"] != new_pt["score"] or old_pt["rank"] != new_pt["rank"]:
            print("{} : {} 번째 토먼트 점수, 랭킹이 다릅니다.".format(season, idx+1))
            sys.exit()
        elif set(old_pt["characters"]) != set(new_pt["characters"]):
            print("{} : {} 번째 캐릭터 풀이 다릅니다.".format(season, idx+1))
            sys.exit()
        elif old_pt["party_count"] != new_pt["party_count"]:
            print("{} : {} 번째 파티 수가 다릅니다.".format(season, idx+1))
            sys.exit()
        elif old_pt.get("assist") is not None and new_pt.get("assist") is not None and old_pt["assist"] != new_pt["assist"]:
            print("{} : {} 번째 조력자가 다릅니다.".format(season, idx+1))
            sys.exit()
        
        for p_idx, old_pt_part in enumerate(old_pt["partys"]):
            new_pt_part = new_pt["partys"][p_idx]
            if list(filter(lambda x: len(x) > 0,
                list(map(lambda x: x["name"], new_pt_part["strikers"]))
            )) != old_pt_part["strikers"]:
                print("{} : {} 번째 스트라이커 배치 또는 구성이 다릅니다.".format(season, idx+1))
                sys.exit()
            if list(filter(lambda x: len(x) > 0,
                list(map(lambda x: x["name"], new_pt_part["specials"]))
            )) != old_pt_part["specials"]:
                print("{} : {} 번째 스페셜 배치 또는 구성이 다릅니다.".format(season, idx+1))
                sys.exit()

    
    print("{} 정상".format(season))

    if set(old_json["assist_filter"]) != set(new_json["assist_filter"]):
        print("{} : 조력자 필터가 변경되었습니다.".format(season))
        print(set(old_json["assist_filter"]))
        print(set(new_json["assist_filter"]))


print("End")