import argparse
from PIL import Image

def extract_text_from_image(image_path, num_bits):
    """画像からテキストを抽出する"""
    # num_bitsのバリデーション
    if not (1 <= num_bits <= 8):
        print("ビット数は1から8の間で指定してください。")
        return

    try:
        image = Image.open(image_path)
    except IOError:
        print("画像の読み込みに失敗しました。ファイルパスを確認してください。")
        return

    # 画像モードの確認とアルファチャネルの対応
    if image.mode not in ('RGB', 'RGBA'):
        image = image.convert('RGBA')
    pixels = image.load()
    width, height = image.size

    # ピクセルデータからテキストビットを抽出
    extracted_bits = ''
    extracted_text = ''
    for y in range(height):
        for x in range(width):
            pixel = pixels[x, y]
            r, g, b = pixel[:3]
            for color in (r, g, b):
                color_bits = format(color, '08b')
                extracted_bits += color_bits[-num_bits:]
                # 8ビットごとに文字に変換
                while len(extracted_bits) >= 8:
                    byte_bits = extracted_bits[:8]
                    extracted_bits = extracted_bits[8:]
                    byte_value = int(byte_bits, 2)
                    char = chr(byte_value)
                    if char == chr(3):  # 終了マーカー（ETX）を検出
                        print("抽出したテキスト：")
                        print(extracted_text)
                        return
                    extracted_text += char
    # 終了マーカーが見つからなかった場合
    print("終了マーカーが見つかりませんでした。正しい画像またはビット数を指定してください。")

def main():
    parser = argparse.ArgumentParser(description='画像からテキストを抽出するツール')
    parser.add_argument('input_image', help='入力画像のパス')
    parser.add_argument('bits', type=int, help='各カラー値から抽出するビット数（1〜8）')
    args = parser.parse_args()

    extract_text_from_image(args.input_image, args.bits)


if __name__ == "__main__":
    main()