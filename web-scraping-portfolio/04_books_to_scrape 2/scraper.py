import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import pandas as pd

url = "http://books.toscrape.com/"
res = requests.get(url)
soup = BeautifulSoup(res.text, "html.parser")
books = soup.select(".product_pod")

exchange_rate = 180  # 1 GBP = 180 JPY

rating_map = {
    "One": "★☆☆☆☆",
    "Two": "★★☆☆☆",
    "Three": "★★★☆☆",
    "Four": "★★★★☆",
    "Five": "★★★★★"
}

data_list = []

for book in books:
    title_en = book.h3.a["title"]
    
    # 翻訳
    try:
        title_ja = GoogleTranslator(source="en", target="ja").translate(title_en)
    except Exception:
        title_ja = "翻訳エラー"
    
    price_text = book.select_one(".price_color").text.strip().replace("Â", "").replace("£", "")
    price = float(price_text)
    
    rating_class = book.p["class"][1]
    rating_jp = rating_map.get(rating_class, "不明")
    price_jpy = round(price * exchange_rate)
    
    data_list.append({
        "title_en / 英語タイトル": title_en,
        "title_ja / 日本語タイトル": title_ja,
        "price / 価格(£)": f"£{price:.2f}",
        "price_jpy / 価格（円）": f"¥{price_jpy}",
        "rating_jp / 評価（星）": rating_jp
    })

df = pd.DataFrame(data_list)

# CSV保存
df.to_csv("books.csv", index=False, encoding="utf-8-sig")

# JSON保存
df.to_json("books.json", orient="records", force_ascii=False)

# Excel保存（文字化け防止）
df.to_excel("books.xlsx", index=False, engine="openpyxl")

print("CSV / JSON / Excel 保存完了！")
