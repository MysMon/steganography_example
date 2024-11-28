import argparse
from PIL import Image

def text_to_bits(text):
    """テキストをビット列に変換する関数"""
    bits = ''
    for char in text:
        # 各文字をASCIIコードに変換
        ascii_code = ord(char)
        # ASCIIコードを8ビットのバイナリ文字列に変換（ゼロパディング）
        binary_string = format(ascii_code, '08b')
        # ビット列に追加
        bits += binary_string
    return bits

def embed_bits_in_color(color_value, bits_to_embed, num_bits):
    """
    カラー値の下位num_bitsビットをbits_to_embedで置き換える関数
    """
    # カラー値を8ビットのバイナリ文字列に変換
    color_bits = format(color_value, '08b')

    # 埋め込むビット列がnum_bits未満の場合、残りを元のビットで補完
    bits_to_embed = bits_to_embed.ljust(num_bits, '0')

    # 新しいカラー値のビット列を作成（上位ビットはそのまま、下位ビットを置き換え）
    new_color_bits = color_bits[:-num_bits] + bits_to_embed

    # 新しいカラー値を整数に変換して返す
    new_color_value = int(new_color_bits, 2)
    return new_color_value

def embed_text_in_image(image_path, output_path, text, num_bits):
    """画像にテキストを埋め込むメインの関数"""
    # 終了マーカー（ETX文字：ASCIIコード3）をテキストの末尾に追加
    end_marker = chr(3)
    text += end_marker

    if not (1 <= num_bits <= 8):
        print("ビット数は1から8の間で指定してください。")
        return

    try:
        image = Image.open(image_path)
    except IOError:
        print("画像の読み込みに失敗しました。ファイルパスを確認してください。")
        return

    # 画像モードがRGBまたはRGBAでない場合、RGBAに変換
    if image.mode not in ('RGB', 'RGBA'):
        image = image.convert('RGBA')

    # ピクセルデータを取得
    pixels = image.load()
    width, height = image.size

    # テキストをビット列に変換
    text_bits = text_to_bits(text)
    text_len = len(text_bits)

    # 画像に埋め込める最大ビット数を計算
    max_capacity = width * height * 3 * num_bits

    # テキストが埋め込み可能か確認
    if text_len > max_capacity:
        print(f"テキストが長すぎます。埋め込める最大ビット数は{max_capacity}です。")
        return

    # 埋め込み開始位置のビットインデックスを初期化
    bit_index = 0

    # 画像の各ピクセルを走査
    for y in range(height):
        for x in range(width):
            # すべてのビットを埋め込んだ場合、ループを終了
            if bit_index >= text_len:
                break

            # 現在のピクセルのカラー値（RGB）を取得
            pixel = pixels[x, y]
            r, g, b = pixel[:3]
            new_rgb = []

            # 各カラー成分に対してビットを埋め込む
            for color in (r, g, b):
                if bit_index < text_len:
                    # 埋め込むべき残りのビット数を計算
                    bits_remaining = text_len - bit_index
                    # 現在のカラー値に埋め込むビット数を決定
                    num_bits_to_embed = min(num_bits, bits_remaining)
                    # 埋め込むビット列を取得
                    bits_to_embed = text_bits[bit_index:bit_index + num_bits_to_embed]
                    # カラー値にビットを埋め込む
                    new_color_value = embed_bits_in_color(color, bits_to_embed, num_bits)
                    # ビットインデックスを更新
                    bit_index += num_bits_to_embed
                else:
                    # 埋め込むビットがない場合は元のカラー値を使用
                    new_color_value = color
                # 新しいカラー値をリストに追加
                new_rgb.append(new_color_value)

            # アルファチャネルがある場合はそのまま保持
            if len(pixel) == 4:
                new_pixel = (*new_rgb, pixel[3])
            else:
                new_pixel = tuple(new_rgb)

            # ピクセルデータを更新
            pixels[x, y] = new_pixel

        if bit_index >= text_len:
            break
    try:
        image.save(output_path)
        print(f"テキストを埋め込みました。出力ファイル：{output_path}")
    except IOError:
        print("画像の保存に失敗しました。出力パスを確認してください。")

def main():
    parser = argparse.ArgumentParser(description='画像にテキストを埋め込むツール')

    parser.add_argument('input_image', help='入力画像のパス')
    parser.add_argument('output_image', help='出力画像のパス')
    parser.add_argument('text', help='埋め込むテキスト')
    parser.add_argument('bits', type=int, help='各カラー値に埋め込むビット数（1〜8）')
    # 引数を解析
    args = parser.parse_args()

    embed_text_in_image(args.input_image, args.output_image, args.text, args.bits)

if __name__ == "__main__":
    main()