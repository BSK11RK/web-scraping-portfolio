import requests, argparse, sys, matplotlib
import pandas as pd
import matplotlib.pyplot as plt

def get_weather_data(lat, lon, timezone="Asia/Tokyo"):
    # Open-Meteo API から気象データを取得して DataFrame で返す

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": [
            "temperature_2m", 
            "relative_humidity_2m", 
            "windspeed_10m"
        ],
        "timezone": timezone,
    }

    try:
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"APIリクエストエラー: {e}")
        sys.exit(1)

    data = res.json()

    if "hourly" not in data:
        print("APIレスポンスに 'hourly' がありません。レスポンス:", data)
        sys.exit(1)
        
    hourly = data["hourly"]

    df = pd.DataFrame({
        "時刻": hourly["time"],
        "気温(℃)": hourly["temperature_2m"],
        "湿度(%)": hourly["relative_humidity_2m"],
        "風速(m/s)": hourly["windspeed_10m"]
    })

    return df

def save_graph(df, filename="temperature_plot.png"):
    matplotlib.rcParams["font.family"] = "MS Gothic"
    matplotlib.rcParams["axes.unicode_minus"] = False
    
    # 気温の折れ線グラフを保存
    
    plt.figure(figsize=(10, 4))
    plt.plot(df["時刻"], df["気温(℃)"], color="red")
    plt.title("気温(℃)の推移")
    plt.xlabel("時刻")
    plt.ylabel("°C")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(filename)
    print(f"気温グラフを保存しました: {filename}")

    
def show_stats(df):
    # 統計量を表示
    
    print("\n=== 気温の統計情報（℃） ===")
    print(f"平均気温: {df['気温(℃)'].mean():.2f} ℃")
    print(f"最高気温: {df['気温(℃)'].max():.2f} ℃")
    print(f"最低気温: {df['気温(℃)'].min():.2f} ℃")

def main():
    parser = argparse.ArgumentParser(description="天気データ取得ツール")
    parser.add_argument("--lat", type=float, default=35.6812, help="緯度") # 東京駅(仮)
    parser.add_argument("--lon", type=float, default=139.7671, help="経度")
    args = parser.parse_args()

    print(f"天気データ取得中...（緯度: {args.lat}, 経度: {args.lon}）")
    
    # CLI 引数で取得した座標を使用
    df = get_weather_data(args.lat, args.lon)

    # 統計量の表示
    show_stats(df)
    
    # CSV 保存
    output_csv = "weather_output.csv"
    df.to_csv(output_csv, index=False, encoding="utf-8-sig")
    print(f"CSV 保存完了: {output_csv}")
    
    # グラフの保存
    save_graph(df)

if __name__ == "__main__":
    main()
