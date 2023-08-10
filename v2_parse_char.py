import requests
import json

res = requests.get("https://raw.githubusercontent.com/lonqie/SchaleDB/main/data/kr/students.json")

res_json = res.json()

result = {}
for e in res_json:
    id = e["Id"]
    name = e["Name"]
    result[id] = name

# JSON 저장
with open("character.json", "w", encoding='utf-8') as f:
    json.dump(result, f, indent=2, ensure_ascii=False)