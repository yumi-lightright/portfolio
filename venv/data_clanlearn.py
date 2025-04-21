import pandas as pd
import numpy as np
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score
from gensim.models import Word2Vec
from collections import Counter
import MeCab
import csv

# CSVファイルを読み込み
input_file = "skills_and_experience.csv"  # 入力ファイルのパスを指定
data = pd.read_csv(input_file)


# 条件を判別するキーワード
必須条件_keywords = ["必須", "MUST", "必須要件", "必須スキル", "必要なスキル", "必須要件(以下のいずれか)","応募要件"]
歓迎条件_keywords = ["歓迎", "WANT", "歓迎要件", "歓迎スキル","望ましい経験／能力","尚可要件"]
求める人物像_keywords = ["求める人物像", "特徴","求める人物タイプ"]

def classify_lines(text):
    必須条件 = []
    歓迎条件 = []
    求める人物像 = []

    # テキストを行に分割
    lines = text.split('\n')

    # 現在のカテゴリ
    current_category = None

    for line in lines:
        # 各行がどのカテゴリに属するかを判定
        if any(keyword in line for keyword in 必須条件_keywords):
            current_category = '必須条件'
            必須条件.append(line)
        elif any(keyword in line for keyword in 歓迎条件_keywords):
            current_category = '歓迎条件'
            歓迎条件.append(line)
        elif any(keyword in line for keyword in 求める人物像_keywords):
            current_category = '求める人物像'
            求める人物像.append(line)
        elif current_category == '必須条件':
            必須条件.append(line)
        elif current_category == '歓迎条件':
            歓迎条件.append(line)
        elif current_category == '求める人物像':
            求める人物像.append(line)

    return '\n'.join(必須条件), '\n'.join(歓迎条件), '\n'.join(求める人物像)

# 入力CSVファイルを開く
with open('skills_and_experience.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    
    # 分けるCSVファイルを準備
    必須条件_file = open('必須条件.csv', 'w', newline='', encoding='utf-8')
    歓迎条件_file = open('歓迎条件.csv', 'w', newline='', encoding='utf-8')
    求める人物像_file = open('求める人物像.csv', 'w', newline='', encoding='utf-8')

    必須条件_writer = csv.writer(必須条件_file)
    歓迎条件_writer = csv.writer(歓迎条件_file)
    求める人物像_writer = csv.writer(求める人物像_file)

    # ヘッダーを書き込む
    必須条件_writer.writerow(['項目'])
    歓迎条件_writer.writerow(['項目'])
    求める人物像_writer.writerow(['項目'])

    # 各行をカテゴリごとに分けて書き込む
    for row in reader:
        text = row['必要なスキル・経験']
        必須条件, 歓迎条件, 求める人物像 = classify_lines(text)

        if 必須条件:
            必須条件_writer.writerow([必須条件])
        if 歓迎条件:
            歓迎条件_writer.writerow([歓迎条件])
        if 求める人物像:
            求める人物像_writer.writerow([求める人物像])

    # ファイルを閉じる
    必須条件_file.close()
    歓迎条件_file.close()
    求める人物像_file.close()

# ファイル名と対応するデータフレーム名を辞書で管理
file_paths = {
    "job_data": "job_descriptions.csv",
    "requisite_data": "必須条件.csv",
    "welcome_data": "歓迎条件.csv",
    "character_data": "求める人物像.csv",
}


# CSVファイルを読み込む辞書
data_frames = {name: pd.read_csv(path) for name, path in file_paths.items()}

# 欠損値を空白で埋める処理
data_frames = {name: df.fillna("") for name, df in data_frames.items()}

# データフレームのアクセス例
job_data = data_frames["job_data"]
requisite_data = data_frames["requisite_data"]
welcome_data = data_frames["welcome_data"]
character_data = data_frames["character_data"]

print(requisite_data.columns)


def preprocess_text(text, stopwords):
    # 小文字化（英語の場合）
    text = text.lower()
    
    # 特殊文字を削除
    text = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff]", " ", text)
    
    # 不要な空白を削除
    text = re.sub(r"\s+", " ", text).strip()
    
    # MeCabを使った形態素解析
    mecab = MeCab.Tagger("-Owakati")
    tokens = mecab.parse(text).strip().split()
    
    # ストップワードを除去
    tokens = [word for word in tokens if word not in stopwords and len(word) > 1]
    
    return " ".join(tokens)

# ストップワードの設定
stopwords = set(["の", "と", "して", "は", "ます", "です", "など"])

# テキストデータの前処理
job_data["仕事内容"] = job_data["仕事内容"].apply(lambda x: preprocess_text(str(x), stopwords))
requisite_data["必須条件"] = requisite_data["必須条件"].apply(lambda x: preprocess_text(str(x), stopwords))
welcome_data["歓迎条件"] = welcome_data["歓迎条件"].apply(lambda x: preprocess_text(str(x), stopwords))
character_data["求める人物像"] = character_data["求める人物像"].apply(lambda x: preprocess_text(str(x), stopwords))

# "processed_仕事内容" 列のみを新しいCSVファイルに保存
job_data[["仕事内容"]].to_csv("processed_job_data.csv", index=False, encoding="utf-8")
requisite_data[["必須条件"]].to_csv("processed_requite_data.csv", index=False, encoding="utf-8")
welcome_data[["歓迎条件"]].to_csv("processed_welcome_data.csv", index=False, encoding="utf-8")
character_data[["求める人物像"]].to_csv("processed_character_data.csv", index=False, encoding="utf-8")
