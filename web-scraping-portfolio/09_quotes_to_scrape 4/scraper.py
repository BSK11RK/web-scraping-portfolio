import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
from deep_translator import GoogleTranslator

BASE_URL = "https://quotes.toscrape.com/"

def get_soup(url):
    res = requests.get(url)
    res.raise_for_status()
    return BeautifulSoup(res.text, "html.parser")

def scrape_quotes():
    soup = get_soup(BASE_URL)
    quotes_data = []

    for quote_box in soup.select(".quote"):
        text = quote_box.select_one(".text").get_text(strip=True)
        author = quote_box.select_one(".author").get_text(strip=True)

        # 英語 → 日本語翻訳
        jp_text = GoogleTranslator(source='en', target='ja').translate(text)
        jp_text = jp_text.replace("。", "。\n")

        quotes_data.append({
            "quote_en": text,
            "quote_ja": jp_text,
            "author": author
        })

    return quotes_data

def save_data(data):
    df = pd.DataFrame(data)

    # CSV保存
    df.to_csv("quotes_translated.csv", index=False, encoding="utf-8-sig", lineterminator="\n")

    # Excel保存
    df.to_excel("quotes_translated.xlsx", index=False)

    # JSON保存
    df.to_json("quotes_translated.json", orient="records", force_ascii=False, indent=4)

def main():
    print("スクレイピング開始...")
    data = scrape_quotes()
    save_data(data)
    print(f"スクレイピング終了！{len(data)}件取得")

if __name__ == "__main__":
    main()
