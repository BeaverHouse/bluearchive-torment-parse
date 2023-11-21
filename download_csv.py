import requests
import os
import win11toast
from v2_parse_detail_after50 import parse_main
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
    
    res = requests.get(url)
    if res.ok:
        with open(f"rawdetail/{file_name}", "wb") as f:
            f.write(res.content)

        parse_main()

        # 로컬 알림용, 주석처리해도 무방
        if platform == "win32":
            win11toast.toast(f"정보가 업데이트되었습니다: {category}, {type}, S{season}")


if __name__ == "__main__":
    # 대결전 중장갑 호드 23.11.15. ~ 23.11.22.
    category: str   = "대결전"
    type: str       = "관통"         
    # season: int     = 999            # 총력전
    season: int     = 4            # 대결전
    
    get_csv(category=category, type=type, season=season)