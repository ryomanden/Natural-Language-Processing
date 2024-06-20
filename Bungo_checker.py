import os
import pandas as pd
import MeCab
from sklearn.feature_extraction.text import TfidfVectorizer


def read_text_files(directory):
    text_files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    texts = {}
    for file in text_files:
        with open(os.path.join(directory, file), 'r', encoding='utf-8') as f:
            texts[file] = f.read()
    return texts


def split_text(filepath):
    def parse_text(text, tagger):
        node = tagger.parseToNode(text)
        parsed_result = []
        while node:
            word_info = node.surface
            parsed_result.append(word_info)
            node = node.next
        return parsed_result

    tagger = MeCab.Tagger()
    texts = read_text_files(filepath)
    flattened_parsed_texts = []
    for file, text in texts.items():
        parsed_text = parse_text(text, tagger)

        flattened_parsed_texts.extend(parsed_text)

    return flattened_parsed_texts


def word_count(texts):
    result = {}
    for text in texts:
        if text in result:
            result[text] += 1
        else:
            result[text] = 1

    return result


def tf_idf(texts):
    vectorizer = TfidfVectorizer(smooth_idf=False)
    X = vectorizer.fit_transform(texts)

    values = X.toarray()
    feature_names = vectorizer.get_feature_names_out()
    tfidf = pd.DataFrame(values, columns=feature_names)

    return values, feature_names, tfidf


def main():
    splitted_texts = split_text('text_raw_dataset/AkutagawaRyunosuke')
    word_count_dict = word_count(splitted_texts)
    word_count_dict = dict(sorted(word_count_dict.items(), key=lambda x: x[1], reverse=True))

    docs = read_text_files('text_raw_dataset/AkutagawaRyunosuke')

    # print()

    values, feature_names, tfidf = tf_idf(list(docs.values()))

    print(tfidf)


if __name__ == '__main__':
    main()
