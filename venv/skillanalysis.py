import pandas as pd
from collections import Counter
import os
import openai
import json

csv_files = {
    "仕事内容": ("processed_csv/processed_job_data.csv", "仕事内容"),
    "必須スキル": ("processed_csv/processed_requite_data.csv", "必須条件"),
    "歓迎スキル": ("processed_csv/processed_welcome_data.csv", "歓迎条件"),
    "求める人物像": ("processed_csv/processed_character_data.csv", "求める人物像")
}

word_counts_per_file = {}

for name, file_info in csv_files.items():
    file, column = file_info  # 明示的に分割してタプルではなく、個別の変数として扱う
    if isinstance(file, str) and os.path.exists(file):  # ファイル名が文字列か確認
        try:
            df = pd.read_csv(file, encoding="utf-8")
            print(f"{file} のカラム: {df.columns}")  # カラム名を表示
            if column in df.columns:
                texts = df[column].dropna().tolist()
                word_counts = Counter(" ".join(texts).split())
                word_counts_per_file[name] = word_counts.most_common(30)
            else:
                print(f"'{file}' に '{column}' カラムが見つかりません")
        except Exception as e:
            print(f" {file} の読み込みエラー: {e}")
    else:
        print(f"ファイルが見つかりません、または無効なファイル名: {file}")


# ファイルごとの頻出単語を表示（トップ15）
for name, word_counts in word_counts_per_file.items():
    print(f"\n {name} の単語頻度トップ15")  
    for word, count in word_counts:  
        print(f"{word}: {count}")

word_counts_per_file = {}
all_words = []  # すべてのファイルの単語を統合するリスト

for name, file_info in csv_files.items():
    file, column = file_info  
    if isinstance(file, str) and os.path.exists(file):  
        try:
            df = pd.read_csv(file, encoding="utf-8")
            if column in df.columns:
                texts = df[column].dropna().tolist()
                words = " ".join(texts).split()
                word_counts_per_file[name] = Counter(words).most_common(0)
                all_words.extend(words)  # 全体統計用リストに追加
            else:
                print(f"'{file}' に '{column}' カラムが見つかりません")
        except Exception as e:
            print(f" {file} の読み込みエラー: {e}")
    else:
        print(f"ファイルが見つかりません、または無効なファイル名: {file}")

# 全ファイル統計を計算
total_word_counts = Counter(all_words).most_common(100)

# 全ファイル統計を表示（トップ15）
print("\n全ファイル統合の単語頻度トップ15")  
for word, count in total_word_counts[:100]:  
    print(f"{word}: {count}")

# #  言葉の分類

# # サンプルの単語リスト
# sentences = [
#     ["機械学習", "深層学習", "AI", "データ", "開発", "設計", "Python", "LLM","deep learning"],
#     ["法人営業", "コンサル", "提案", "マネジメント", "運用", "プロジェクト"],
#     ["コミュニケーション", "積極", "チーム", "主体", "成長", "意欲"]
# ]

# # Word2Vecモデルを学習
# model = Word2Vec(sentences, vector_size=100, window=5, min_count=1, sg=0)

# # 単語リストを取得
# words = list(model.wv.index_to_key)
# vectors = [model.wv[word] for word in words]

# # KMeansクラスタリング（3つのクラスタに分割）
# num_clusters = 3
# kmeans = KMeans(n_clusters=num_clusters, random_state=0)
# kmeans.fit(vectors)

# # クラスタごとの単語を表示
# clusters = {i: [] for i in range(num_clusters)}
# for word, label in zip(words, kmeans.labels_):
#     clusters[label].append(word)

# print(clusters)


# # OpenAIで統計結果を入れ考察

# openai.api_key = "YOUR_API_KEY"  # ここにOpenAIのAPIキーを設定

# def analyze_text_with_gpt(text):
#     response = openai.ChatCompletion.create(          
#         model="gpt-4",
#         messages=[{"role": "system", "content": "以下の単語頻度データを分析し、傾向を考察してください。"},
#                   {"role": "user", "content": text}]
#     )
#     return response["choices"][0]["message"]["content"]

# # 統計データをJSON形式で変換
# data_to_analyze = json.dumps(total_word_counts, ensure_ascii=False, indent=2)

# # GPTに分析依頼
# result = analyze_text_with_gpt(data_to_analyze)
# print(result)