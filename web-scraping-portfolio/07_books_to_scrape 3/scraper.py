import requests, csv, json, time, openpyxl
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from deep_translator import GoogleTranslator

BASE_URL = "http://books.toscrape.com/"

translator = GoogleTranslator(source="auto", target="ja")

# 評価を星の数に変換
RATING_MAP = {
    "One": "★☆☆☆☆",
    "Two": "★★☆☆☆",
    "Three": "★★★☆☆",
    "Four": "★★★★☆",
    "Five": "★★★★★"
}

# ポンド → 日本円
def gbp_to_jpy(price_str):
    gbp_rate = 185
    price_float = float(price_str.replace("£", ""))
    return int(price_float * gbp_rate)

def scrape_page(url):
    # 1ページ分をスクレイピングしてデータを返す
    res = requests.get(url, timeout=10)
    res.encoding = "utf-8-sig"
    soup = BeautifulSoup(res.text, "html.parser")
    
    books = soup.select(".product_pod")
    data = []
    
    for b in books:
        title = b.h3.a["title"]
        price = b.select_one(".price_color").text
        rating = RATING_MAP.get(b.p["class"][1], "不明")
        
        detail_url = urljoin(BASE_URL, b.h3.a["href"])
        
        # 日本語翻訳
        jp_title = translator.translate(title)
        
        # 日本円換算
        price_jpy = gbp_to_jpy(price)
        
        data.append({
            "title": title,
            "日本語タイトル": jp_title,
            "price": price,
            "日本円": price_jpy,
            "評価（星）": rating,
            "detail_url": detail_url
        })
                
    return data

def main():
    page = 1
    max_pages = 5
    all_data = []
    
    while page <= max_pages:
        url = f"{BASE_URL}catalogue/page-{page}.html"
        print(f"{page} ページをスクレイピング中 ...")
        
        res = requests.get(url)
        if res.status_code == 404:
            print("ページが存在しません。終了します。")
            break
        
        page_data = scrape_page(url)
        all_data.extend(page_data)
        
        time.sleep(1) # サーバーへの負荷対策
        page += 1
        
    # CSV 出力
    with open("books_all.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["title", "日本語タイトル", "price", 
                         "日本円", "評価（星）", "detail_url"])
        
        for d in all_data:
            writer.writerow([
                d["title"],
                d["日本語タイトル"],
                d["price"],
                d["日本円"],
                d["評価（星）"],
                d["detail_url"]
            ])
        
    # JSON 出力    
    with open("books_output.json", "w", encoding="utf-8-sig") as jf:
        json.dump(all_data, jf, ensure_ascii=False, indent=2)
        
    # Excel 出力
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["title", "日本語タイトル", "price", 
               "日本円", "評価（星）", "detail_url"])
    
    for d in all_data:
        ws.append([
            d["title"],
            d["日本語タイトル"],
            d["price"],
            d["日本円"],
            d["評価（星）"],
            d["detail_url"]
        ])
        
        wb.save("books_output.xlsx")  
    print("CSV / JSON / Excel 保存完了!")
    
if __name__ == "__main__":
    main()