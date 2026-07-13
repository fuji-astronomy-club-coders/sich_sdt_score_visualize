import os, cv2, numpy as np, tqdm
import cv2
import numpy as np
import os
import tqdm

def extract_sun_mini(folder, size):
    #もし指定されたフォルダは存在しなければ、エラーを出さずに空の配列を返す
    if not os.path.exists(folder):
        print("f:注意:フォルダ '{folder}'が見つからないため、本番処理をスキップしてダミーデータへ移行します。")
        return np.array([])
    
    # 画像ファイルのみ1000枚取得
    files = [f for f in sorted(os.listdir(folder)) if f.lower().endswith(('.png', '.jpg', '.jpeg'))][:1000]
    frames = []

@@ -14,11 +22,28 @@ def extract_sun_mini(folder, size):
        if M["m00"] == 0: continue    
            cx, cy = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
        
        # 切り抜き（画面端のガード付き）
        h, w = img.shape
        y1, y2, x1, x2 = max(0, cy-size//2), min(h, cy+size//2), max(0, cx-size//2), min(w, cx+size//2)
        frames.append(img[y1:y2, x1:x2])
        
        #切り抜きたい理想の範囲（画面外にはみ出す可能性あり）
        h,w = img.shape
        half = size//2
        y1,y2 =  cy - half, cy + half
        x1,x2 = cx - half,cx + half

        #画面外にはみ出している量（余白の計算）
        top =max(0,-y1)
        bottom =max(0,y2 - h)
        left = max(0,-x1)
        right =max(0,x2 - w)

        #画面内に収まる安全な範囲だけでまずは切りぬく
        crop_y1,crop_y2 = max(0,y1),min(h,y2)
        crop_x1,crop_x2 = max(0,x1),min(w,x2)
        cropped = img[crop_y1:crop_y2,crop_x1:crop_x2]

        #はみ出していた部分を黒色（0）で埋めて、常にsize x size　にする 
        padded = cv2.copyMakeBorder(cropped,top,bottom,left,right,cv2.BORDER_CONSTANT,value = 0)

        frames.append(padded)

    return np.array(frames)

# --- 実行とCSV保存（1フレームずつピクセル保存） ---

@@ -32,9 +57,11 @@ if __name__ == "__main__":
    # 1フレームごと、全ピクセルをCSVに保存
    for i, frame in enumerate(frames):
        np.savetxt(f"{out_dir}/frame_{i+1:03d}.csv", frame, delimiter=",", fmt="%d")
        
    # 1ピクセルずつの個別アクセス（例：1枚目の座標x=10, y=20の明るさ）
    print(f"個別ピクセル明るさ: {frames[0, 20, 10]}")

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