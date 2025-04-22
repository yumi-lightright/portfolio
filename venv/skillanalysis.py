import pandas as pd
from collections import Counter
import os

csv_files = {
    "job_data": ("processed_job_data.csv", "仕事内容"),
    "requisite_data": ("processed_requite_data.csv", "必須条件"),
    "welcome_data": ("processed_welcome_data.csv", "歓迎条件"),
    "character_data": ("processed_character_data.csv", "求める人物像")
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
                word_counts_per_file[name] = Counter(words).most_common(30)
                all_words.extend(words)  # 全体統計用リストに追加
            else:
                print(f"'{file}' に '{column}' カラムが見つかりません")
        except Exception as e:
            print(f" {file} の読み込みエラー: {e}")
    else:
        print(f"ファイルが見つかりません、または無効なファイル名: {file}")

# 全ファイル統計を計算
total_word_counts = Counter(all_words).most_common(30)

# 全ファイル統計を表示（トップ15）
print("\n全ファイル統合の単語頻度トップ15")  
for word, count in total_word_counts[:35]:  
    print(f"{word}: {count}")

