import numpy as np
import ffmpeg

def compress_analysis_frames(
    frames: np.ndarray, 
    output_path: str, 
    fps: int = 30, 
    lossless: bool = True,
    pix_fmt_in: str = 'rgb24'
) -> None:
    """
    ノイズ状の解析結果画像の配列(np.ndarray)を保存する関数

    :param frames: (N, H, W, 3) の uint8 配列
    :param output_path: 保存先のmp4パス
    :param lossless: Trueの場合は完全無劣化(CRF 0)、Falseの場合は高品質視認用(CRF 18)
    """
    num_frames, height, width, _ = frames.shape

    output_args = {
        'r': fps,
        'preset': 'veryslow', # 画像に対して圧縮効率を高める設定
    }

    if lossless:
        # 完全無劣化 (Lossless) 設定
        output_args.update({
            'vcodec': 'libx264rgb',
            'crf': 0,
            'pixel_format': 'rgb24' # 色変換による劣化を防止
        })
    else:
        # 高品質（視認用）設定
        output_args.update({
            'vcodec': 'libx264',
            'crf': 18,
            'pix_fmt': 'yuv420p' # 互換性重視（※色滲みが発生します）
        })

    process = (
        ffmpeg
        .input('pipe:', format='rawvideo', pix_fmt=pix_fmt_in, s=f'{width}x{height}', r=fps)
        .output(output_path, **output_args)
        .overwrite_output()
        .run_async(pipe_stdin=True)
    )

    process.stdin.write(frames.tobytes())
    process.stdin.close()
    process.wait()

    print(f"[INFO]:finish ({'lossless' if lossless else 'CRF=18'}): {output_path}")