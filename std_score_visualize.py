        padded = cv2.copyMakeBorder(cropped,top,bottom,left,right,cv2.BORDER_CONSTANT,value = 0)

        frames.append(padded)

    return np.array(frames)

# --- 実行とCSV保存（1フレームずつピクセル保存） ---
if __name__ == "__main__":
    out_dir = "./output_pixels"
    os.makedirs(out_dir, exist_ok=True)
    
    # 実行（フォルダ名とサイズを指定）
    frames = extract_sun_mini("./sun_images", 200)
    
    # 1フレームごと、全ピクセルをCSVに保存
    for i, frame in enumerate(frames):
        np.savetxt(f"{out_dir}/frame_{i+1:03d}.csv", frame, delimiter=",", fmt="%d")

    #本番用の画像が1枚以上読み込めている場合のみ実行（空エラー防止用）
    if len(frames) > 0:  
        # 1ピクセルずつの個別アクセス（例：1枚目の座標x=10, y=20の明るさ）
        print(f"個別ピクセル明るさ: {frames[0, 20, 10]}")
#平均を計算
mean=np.mean(frames,axis=0)
print("平均画像の画素値")
print(mean)
#標準偏差を計算
std=np.std(frames,axis=0)
print("標準偏差画像")
#偏差値を計算
hensachi=50+10*(frames-mean)/std
print("偏差値画像")
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
hensachi=50+10*(frames-mean)/std
print("偏差値画像")
print(hensachi)
#偏差値画像を1枚ずつ表示する。
for i in range(len(hensachi)):
    print(f"{i+1}枚目の偏差値画像")
    print(hensachi[i])