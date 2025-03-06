import re
import argparse

def convert_file(input_file, output_file):
    # 正規表現パターン: 行の先頭が # で始まり、その後に数字とタイトルが続く形式をマッチ
    pattern = r"^(#+) ([\d.]+) (.+)$"  # 例: # 1.1 sample text

    def replacement(match):
        heading_level = match.group(1)  # 見出し記号の個数 (例: `#`, `##`, `###`, `####`)
        number = match.group(2)         # 数字部分 (例: `1`, `1.1`, `1.1.1`, `1.1.1.1`)
        title = match.group(3)          # タイトル部分 (例: `sample text`)

        # スラッシュ `/` および丸括弧 `()` をタイトル部分から削除
        # title = title.replace("/", "").replace("(", "").replace(")", "")

        # IDを生成: 数字部分のピリオドを削除、スペースをハイフンに置き換え、小文字化
        id_value = f"{number.replace('.', '')}-{title.replace(' ', '-').replace("/", "").replace("(", "").replace(")", "").lower()}"

        # 新しいフォーマット: `見出し記号 数字 タイトル <a id= ... ></a>`
        return f"<a id=\"{id_value}\"></a>\n\n{heading_level} {number} {title}"

    # 入力ファイルを開いて読み込み
    with open(input_file, "r", encoding="utf-8") as infile:
        lines = infile.readlines()

    # 行ごとに変換を実施
    processed_lines = []
    for line in lines:
        # 行が見出しパターンにマッチするかチェック
        if re.match(pattern, line):
            transformed_line = re.sub(pattern, replacement, line)
            processed_lines.append(transformed_line)
        else:
            # マッチしない場合、そのまま保持
            processed_lines.append(line)

    # 結果を出力ファイルに書き込み
    with open(output_file, "w", encoding="utf-8") as outfile:
        outfile.writelines(processed_lines)


def main():
    # コマンドライン引数のパーサーを設定
    parser = argparse.ArgumentParser(description="Convert heading lines with anchors.")
    parser.add_argument("input_file", help="The input file containing the text to be converted.")
    parser.add_argument("output_file", help="The output file to save the converted text.")
    args = parser.parse_args()

    # ファイル変換処理を実行
    convert_file(args.input_file, args.output_file)


if __name__ == "__main__":
    main()
