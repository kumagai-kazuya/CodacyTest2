import sys
import os
import re

def conv_main(input_filename, output_filename):
    try:
        with open(input_filename, 'r', encoding='utf-8') as infile, \
             open(output_filename, 'w', encoding='utf-8') as outfile:
            inside_toc = False
            inside_changelog = False
            for line in infile:
                # <Toc></Toc> <ChangeLog></ChangeLog>　タグで囲まれた部分は除外（無変換）する
                if line.strip() == "<Toc>":
                    inside_toc = True
                elif line.strip() == "</Toc>":
                    inside_toc = False
                elif line.strip() == "<ChangeLog>":
                    inside_changelog = True
                elif line.strip() == "</ChangeLog>":
                    inside_changelog = False

                if (inside_toc and line.strip() != "<Toc>") or (inside_changelog and line.strip() != "<ChangeLog>"):
                    outfile.write(line)

                # 行変換対象処理
                if (not inside_toc and line.strip() != "</Toc>") and (not inside_changelog and line.strip() != "</ChangeLog>"):
                    converted_line = convert_patterns_to_markdown_heading(line)
                    outfile.write(converted_line)

    except FileNotFoundError:
        print(f"Error: The file '{input_filename}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

# 

# パターンにマッチした行をMarkdownの見出しに変換する
def convert_patterns_to_markdown_heading(line):
    # 正規表現パターンを定義
    pattern = r'\[([0-9]+(\.[0-9]+)*)\]'
    match = re.match(pattern, line.strip())
    
    # パターンにマッチした場合、変換を行う
    if match:
        levels = match.group(1).split('.')
        heading_level = '#' * len(levels)  # レベルに応じたMarkdownの見出しを作成
        remaining_text = line[len(match.group(0)):].strip()
        return f'{heading_level} {match.group(1)} {remaining_text}'
    return line

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_changelog.py input_filename")
    else:
        input_filename = sys.argv[1]
        base_filename = os.path.splitext(input_filename)[0]
        output_filename = base_filename + ".md"
        conv_main(input_filename, output_filename)
