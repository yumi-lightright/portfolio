import pandas as pd
from collections import Counter
import os
import openai
import json
from dotenv import load_dotenv
import os


csv_files = {
    "仕事内容": ("processed_csv/processed_job_data.csv", "仕事内容"),
    "必須スキル": ("processed_csv/processed_requite_data.csv", "必須条件"),
    "歓迎スキル": ("processed_csv/processed_welcome_data.csv", "歓迎条件"),
    "求める人物像": ("processed_csv/processed_character_data.csv", "求める人物像")
}

word_counts_per_file = {}  # 各カテゴリの頻度データ
all_words = []  # 全ファイルの単語リスト


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
                all_words.extend(word_counts)  # 全体統計用リストに追加
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


# openaiの考察


load_dotenv()# .envファイルをロード
openai.api_key = os.getenv("OPENAI_API_KEY")# OpenAI APIキーを環境変数から取得
print(os.getenv("OPENAI_API_KEY"))  # 環境変数の中身を表示



def analyze_text_with_gpt(text):
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "120件の求人票の仕事内容、必須スキル、歓迎スキルと全体の合計の頻出ワードを取得したけど、仕事内容、必須スキル、歓迎スキル、全体の必須ワードごとの考察し、必要なスキルについて分析して欲しい"},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"OpenAI APIの呼び出しでエラーが発生しました: {e}"


# **GPTに渡すデータ構造**
data_to_analyze = json.dumps({
    "個別カテゴリー": word_counts_per_file,
    "全体統計": total_word_counts
}, ensure_ascii=False, indent=2)

# GPTに分析依頼
result = analyze_text_with_gpt(data_to_analyze)
print("\nGPTによる分析結果:")
print(result)
