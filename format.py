import os
import re
import sys
import MeCab

nm = MeCab.Tagger('-Owakati')


def clean(raw_text):
    """
    ルビや入力者注を削除して一文毎に分割,分かち書き
    """
    text = raw_text.replace('\n', '').replace('\u3000', '')
    text = re.sub('[［《]', '／', text)
    text = re.sub('[］》]', '＼', text)
    text = re.sub('／[^＼]*?＼', '', text)
    text = text.replace('。', '。\n')
    text = text.replace('「', '')
    text = text.replace('」', '\n').split('\n')

    return [nm.parse(t).split(' ') for t in text if t]


def make_stopdic(lines):
    """
    空白区切りの文の集まりのテキストのリストからストップワードの辞書を作成する。
    """
    calc_words = {}
    for line in lines:
        for word in line:
            if word in calc_words:
                calc_words[str(word)] += 1
            else:
                calc_words[str(word)] = 1
    sorted_stop = sorted(calc_words.items(), key=lambda x: x[1], reverse=True)
    print("sorted_stop:" + str(len(sorted_stop)))
    freq_num = int(len(sorted_stop) * 0.03) # 単語数の3%を算出
    n = 0
    stop_words = []
    print("freq_num:" + str(freq_num))
    for data in sorted_stop:
        stop_words.append(str(data[0]))
        n += 1
        if n > freq_num:
            break
    # 作成したストップワードの辞書の保存
    with open('./origin_stopwords.txt', 'w', encoding="utf-8") as f:
        f.write('\n'.join(stop_words))


def stopword_bydic(text):
    """
    辞書によるストップワードの除去
    """
    # 読み込むストップワード辞書の指定。
    with open('./origin_stopwords.txt', encoding="utf-8") as f:
        data = f.read()
        stopwords = data.split('\n')
    lines = []
    for line in text:
        words = []
        for word in line:
            if word not in stopwords:
                words.append(word)
        lines.append(words)
    return lines


def format(input_folder, output_file, create_stopwords=False):
    authors = {'dazai': [], 'mori': [], 'akutagawa': []}
    cleaned_data = []

    # txtファイルを全部読み込んで分かち書きやクリーニングをしていく
    files = [f for f in os.listdir(input_folder) if f.split('.')[-1] == 'txt']
    for f in files:
        name = f.split('.')[0]
        print(name)
        with open(os.path.join(input_folder, f), 'r', encoding="utf-8") as f:
            clean_text = clean(f.read())
            authors[name] = clean_text
            cleaned_data += clean_text

    make_stopdic(cleaned_data)
    print("cleaned_data:" + str(len(cleaned_data)))

    # ストップワードリストの作成
    stop_data = {}
    for f in files:
        with open(os.path.join(input_folder, f), encoding="utf-8") as f1:
            print(f)
            nm = MeCab.Tagger('-Owakati')
            text = nm.parse(f1.read()).split(' ')
            for word in text:
                if word in stop_data:
                    stop_data[str(word)] += 1
                else:
                    stop_data[str(word)] = 1

    sorted_stop = sorted(stop_data.items(), key=lambda x: x[1], reverse=True)

    print(len(sorted_stop))

    freq_num = int(len(sorted_stop) * 0.03)
    n = 0
    stop_words = []
    print(freq_num)
    for data in sorted_stop:
        stop_words.append(str(data[0]))
        print('High frequency word: ', str(data[0]), str(data[1]))
        n += 1
        if n > freq_num:
            break

    # 作成したストップワードの辞書の保存
    if create_stopwords:
        with open('./origin_stopwords.txt', 'w', encoding="utf-8") as f:
            f.write('\n'.join(stop_words))

    sum_lines = len(stopword_bydic(cleaned_data))
    sum_words = []
    for line in stopword_bydic(cleaned_data):
        for word in line:
            if word not in sum_words:
                sum_words.append(word)
    print('sum_lines: ', sum_lines)
    print('sum_words: ', len(sum_words))
    with open('origin_words.txt', 'w', encoding="utf-8") as f:
        f.write('\n'.join(sum_words))
    cleaned_data = []
    for author, data in authors.items():
        data = stopword_bydic(data)
        for line in data:
            cleaned_data.append(author + ',' + ' '.join(line))

    # 作成したコーパスの保存
    with open(output_file, 'w', encoding="utf-8") as f:
        f.write(''.join(cleaned_data))


def main():
    # データセットフォルダと出力ファイル名を指定
    input_folder = 'text_raw_dataset'
    output_file = 'corpus.csv'
    format(input_folder, output_file, create_stopwords=False)


if __name__ == "__main__":
    main()

