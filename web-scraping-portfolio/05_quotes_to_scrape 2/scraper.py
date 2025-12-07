import requests, time
import pandas as pd
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

BASE_URL = "https://quotes.toscrape.com/page/{page}/"
MAX_PAGES = 10

def translate_text(en_text):
    try:
        # deep_translator は外部アクセスするためネット接続必須
        return GoogleTranslator(source="auto", target="ja").translate(en_text)
    except Exception:
        return en_text # 翻訳できなければ原文を返す

def scraper_quotes(max_pages=MAX_PAGES, delay=0.8):
    records = []
    for p in range(1, max_pages + 1):
        url = BASE_URL.format(page=p)
        print(f"[INFO] Fetching page {p}: {url}")    
        try:
            res = requests.get(url, timeout=10)
            res.raise_for_status()
        except Exception as e:
            print(f"[WARN] ページ取得失敗 (page {p}): {e}")
            break
        
        soup = BeautifulSoup(res.text, "html.parser")
        quotes = soup.select(".quote")
        if not quotes:
            print(f"[INFO] page {p} に quote 要素が見つかりません。終了します。")
            break
        
        for q in quotes:
            text = q.select_one(".text").get_text(strip=True)
            author = q.select_one(".author").get_text(strip=True)
            tags = [t.get_text(strip=True) for t in q.select(".tag")]
            tags_str = ", ".join(tags)
            
            # 翻訳（日本語）
            text_ja = translate_text(text)
            
            records.append({
                "quote_en": text,
                "quote_ja": text_ja,
                "author": author,
                "tags": tags_str
            })
            
        time.sleep(delay)
    return records

def save_all(records):
    df = pd.DataFrame(records)
    # CSV
    df.to_csv("quotes_05.csv", index=False, encoding="utf-8-sig")
    # JSON (整形)
    df.to_json("quotes_05.json", orient="records", force_ascii=False, indent=2)
    # Excel
    df.to_excel("quotes_05.xlsx", index=False, engine="openpyxl")
    print("CSV / JSON / Excel を保存しました")
    
def main():
    print("Start scraping quotes.toscrape.com")
    records = scraper_quotes()
    if not records:
        print("[WARN] 取得データが空です。処理を中止します。")
        return
    save_all(records)
    
    # 簡単な統計
    df = pd.DataFrame(records)
    print(f"[INFO] 記事数: {len(df)}")
    print("[INFO] 上位タグトップ10:")
    tag_series = df["tags"].str.split(", ").explode().value_counts().head(10)
    print(tag_series.to_string())
    
if __name__ == "__main__":
    main()