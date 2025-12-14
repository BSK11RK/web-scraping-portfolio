import feedparser, pandas as pd
from deep_translator import GoogleTranslator

KEYWORDS = ["AI", "Python", "DX"]

translator = GoogleTranslator(source="auto", target="ja")
rows = []

for keyword in KEYWORDS:
    url = f"https://news.google.com/rss/search?q={keyword}&hl=ja&gl=JP&ceid=JP:ja"
    
    feed = feedparser.parse(
        url,
        request_headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
    )
    
    print(f"[{keyword}] 取得件数:", len(feed.entries))
    
    for entry in feed.entries[:10]:
        title_en = entry.title
        title_ja = translator.translate(title_en)
        
        rows.append({
            "キーワード": keyword,
            "title_en": title_en,
            "タイトル": title_ja,
            "公開日時": entry.get("published", ""),
            "リンク": entry.link,
            "タイトル取得数": len(title_en)       
            })
        
df = pd.DataFrame(rows)


# 統計情報
status = {
    "総記事数": len(df),
    "平均タイトル文字数": round(df["タイトル取得数"].mean(), 2),
    "最大タイトル文字数": df["タイトル取得数"].max(),
}

print("\n統計情報")
for k, v in status.items():
    print(f"{k}: {v}")
    
# 保存 
df.drop(columns=["タイトル取得数"], inplace=True)

df.to_csv("news_multi.csv", index=False, encoding="utf-8-sig")
df.to_json("news_multi.json", force_ascii=False, indent=2)
df.to_excel("news_multi.xlsx", index=False)


print("\n複数キーワードニュース保存完了")