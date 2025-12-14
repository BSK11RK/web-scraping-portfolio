import requests, pandas as pd

KEYWORD = "AI" 
API_URL = "https://kokkai.ndl.go.jp/api/speech"

params = {
    "any": KEYWORD,
    "maximumRecords": 20,
    "recordPacking": "json"
}

res = requests.get(API_URL, params=params)
data = res.json()

rows = []

for item in data["speechRecord"]:
    rows.append({
        "会議名": item.get("nameOfMeeting"),
        "発言者": item.get("speaker"),
        "発言内容": item.get("speech"),
        "発言日": item.get("data"),
        "発言URL": item.get("speechURL")
    })
    
df = pd.DataFrame(rows)

# 統計
stats = {
    "総発言数": len(df),
    "発言者数": df["発言者"].nunique()
}

print("統計情報")
for k, v in stats.items():
    print(f"{k}: {v}")

# 保存
df.to_csv("diet_minutes.csv", index=False, encoding="utf-8-sig")
df.to_json("diet_minutes.json", force_ascii=False, indent=2)
df.to_excel("diet_minutes.xlsx", index=False)

print("\n国会会議録データ 保存完了")