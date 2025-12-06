import requests, csv
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

url = "http://books.toscrape.com/"
res = requests.get(url)
soup = BeautifulSoup(res.text, "html.parser")

books = soup.select(".product_pod")

exchange_rate = 180  # 1 GBP = 180 JPY（

# 英語の評価クラスを日本の星評価にマップ
rating_map = {
    "One": "★☆☆☆☆",
    "Two": "★★☆☆☆",
    "Three": "★★★☆☆",
    "Four": "★★★★☆",
    "Five": "★★★★★"
}

with open("books.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow([
        "title_en / 英語タイトル",
        "title_ja / 日本語タイトル",
        "price / 価格(£)",
        "price_jpy / 価格（円）",
        "rating_jp / 評価（星）"
    ])
    
    for book in books:
        title_en = book.h3.a["title"]
        
        # 翻訳
        try:
            title_ja = GoogleTranslator(source="en", target="ja").translate(title_en)
        except Exception:
            title_ja = "翻訳エラー"
        
        price_text = (
            book.select_one(".price_color").text
            .strip()
            .replace("Â", "")
            .replace("£", "")
        )
        price = float(price_text)
        
        # 英語クラス名を取得して日本の星評価に変換
        rating_class = book.p["class"][1]
        rating_jp = rating_map.get(rating_class, "不明")
        
        price_jpy = round(price * exchange_rate)
        
        writer.writerow([
            title_en,
            title_ja,
            f"£{price:.2f}",
            f"¥{price_jpy}",
            rating_jp
        ])
        
print("CSV 保存完了！")
