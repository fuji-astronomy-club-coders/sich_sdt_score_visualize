import numpy as np
import cv2

# ダミーデータ作成用
# 画像サイズを実際の動画と同じように設定
height = 1104
width = 1608

# フレーム数を動作確認用として10frameに設定
n_frames = 10

# 1~100の間のランダム差値データを格納する3次元配列を作成
dummy_data = np.random.uniform(
    low=1,
    high=100,
    size=(n_frames,height,width)
)
# print(dummy_data)

# カラーマップ作成用
def create_colormap():
    # 256要素を持つLUTを作成(偏差値0~100に対応する色を設定)
    lut = np.zeros((256,1,3),dtype=np.uint8)

    # 偏差値50未満は濃い青から白へ段階的に変化
    lut[0:5] = [100,0,0]
    lut[5:10] = [115,25,25]
    lut[10:15] = [130,50,50]
    lut[15:20] = [145,75,75]
    lut[20:25] = [160,100,100]
    lut[25:30] = [175,125,125]
    lut[30:35] = [190,150,150]
    lut[35:40] = [205,175,175]
    lut[40:45] = [220,200,200]
    lut[45:50] = [235,225,225]
    # 偏差値50以上は白から濃い赤へ段階的に変化
    lut[50:55] = [255,255,255]
    lut[55:60] = [225,225,240]
    lut[60:65] = [195,195,225]
    lut[65:70] = [165,165,210]
    lut[70:75] = [135,135,195]
    lut[75:80] = [105,105,180]
    lut[80:85] = [75,75,165]
    lut[85:90] = [45,45,150]
    lut[90:95] = [15,15,135]
    lut[95:256] = [0,0,120]
    return lut

colormap_lut = create_colormap()

# LUTの色を確認するためのカラーバー作成用(必要に応じて使用)
#line = np.linspace(0, 100, width, dtype=np.uint8)
# 高さ50ピクセルに設定
#colorbar = np.tile(line, (50, 1))
# グレースケール→BGR
#colorbar_bgr = cv2.cvtColor(colorbar, cv2.COLOR_GRAY2BGR)
# LUT適用
#colorbar_result = cv2.LUT(colorbar_bgr, colormap_lut)
# 保存
#cv2.imwrite(r"C:\Users\2025005585\Desktop\python\colorbar.png", colorbar_result)

# 動画作成用
# 出力動画の設定
video_writer = cv2.VideoWriter(
    r"C:\Users\2025005585\Desktop\python\output_test2.mp4",
    cv2.VideoWriter_fourcc(*'mp4v'),
    30.0,
    (width, height)
)

# 1フレームずつ取り出し、LUTを適用して動画に書き込む
for i in range(n_frames):
    frame = dummy_data[i]
    # 偏差値を0〜100に収めてuint8 型に変換
    clipped_frame = np.clip(frame, 0, 100).astype(np.uint8)
    # LUTを適用するため、グレースケール画像を3チャンネル(BGR)画像へ変換
    three_channel_frame = cv2.cvtColor(clipped_frame,cv2.COLOR_GRAY2BGR)
    # LUTを適用し、偏差値を対応する色へ変換
    color_mapped_frame = cv2.LUT(three_channel_frame, colormap_lut)
    # 動画ファイルに1フレーム書き込む
    video_writer.write(color_mapped_frame)

video_writer.release()
print("動画の作成が完了しました")
