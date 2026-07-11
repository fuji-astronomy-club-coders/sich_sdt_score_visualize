import os, cv2, numpy as np, tqdm

def extract_sun_mini(folder, size):
    # 画像ファイルのみ1000枚取得
    files = [f for f in sorted(os.listdir(folder)) if f.lower().endswith(('.png', '.jpg', '.jpeg'))][:1000]
    frames = []
    
    for f in tqdm.tqdm(files):
        img = cv2.imread(os.path.join(folder, f), cv2.IMREAD_GRAYSCALE)
        if img is None: continue
        
        # 太陽の重心(cx, cy)を計算
        M = cv2.moments(cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)[1])
        if M["m00"] == 0: continue
        cx, cy = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
        
        # 切り抜き（画面端のガード付き）
        h, w = img.shape
        y1, y2, x1, x2 = max(0, cy-size//2), min(h, cy+size//2), max(0, cx-size//2), min(w, cx+size//2)
        frames.append(img[y1:y2, x1:x2])
        
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