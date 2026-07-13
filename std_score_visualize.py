#平均を計算
mean=np.mean(frames,axis=0)
print("平均画像の画素値")
print(mean)
#標準偏差を計算
std=np.std(frames,axis=0)
print("標準偏差画像")
print(std)
#偏差値を計算
# 標準偏差が0の画素は、0で割ることを防ぐため50を代入する
hensachi = np.where(
    std == 0,
    50,
    50 + 10 * (frames - mean) / std
)
print("偏差値画像")
print(hensachi)
#偏差値画像を1枚ずつ表示する。
for i in range(len(hensachi)):
    print(f"{i+1}枚目の偏差値画像")
    print(hensachi[i])

#以下、ダミーデータ
#NumPy使います！の宣言
import numpy as np
#3枚のダミー画像を作る。
frames=np.array([
    [[100,110],
    [120,130]],
    
    [[102,111],
    [119,131]],
    
    [[101,109],
    [121,132]]
])
#念のため確認
print("元データ")
print(frames)
#平均を求める
mean=np.mean(frames,axis=0)
print("平均画像の画素値")
print(mean)
#axis=0は、フレーム方向(時間方向)に平均を取る！
#標準偏差を求める。
std=np.std(frames,axis=0)
print("標準偏差画像")
print(std)
#各ピクセルについて、全フレームの平均・標準偏差から偏差値を計算する。
# 標準偏差が0の画素は、0で割ることを防ぐため50を代入する
hensachi = np.where(
    std == 0,
    50,
    50 + 10 * (frames - mean) / std
)
print("偏差値画像")
print(hensachi)
#偏差値画像を1枚ずつ表示する。
for i in range(len(hensachi)):
    print(f"{i+1}枚目の偏差値画像")
    print(hensachi[i])
