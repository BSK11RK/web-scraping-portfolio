import requests, time
from bs4 import BeautifulSoup
import pandas as pd
from deep_translator import GoogleTranslator
from datetime import datetime

# GitHub トレンド URL
URL = "https://github.com/trending"

def translate_ja(text):
    try:
        return GoogleTranslator(source="auto", target="ja").translate(text)
    except:
        return text # 翻訳失敗時は英語のまま返す
    
def scrape_github_trending():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    res = requests.get(URL, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    
    repo_list = soup.select("article.Box-row")
    
    data = []
    
    for repo in repo_list:
        title = repo.h2.text.strip().replace("\n", "").replace(" ", "")
        repo_url = "https://github.com/" + title
        
        description = repo.p.text.strip() if repo.p else "No description"
        lang = repo.find("span", itemprop="programmingLanguage")
        language = lang.text.strip() if lang else "N/A"
        
        stars = repo.select_one("a.Link--muted[href$='/stargazers']")
        stars = stars.text.strip().replace(",", "") if stars else "0"
        
        # 日本語翻訳
        description_ja = translate_ja(description)
        
        data.append({
            "repository": title,
            "language": language,
            "stars": int(stars),
            "description_en": description,
            "description_ja": description_ja,
            "url": repo_url
        })
        
        return pd.DataFrame(data)
    
# 実行
df = scrape_github_trending()

# 統計情報
avg_stars = df["stars"].mean()
max_stars = df["stars"].max()
top_repo = df.loc[df["stars"].idxmax(), "repository"]

print("▼ GitHubトレンド 統計情報")
print(f"平均スター数: {avg_stars:.2f}")
print(f"最大スター数: {max_stars}")
print(f"最も人気のリポジトリ: {top_repo}")

# 保存
today = datetime.now().strftime("%Y%m%d")

df.to_csv(f"Github_Trending_{today}.csv", index=False, encoding="utf-8-sig")
df.to_json(f"Github_Trending_{today}.json", orient="records", indent=2, force_ascii=False)
df.to_excel(f"Github_Trending_{today}.xlsx", index=False)

print("\nCSV / JSON / Excel: 保存完了!")