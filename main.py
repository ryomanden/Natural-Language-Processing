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


def main(dataset, author, cleaned=False):
    if cleaned:
        texts = read_text_files(f'{dataset}/{author}_cleaned')
    else:
        texts = read_text_files(f'{dataset}/{author}')

    tagger = MeCab.Tagger()
    word_counts = 30

    flattened_parsed_texts = []
    for file, text in texts.items():
        parsed_text = parse_text(text, tagger)
        flattened_parsed_texts.extend(parsed_text)

    word_count_dict = word_count(flattened_parsed_texts)
    word_count_dict = dict(sorted(word_count_dict.items(), key=lambda x: x[1], reverse=True)[:word_counts])
    print(word_count_dict)

    labels = list(word_count_dict.keys())
    values = list(word_count_dict.values())

    plt.figure(figsize=(10, 5))
    plt.bar(labels, values, color='gray')
    plt.xlabel('Words', fontproperties=font_mono_prop)
    plt.ylabel('Values', fontproperties=font_mono_prop)
    plt.title(f"{author}'s Top {word_counts} words ({dataset})", fontproperties=font_mono_prop)

    plt.xticks(rotation=90, fontproperties=font_mono_prop)
    plt.yticks(fontproperties=font_mono_prop)

    plt.savefig(f'result/Top_{word_counts}_words_chart_{author}_{dataset}.svg')
    plt.show()

    wc = wordcloud.WordCloud(font_path=font_seed_path, width=1080, height=720, background_color='white')
    wc.generate_from_frequencies(word_count_dict)

    plt.imsave(f'result/Top_{word_counts}_wordcloud_{author}_{dataset}.png', wc.to_array())


if __name__ == "__main__":
    dataset = 'text_raw_dataset'
    cleaned = False
    main(dataset, 'AkutagawaRyunosuke', cleaned)
    main(dataset, 'DazaiOsamu', cleaned)
    main(dataset, 'MoriOgai', cleaned)