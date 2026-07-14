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
hensachi=50+10*(frames-mean)/std
print("偏差値画像")
print(hensachi)
#偏差値画像を1枚ずつ表示する。
for i in range(len(hensachi)):
    print(f"{i+1}枚目の偏差値画像")
    print(hensachi[i])