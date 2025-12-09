from playwright.sync_api import sync_playwright
import openpyxl, json

BASE_URL = "http://quotes.toscrape.com/js/"

def scrape_playwright():
    data = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(BASE_URL)
        
        quotes = page.locator(".quote")
        for i in range(quotes.count()):
            q = quotes.nth(i)
            text = q.locator(".text").inner_text()
            author = q.locator(".author").inner_text()
            data.append({"text": text, "author": author})
            
        browser.close()
    return data

def save_files(data):
    # JSON
    with open("quotes.json", "w", encoding="utf-8-sig") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    # Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["text", "author"])
    for d in data:
        ws.append([d["text"], d["author"]])
    wb.save("quotes.xlsx")
    print("JSON / Excel 保存完了")
    
if __name__ == "__main__":
    data = scrape_playwright()
    save_files(data)