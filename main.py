import os
import MeCab
import matplotlib.pyplot as plt
from matplotlib import font_manager
# import matplotlib_fontja
import wordcloud

font_mono_path = 'fonts/LINESeedJP_OTF_Rg.otf'
font_seed_path = 'fonts/LINESeedJP_OTF_0.otf'
font_mono_prop = font_manager.FontProperties(fname=font_mono_path)


def read_text_files(directory):
    text_files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    texts = {}
    for file in text_files:
        with open(os.path.join(directory, file), 'r', encoding='utf-8') as f:
            texts[file] = f.read()
    return texts


def parse_text(text, tagger):
    node = tagger.parseToNode(text)
    parsed_result = []
    while node:
        word_info = node.surface
        parsed_result.append(word_info)
        node = node.next
    return parsed_result

def word_count(texts):
    word_count = {}
    for text in texts:
        for word in text:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1
    return word_count

def main(directory):
    texts = read_text_files(directory)
    tagger = MeCab.Tagger()

    flattened_parsed_texts = []
    for file, text in texts.items():
        parsed_text = parse_text(text, tagger)
        flattened_parsed_texts.extend(parsed_text)

    word_count_dict = word_count(flattened_parsed_texts)
    word_count_dict = dict(sorted(word_count_dict.items(), key=lambda x: x[1], reverse=True)[:10])
    print(word_count_dict)

    labels = list(word_count_dict.keys())
    values = list(word_count_dict.values())

    plt.figure(figsize=(10, 5))
    plt.bar(labels, values)
    plt.xlabel('Labels', fontproperties=font_prop)
    plt.ylabel('Values', fontproperties=font_prop)
    plt.title('Top 10 words', fontproperties=font_prop)

    plt.xticks(fontproperties=font_prop)
    plt.yticks(fontproperties=font_prop)

    plt.savefig(f'result/Top_{word_counts}_words_chart_{author}_{dataset}.svg')
    plt.show()

    wc = wordcloud.WordCloud(font_path=font_path, width=800, height=400, background_color='white')
    wc.generate_from_frequencies(word_count_dict)

    plt.imsave('result/wordcloud.png', wc.to_array())

if __name__ == "__main__":
    main('dataset/AkutagawaRyunosuke_cleaned')
