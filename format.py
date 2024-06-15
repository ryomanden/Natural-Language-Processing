import os
import glob
import re

# 入力フォルダと出力フォルダのパスを指定
input_folder = 'dataset/MoriOgai'
output_folder = 'dataset/MoriOgai_cleaned'

# フォルダが存在しない場合は作成
os.makedirs(output_folder, exist_ok=True)


def clean_text(text):
    # メタデータセクションを削除する
    lines = text.split('\n')
    clean_lines = []
    inside_metadata = False
    for line in lines:
        if '-------------------------------------------------------' in line:
            inside_metadata = not inside_metadata
            continue
        if inside_metadata:
            continue
        clean_lines.append(line)

    # メタデータセクションの外の部分のみ保持
    clean_text = '\n'.join(clean_lines)

    # 最初の空行またはタイトル行まで削除
    clean_text = re.sub(r'^(.*?\n)*?\n', '', clean_text, count=1)

    # 底本以降を削除
    clean_text = re.sub(r'\n底本.*$', '', clean_text, flags=re.DOTALL)

    # 特定の記号と囲まれた部分を削除
    clean_text = re.sub(r'《.*?》', '', clean_text)
    clean_text = re.sub(r'［＃.*?］', '', clean_text)
    clean_text = clean_text.replace('｜', '')

    return clean_text


def convert_file(input_file, output_file):
    with open(input_file, 'r', encoding='shift_jis', errors='ignore') as f:
        text = f.read()

    clean_content = clean_text(text)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(clean_content)


def process_files(input_folder, output_folder):
    files = glob.glob(os.path.join(input_folder, '*.txt'))
    for input_file in files:
        file_name = os.path.basename(input_file)
        output_file = os.path.join(output_folder, file_name)
        convert_file(input_file, output_file)
        print(f"Processed: {file_name}")


# 実行
process_files(input_folder, output_folder)
