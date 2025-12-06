from selenium import webdriver
from selenium.webdriver.common.by import By
from deep_translator import GoogleTranslator
import csv, time


driver = webdriver.Chrome()
base_url = "https://quotes.toscrape.com/page/{}/"

translator = GoogleTranslator(source="en", target="ja")

with open("quotes_selenium.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow([
        "text_en", "text_ja",
        "author_en", "author_ja",
        "tags"
    ])
    
    for page in range(1, 11):
        url = base_url.format(page)
        driver.get(url)
        
        time.sleep(1)
        
        quotes = driver.find_elements(By.CLASS_NAME, "quote")
        
        for q in quotes:
            text_en = q.find_element(By.CLASS_NAME, "text").text
            author_en = q.find_element(By.CLASS_NAME, "author").text
            tags = [tag.text for tag in q.find_elements(By.CLASS_NAME, "tag")]
            tags_str =", ".join(tags)
            
            # 翻訳処理
            try:
                text_ja = translator.translate(text_en)
            except:
                text_ja = "翻訳エラー"
                
            try:
                author_ja = translator.translate(author_en)
            except:
                author_ja = "翻訳エラー"
                
            writer.writerow([
                text_en, text_ja,
                author_en, author_ja,
                tags_str
            ])
        
        print(f"Page {page} scraped")
        
driver.quit()
print("CSV 保存完了！")