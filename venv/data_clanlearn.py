import pandas as pd
import numpy as np
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score
from gensim.models import Word2Vec
from collections import Counter

# 1. CSVファイルの読み込み
data = pd.read_csv("job_data.csv")
print("データを確認:\n", data.head())

# 2. 欠損値の処理
data = data.fillna("")  # 欠損値を空白で埋める

# 3. テキストデータの前処理
data['仕事内容'] = data['仕事内容'].str.lower()  # 小文字化
data['必要なスキル・経験'] = data['必要なスキル・経験'].str.lower()

# 4. 不要なキーワードの削除
remove_keywords = [
    "【概要】", "【事業内容】", "【案件例】", "【仕事の魅力】", "など", "仕事内容:", "◎開発メンバー", "...etc",
    "【仕事内容】", "■開発環境", "etc...", "【主な業務内容】", "【開発環境】", "etc...", "▽", "/", "【", "】", ":",
    ",", "→", "on", "...etc", "【プロジェクト例】", "▽", "【", "】", ":", "+",
    "開発", "運用", "【開発環境】", "-", "*"
]
def clean_text(text):
    return re.sub(r"|".join(map(re.escape, remove_keywords)), "", text)

data['仕事内容'] = data['仕事内容'].apply(clean_text)
data['必要なスキル・経験'] = data['必要なスキル・経験'].apply(clean_text)

# クレンジング後のデータを保存
data.to_csv("cleaned_filtered_data.csv", index=False, encoding="utf-8")
print("クレンジング後のデータを保存しました: cleaned_filtered_data.csv")

# 5. 重複単語の抽出
all_text = " ".join(data['仕事内容']) + " " + " ".join(data['必要なスキル・経験'])
words = all_text.split()
word_counts = Counter(words)
duplicate_words = {word: count for word, count in word_counts.items() if count > 1}

duplicate_df = pd.DataFrame(list(duplicate_words.items()), columns=['単語', '出現回数'])
duplicate_df.to_csv("duplicate_words.csv", index=False, encoding="utf-8")
print("重複ワードを保存しました: duplicate_words.csv")

# 6. TF-IDFベクトル化
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data['仕事内容'] + " " + data['必要なスキル・経験'])

# 7. ラベル列の作成（仮のラベル付け）
data['ラベル'] = np.random.randint(0, 2, size=len(data))  # 仮ラベル
y = data['ラベル']
print("ラベルの分布:\n", data['ラベル'].value_counts())

# 8. データ分割
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 9. モデルのトレーニング（Random Forest）
rf_model = RandomForestClassifier()
rf_model.fit(X_train, y_train)
rf_accuracy = rf_model.score(X_test, y_test)
print(f"Random Forestモデルの精度: {rf_accuracy:.2f}")

# 10. Word2Vecでベクトル化
documents = data['仕事内容'] + " " + data['必要なスキル・経験']
sentences = [doc.split() for doc in documents]
word2vec_model = Word2Vec(sentences, vector_size=100, window=5, min_count=1)

# 文書をベクトルに変換
X_word2vec = [word2vec_model.wv[doc.split()] for doc in documents]

# モデルのトレーニング（Gradient Boosting）
gb_model = GradientBoostingClassifier()
gb_model.fit(X_train, y_train)
gb_accuracy = gb_model.score(X_test, y_test)
print(f"Gradient Boostingモデルの精度（Word2Vec使用）: {gb_accuracy:.2f}")