#ダミーデータだよ。
import numpy as np
import matplotlib.pyplot as plt

from std_score_visualize import extract_sun_mini
from std_score_visualize import calculate_hensachi

#log用のやつ
from datetime import datetime, timezone, timedelta
JST = timezone(timedelta(hours=9))
now_jst = datetime.now(JST)

print(now_jst.isoformat(timespec="milliseconds"))

# ファイルの上のほうに追加！
INPUT_DIR = r"J:\Observe-Data\2025-08-30\2025-08-30pic-PL\2025-08-30-0448_4-CapObj"  # 入力フォルダのパス
CROP_H = 800             # 切り取る高さ（数値）
CROP_W = 800             # 切り取る幅（数値）

#強調するフレーム
emphasis=[(8,9),(708,709)]

# 見たいピクセル座標
y = 400
x = 400
# ダミーの偏差値画像（10フレーム、5×5ピクセル）
#hensachi = np.random.normal(
#    loc=50,      # 平均50
#    scale=10,    # 標準偏差10
#   size=(10, 5, 5)
#)

#y = 2
#x = 3

#pixel_values = hensachi[:, y, x]

#print(pixel_values)

#pixel_values = hensachi[:, y, x]

# フレーム番号
#frames = np.arange(len(pixel_values))

# グラフ作成
#plt.figure(figsize=(10, 4))
#plt.plot(frames, pixel_values, marker="o")
#plt.xlabel("Frame")
#plt.ylabel("Hensachi")
#plt.title(f"Hensachi of Pixel ({x}, {y})")
#plt.grid(True)
#plt.savefig("pixel_graph.png", dpi=300)
#plt.show()


#本データだよ。

print(f"\n--- 画像ファイルの読み込み開始: {INPUT_DIR} ---")
frames, centers = extract_sun_mini(
    INPUT_DIR,
    h_size=CROP_H,
    w_size=CROP_W
)

mean, std, hensachi = calculate_hensachi(frames)



# 全フレームのそのピクセルの偏差値を取り出す
pixel_values = hensachi[:, y, x]

# フレーム番号
frames = np.arange(len(pixel_values))

# グラフ作成

plt.figure(figsize=(11, 4))

plt.minorticks_on()
plt.xticks(np.arange(0, len(frames), 100))
plt.yticks(np.arange(0, 100, 10))

plt.plot(frames, pixel_values, marker="o",markersize=0,markerfacecolor="#ec468a")

for emp in emphasis:
    plt.axvspan(emp[0]-0.5, emp[1]+0.5, color='orange', alpha=0.3, label='Highlight Area')

plt.xlabel("Frames")
plt.ylabel("Standardized test score (deviation score)")
plt.title(f"Trend of the deviation value for the specified pixel (x={x}, y={y})")
plt.grid(True)

plt.tight_layout()
plt.savefig(f"pixel_graph_x{x}_y{y}.png", dpi=300)

plt.close()