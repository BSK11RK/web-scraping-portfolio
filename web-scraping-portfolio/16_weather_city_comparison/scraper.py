import requests, pandas as pd
import matplotlib.pyplot as plt
from datetime import date, timedelta

# 日本語フォント
plt.rcParams["font.family"] = "Meiryo"

# 都市
cities = {
    "Tokyo": (35.6895, 139.6917),
    "Osaka": (34.6937, 135.5023),
    "Sapporo": (43.0618, 141.3545),
    "London": (51.5074, -0.1278),
    "Paris": (48.8566, 2.3522),
    "Berlin": (52.52, 13.405),
    "New York": (40.7128, -74.0060),
    "Los Angeles": (34.0522, -118.2437),
    "Seoul": (37.5665, 126.9780),
    "Singapore": (1.3521, 103.8198),
}

end = date.today()
start = end - timedelta(days=7)

rows = []

for city, (lat, lon) in cities.items():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_mean",
        "current_weather": "true",
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "timezone": "auto"
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    daily_temps = data["daily"]["temperature_2m_mean"]
    avg_temp = round(sum(daily_temps) / len(daily_temps), 1)
    current_temp = data["current_weather"]["temperature"]

    rows.append({
        "都市": city,
        "現在気温（℃）": current_temp,
        "直近7日平均気温（℃）": avg_temp
    })

df = pd.DataFrame(rows)

# 保存
df.to_csv("city_temperature.csv", index=False, encoding="utf-8-sig")
df.to_json("city_temperature.json", force_ascii=False, indent=2)
df.to_excel("city_temperature.xlsx", index=False)

# グラフ 
plt.figure(figsize=(10, 5))
plt.bar(df["都市"], df["直近7日平均気温（℃）"])
plt.title("都市別 平均気温比較（直近7日）")
plt.xlabel("都市")
plt.ylabel("平均気温（℃）")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("city_temperature.png")
plt.show()

print("CSV / JSON / Excel / グラフ 保存完了")