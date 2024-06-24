# モジュール読み込み
import csv
import pickle

import gensim
from gensim import models
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

dataset_file_name = './corpus.csv'
model_file_name = 'logistic.pkl'

# csvファイルを扱いやすいフォーマットに変形

with open(dataset_file_name, 'r', encoding='utf-8') as f:
    data = list(csv.reader(f))

texts, label_ids = [], []
label2id = {}
idx_label, idx_sentence = 0, 1
sum_words = []

for counter, row in enumerate(data):
    if counter == 0:
        continue
    label = row[idx_label]
    if label not in label2id:
        label2id[label] = len(label2id)
    label_ids.append(label2id[label])
    word_list = row[idx_sentence].split(' ')
    texts.append(word_list)

    for line in word_list:
        for word in line:
            sum_words.append(word)

print('sum_words: ', len(sum_words))
id2label = {v: k for k, v in label2id.items()}

#　テキストとラベルのデータをtrain, testに分割します
X_train_texts, X_test_texts, y_train, y_test = train_test_split(texts, label_ids, test_size=0.2, random_state=42)

# trainのテキストデータから、tfidfで重み付けされた単語文書行列を作成します

# テキストデータから辞書を作成します
dictionary = gensim.corpora.Dictionary(X_train_texts)
# 辞書を用いてBoW形式に文章を行列化します
corpus = [dictionary.doc2bow(text) for text in X_train_texts]

# BoW形式で作成したcorpusをtfidfを用いて重み付けします
tfidf_model = models.TfidfModel(corpus)
tfidf_corpus = tfidf_model[corpus]

num_words = len(dictionary)
X_train_tfidf = gensim.matutils.corpus2dense(tfidf_corpus, num_terms=num_words).T

# testのテキストデータから、tfidfで重み付けされた単語文書行列を作成します

# 辞書を用いてBoW形式に文章を行列化します
corpus = [dictionary.doc2bow(text) for text in X_test_texts]
# BoW形式で作成したcorpusをtfidfを用いて重み付けします
tfidf_corpus = tfidf_model[corpus]

num_words = len(dictionary)
X_test_tfidf = gensim.matutils.corpus2dense(tfidf_corpus, num_terms=num_words).T

# trainデータを用いて分類器を構築します
clf = LogisticRegression(C=1, penalty='l2')
clf.fit(X_train_tfidf, y_train)

# testデータを用いて分類器の精度を評価します
y_pred = clf.predict(X_test_tfidf)
target_names = list(id2label.values())

print(classification_report(y_test, y_pred, target_names=target_names))
print(confusion_matrix(y_test, y_pred))