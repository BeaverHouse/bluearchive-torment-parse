import requests
import os
import win11toast
from sys import platform

baseURL = "https://storage.googleapis.com/info.herdatasam.me"
types = ["폭발", "관통", "신비"]

def get_csv(category: str, type: str, season: int):
    os.makedirs("rawdetail", exist_ok=True)

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
        if res.ok:
            f.write(res.content)
            # 로컬 알림용, 주석처리해도 무방
            if platform == "win32":
                win11toast.toast(f"정보가 업데이트되었습니다: {category}, {type}, S{season}")


if __name__ == "__main__":
    category: str   = "총력전"
    type: str       = "관통"
    season: int     = 59            # 총력전
    # season: int     = 3            # 대결전
    
    get_csv(category=category, type=type, season=season)