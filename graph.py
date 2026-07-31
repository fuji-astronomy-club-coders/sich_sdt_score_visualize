#ダミーデータだよ。
import numpy as np
import matplotlib.pyplot as plt

from std_score_visualize import extract_sun_mini
from std_score_visualize import calculate_hensachi

# ファイルの上のほうに追加！
r"""memo:実行するパス
[ ] - r"J:\Observe-Data\2025-07-20\2025-07-20pic-LT",
[ ] - r"J:\Observe-Data\2025-07-20\2025-07-20pic-PL",
[ ] - r"J:\Observe-Data\2025-08-30\2025-08-30pic-LT",
[ ] - r"J:\Observe-Data\2025-08-30\2025-08-30pic-PL",
[ ] - r"J:\Observe-Data\2026-01-17\2026-1-17pic-LT",
[ ] - r"J:\Observe-Data\2026-01-17\2026-1-17pic-PL",
"""
INPUT_DIR = r"J:\2025-08-30\2025-08-30pic-LT2"  # 入力フォルダのパス
CROP_H = 800             # 切り取る高さ（数値）
CROP_W = 800             # 切り取る幅（数値）

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

# 見たいピクセル座標
y = 350
x = 420

# 全フレームのそのピクセルの偏差値を取り出す
pixel_values = hensachi[:, y, x]

# フレーム番号
frames = np.arange(len(pixel_values))

# グラフ作成
plt.figure(figsize=(10, 4))
plt.plot(frames, pixel_values, marker="o")
plt.xlabel("Frame")
plt.ylabel("Hensachi")
plt.title(f"Hensachi of Pixel ({x}, {y})")
plt.grid(True)
plt.savefig("pixel_graph.png", dpi=300)
plt.show()