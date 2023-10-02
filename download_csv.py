import requests
import os

baseURL = "https://storage.googleapis.com/info.herdatasam.me"
types = ["폭발", "관통", "신비"]

def get_csv(category: str, type: str, season: int):
    os.makedirs("rawdetail", exist_ok=True)

    print(category, type, season)

    url, file_name = "", ""
    if category == "총력전":
        url = f"{baseURL}/BlueArchiveJP/RaidRankData/S{season}/TeamDataDetail_Original.csv"
        file_name = f"S{season}D.csv"
    else:
        type_idx = types.index(type)+1
        file_name = f"3S{season}-TD.csv"
        url = f"{baseURL}/BlueArchiveJP/RaidRankDataER/S{season}/TeamDataDetailBoss{type_idx}_Original.csv"
    
    with open(f"rawdetail/{file_name}", "wb") as f:
        res = requests.get(url)
        f.write(res.content)


if __name__ == "__main__":
    category = input("총력전 / 대결전 : ")
    if category == "대결전":
        type = input("토먼트 속성 : ")
    season = int(input("시즌 숫자 : "))
    
    get_csv(category=category, type=type, season=season)