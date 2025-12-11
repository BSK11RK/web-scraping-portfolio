import requests, time
from bs4 import BeautifulSoup
import pandas as pd
from deep_translator import GoogleTranslator

BASE_URL = "https://en.wikipedia.org"

# User-Agentを設定（これがないと Wikipedia は403になる） 
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def get_page(url):
    res = requests.get(url, headers=HEADERS)
    res.raise_for_status()
    return BeautifulSoup(res.text, "html.parser")

def translate_text(text):
    try:
        ja = GoogleTranslator(source="auto", target="ja").translate(text)
        return f"{text}\n{ja}"
    except:
        return text

def scrape_category(category_url):
    soup = get_page(category_url)

    articles = soup.select("#mw-pages li a")
    data = []

    for a in articles:
        title = a.text
        articles_url = BASE_URL + a.get("href")

        article_soup = get_page(articles_url)

        # 最初の段落を取得
        p = article_soup.select_one("p")
        summary_en = p.text.strip() if p else ""
        summary_translated = translate_text(summary_en)

        # 最終更新日時
        info = article_soup.select_one("#footer-info-lastmod")
        lastmod = info.text.strip() if info else ""

        data.append({
            "title": title,
            "summary_en_ja": summary_translated,
            "url": articles_url,       
            "last_modified": lastmod
        })

        time.sleep(1)

    return data

def save_all(data):
    df = pd.DataFrame(data)
    df.to_csv("wikipedia_category.csv", index=False, encoding="utf-8-sig")
    df.to_json("wikipedia_category.json", orient="records",
               indent=2, force_ascii=False)
    df.to_excel("wikipedia_category.xlsx", index=False)


def main():
    category_url = "https://en.wikipedia.org/wiki/Category:Python_(programming_language)"
    print("スクレイピング開始...")
    data = scrape_category(category_url)
    save_all(data)
    print("スクレイピング完了!")


if __name__ == "__main__":
    main()