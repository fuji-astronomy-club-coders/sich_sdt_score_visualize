import cv2
import tqdm
import numpy as np
from pathlib import Path

from lib.MIN2ver2 import MIN2_ignore_sunspots
from lib.zip_operator import get_image_names_from_dir, load_image_from_path_cv2

# 関数
def create_colormap():
    # 256要素を持つLUTを作成(偏差値0~100に対応する色を設定)
    lut = np.zeros((256, 1, 3), dtype=np.uint8)
    # 偏差値50未満は濃い青から白へ段階的に変化
    lut[0:5] = [100, 0, 0]
    lut[5:10] = [115, 25, 25]
    lut[10:15] = [130, 50, 50]
    lut[15:20] = [145, 75, 75]
    lut[20:25] = [160, 100, 100]
    lut[25:30] = [175, 125, 125]
    lut[30:35] = [190, 150, 150]
    lut[35:40] = [205, 175, 175]
    lut[40:45] = [220, 200, 200]
    lut[45:50] = [235, 225, 225]
    # 偏差値50以上は白から濃い赤へ段階的に変化
    lut[50:55] = [255, 255, 255]
    lut[55:60] = [225, 225, 240]
    lut[60:65] = [195, 195, 225]
    lut[65:70] = [165, 165, 210]
    lut[70:75] = [135, 135, 195]
    lut[75:80] = [105, 105, 180]
    lut[80:85] = [75, 75, 165]
    lut[85:90] = [45, 45, 150]
    lut[90:95] = [15, 15, 135]
    lut[95:256] = [0, 0, 120]
    return lut


def normalize_image(image):
    """
    画像を50〜100に正規化する
    image:
        meanやstdなどの2次元画像
    Returns:
        50〜100のuint8画像
    """

    img_min = image.min()
    img_max = image.max()

    # 全画素が同じ値の場合
    if img_max == img_min:
        return np.zeros_like(image, dtype=np.uint8)

    normalized = (image - img_min) / (img_max - img_min) * 50 + 50

    return normalized.astype(np.uint8)


def statistics_image(image,save_path=""):
    """
    meanやstdを正規化してカラーマップ画像として保存
    """

    # 0〜100に正規化
    normalized_image = normalize_image(image)

    # LUT適用のため3チャンネル化
    three_channel_image = cv2.cvtColor(normalized_image, cv2.COLOR_GRAY2BGR)

    # カラーマップ適用
    color_mapped_image = cv2.LUT(three_channel_image, create_colormap())
    if save_path:
        # 保存
        cv2.imwrite(save_path, color_mapped_image)
    
    return color_mapped_image


def crop_and_pad(
    img: np.ndarray, cx: int, cy: int, crop_h: int, crop_w: int
) -> np.ndarray:
    # 切り抜きたい理想の範囲（画面外にはみ出す可能性あり）
    h, w = img.shape
    crop_h=int(crop_h/2)
    crop_w=int(crop_w/2)
    y1, y2 = cy - crop_h, cy + crop_h
    x1, x2 = cx - crop_w, cx + crop_w

    # 画面外にはみ出している量（余白の計算）
    top = max(0, -y1)
    bottom = max(0, y2 - h)
    left = max(0, -x1)
    right = max(0, x2 - w)

    # 画面内に収まる安全な範囲だけでまずは切りぬく
    crop_y1, crop_y2 = max(0, y1), min(h, y2)
    crop_x1, crop_x2 = max(0, x1), min(w, x2)
    cropped = img[crop_y1:crop_y2, crop_x1:crop_x2]

    # はみ出していた部分を黒色（0）で埋めて、常にsize x size にする
    padded = cv2.copyMakeBorder(
        cropped, top, bottom, left, right, cv2.BORDER_CONSTANT, value=0
    )

    return padded


def extract_sun_mini(
    dir_path: str, h_size: int, w_size: int
) -> tuple[np.ndarray, np.ndarray]:
    """フォルダ内の太陽画像から太陽中心を算出し、指定サイズで切りぬいた画像配列を返します。
    画面端にかかる場合は、足りない部分を黒く塗りつぶします。

    Args:
        folder(str):対象の画像が保存されているフォルダのパス
        h_size(int):切りぬく長方形の縦幅
        w_size(int):切りぬく長方形の横幅

    Returns:
        tuple[np.ndarray, np.ndarray]:
            - 切りぬかれた画像の3次元配列（N,h_size,w_size)
            - 各画像の中心座標配列（N,2）
    """

    print(f"---画像の読み込みと切り抜き処理を開始:{dir_path}---")
    # 画像ファイルのみ1000枚取得
    image_names = get_image_names_from_dir(dir_path)
    frames = []
    min2_centers = []
    # tqdmによる進捗表示
    for name in tqdm.tqdm(image_names, desc="Processing images"):
        # 16bit(下位12bit)画像を輝度値(1ch)のまま正しく読み込む
        img = load_image_from_path_cv2(dir_path, name)
        if img is None:
            continue
        try:
            cx, cy, r = MIN2_ignore_sunspots(img, show=False, debug=False)
        except Exception:
            continue

        cx = int(cx)
        cy = int(cy)

        padded = crop_and_pad(img, cx, cy, h_size, w_size)

        frames.append(padded)
        min2_centers.append([cx,cy])

    return np.array(frames), np.array(min2_centers)


def calculate_hensachi(frames: np.ndarray):
    """平均画像・標準偏差画像・偏差値画像を計算する。"""

    # 平均画像
    mean = np.mean(frames, axis=0)

    # 標準偏差画像
    std = np.std(frames, axis=0)

    # 偏差値画像
    hensachi = np.where(std == 0, 50, 50 + 10 * (frames - mean) / std)

    return mean, std, hensachi

    """
    #偏差値画像を1枚ずつ表示する。
    for i in range(len(hensachi)):
        print(f"{i+1}枚目の偏差値画像")
        print(hensachi[i])
    """
