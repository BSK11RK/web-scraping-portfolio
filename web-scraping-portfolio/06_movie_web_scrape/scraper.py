import requests, pandas as pd

BASE_URL = BASE_URL = "https://scrapethissite.com/pages/ajax-javascript/?ajax=true&year="

all_data = []

for year in range(2010, 2017):
    url = BASE_URL + str(year)
    print(f"取得中: {url}")

    res = requests.get(url, timeout=10)
    res.raise_for_status()


    movies = res.json()

    for m in movies:
        all_data.append({
            "year": m.get("year"),
            "title": m.get("title"),
            "rating": m.get("rating"),
            "genre": m.get("genre"),
            "duration": m.get("duration"),
            "director": m.get("director"),
            "actors": ", ".join(m.get("actors", [])),
            "gross": m.get("gross"),
        })
    
    df = pd.DataFrame(all_data)
    
    # 保存
    df.to_csv("movies.csv", index=False, encoding="utf-8-sig")
    df.to_json("movies.json", orient="records", force_ascii=False, indent=2)
    df.to_excel("movies.xlsx", index=False, engine="openpyxl")
    
    print("CSV / JSON / Excel 保存完了！")