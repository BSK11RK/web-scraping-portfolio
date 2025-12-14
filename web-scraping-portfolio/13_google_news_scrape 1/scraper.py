import feedparser
import pandas as pd
from deep_translator import GoogleTranslator

KEYWORD = "AI"
URL = f"https://news.google.com/rss/search?q={KEYWORD}&hl=ja&gl=JP&ceid=JP:ja"

feed = feedparser.parse(
    URL,
    request_headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
)

print("取得件数:", len(feed.entries)) 

rows = []
translator = GoogleTranslator(source="auto", target="ja")

for entry in feed.entries[:10]:
    rows.append({
        "title_en": entry.title,
        "タイトル": translator.translate(entry.title),
        "公開日時": entry.get("published", ""),
        "リンク": entry.link
    })

df = pd.DataFrame(rows)

df.to_csv("news.csv", index=False, encoding="utf-8-sig")
df.to_json("news.json", force_ascii=False, indent=2)
df.to_excel("news.xlsx", index=False)

print("✅ Googleニュース保存完了")