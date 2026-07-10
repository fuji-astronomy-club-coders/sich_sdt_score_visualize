mean=np.mean(frames,axis=0)
std=np.std(frames,axis=0)
#偏差値を計算
hensachi=50+10*(frames-mean)/std
#1フレーム目の偏差値画像を見る。
hensachi_frame1=hensachi[0]
print(hensachi_frame1)