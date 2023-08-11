import json

with open('result/S47.json', encoding='utf-8') as f:
    old_json = json.load(f)

partys = old_json["partys"]
for party in partys:
    for i in party["partys"]:
        i["strikers"] = list(map(lambda x: {
            "name": x,
            "star": 99,
            "assist": False
        }, i["strikers"]))
        i["specials"] = list(map(lambda x: {
            "name": x,
            "star": 99,
            "assist": False
        }, i["specials"]))

old_json["partys"] = partys

# JSON 저장
with open("result_detail/S47.json", "w", encoding='utf-8') as f:
    json.dump(old_json, f, indent=2, ensure_ascii=False)