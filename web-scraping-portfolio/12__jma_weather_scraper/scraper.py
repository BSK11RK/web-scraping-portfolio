from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options # headless
import time
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

options = Options()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
driver.get("https://www.data.jma.go.jp/risk/obsdl/index.php")
driver.implicitly_wait(3)

time.sleep(1)

# 「東京」の「東京」をクリック
btn_tokyo_1 = driver.find_element(By.ID, "pr44")
btn_tokyo_1.click()
btn_tokyo_2 = driver.find_element(By.CSS_SELECTOR, "#stationMap > div:nth-child(11)")
btn_tokyo_2.click()

# 「項目を選ぶ」をクリック
btn_element = driver.find_element(By.ID, "elementButton") # ある要素が表示されるまで待機
btn_element.click()

# 「日別値」-「日平均気温」をクリック
radio_by_day = driver.find_element(By.CSS_SELECTOR, "#aggrgPeriod_1")
radio_by_day.click()
radio_temp = driver.find_element(By.ID, "平均気温")
radio_temp.click()

# 「期間を選ぶ」をクリック
btn_period = driver.find_element(By.ID, "periodButton")
btn_period.click()

# 開始の年月日
pull_down_ini_y = driver.find_element(By.NAME, "iniy")
Select(pull_down_ini_y).select_by_visible_text("2025")

pull_down_ini_m = driver.find_element(By.NAME, "inim")
Select(pull_down_ini_m).select_by_visible_text("1")

pull_down_ini_d = driver.find_element(By.NAME, "inid")
Select(pull_down_ini_d).select_by_visible_text("1")

# 終了の年月日
pull_down_end_y = driver.find_element(By.NAME, "endy")
Select(pull_down_end_y).select_by_visible_text("2025")

pull_down_end_m = driver.find_element(By.NAME, "endm")
Select(pull_down_end_m).select_by_visible_text("1")

pull_down_end_d = driver.find_element(By.NAME, "endd")
Select(pull_down_end_d).select_by_visible_text("31")


# 「画面に表示」をクリック
btn_display = driver.find_element(By.CSS_SELECTOR, "#loadTable > img")
btn_display.click()

table_left = driver.find_element(By.CLASS_NAME, "grid-canvas-left")
table_right = driver.find_element(By.CLASS_NAME, "grid-canvas-right")

dates = table_left.find_elements(By.CLASS_NAME, "slick-cell")
temps = table_right.find_elements(By.CLASS_NAME, "slick-cell")

for d, t in zip(dates, temps):
    print(f"{d.text} : {t.text}度")

# データの取得
history = driver.find_element(By.ID, "oshirase")
HTML = history.get_attribute("innerHTML")
print(f"HTML : {HTML}")

# --------------------------------------------------

# DataFrame に変換
date_list = [d.text for d in dates]
temp_list = [float(t.text) for t in temps]

df = pd.DataFrame({
    "日付": date_list,
    "平均気温(℃)": temp_list
})

print(df)

# 保存（CSV / JSON / Excel）
today = datetime.now().strftime("%Y%m%d")

csv_path = f"tokyo_temp_{today}.csv"
json_path = f"tokyo_temp_{today}.json"
excel_path = f"tokyo_temp_{today}.xlsx"

df.to_csv(csv_path, index=False, encoding="utf-8-sig")
df.to_json(json_path, orient="records", indent=2, force_ascii=False)
df.to_excel(excel_path, index=False)


print("\nCSV / JSON / Excel 保存完了！")

# 折れ線グラフ
plt.rcParams["font.family"] = "MS Gothic"  # Windows日本語フォント
plt.rcParams["axes.unicode_minus"] = False # マイナス符号の文字化け防止

plt.figure(figsize=(10, 5))
plt.plot(df["日付"], df["平均気温(℃)"])
plt.xticks(rotation=45)
plt.xlabel("日付")
plt.ylabel("平均気温(℃)")
plt.title("東京・日平均気温（気象庁データ）")
plt.tight_layout()
plt.savefig(f"tokyo_temp_graph_{today}.png")
plt.show()

print("折れ線グラフ 保存完了!")

time.sleep(2)
driver.quit()