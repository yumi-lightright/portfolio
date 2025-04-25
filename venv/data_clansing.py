import pandas as pd
import re
import csv
import sudachipy
from sudachipy import Dictionary

# CSVファイルのパスを管理
file_paths = {
    "skills_data": "csv/skills_and_experience.csv",
    "job_data": "csv/job_discription.csv",
    "requisite_data": "csv/必須条件.csv",
    "welcome_data": "csv/歓迎条件.csv",
    "character_data": "csv/求める人物像.csv",
}

# 必須・歓迎・人物像のキーワード定義
keywords = {
    "必須条件": ["必須", "MUST", "必須要件", "必須スキル", "必要なスキル", "必須要件(以下のいずれか)", "応募要件"],
    "歓迎条件": ["歓迎", "WANT", "歓迎要件", "歓迎スキル", "望ましい経験／能力", "尚可要件"],
    "求める人物像": ["求める人物像", "特徴", "求める人物タイプ"]
}

# Sudachiの設定
tokenizer_obj = Dictionary().create()
mode = sudachipy.SplitMode.C  # Cモードで意味単位の分割

# フレーズ辞書
phrase_list = ["機械学習", "深層学習", "要件定義", "自然言語処理", "企画提案", "業務改善", "web開発",
               "基本情報技術者", "応用情報技術者", "基本設計", "詳細設計", "scikit learn",
               "ディープラーニング", "統計学", "画像処理", "音声処理", "開発経験", "データ処理", "データ分析",
               "意見交換", "新しい技術", "データ解析", "社会貢献", "受託開発", "産業機械"
               "情報提供","画像解析","モデル評価","モデル設計","学習モデル","パイプライン構築","モデル構築",
               "パートナー連携","チャットエンジン","医療問題","業務効率化","受託業務","新規開発","開発支援"
               "データソリューション","技術調査","既存開発","進捗管理","技術開発","データサイエンス","モデル生成"
               "最新技術","自動運転","画像認識処理 ","開発現場","営業経験","スキルアップ","営業経験","営業経験","営業経験"
               "得意分野","エッジデバイス","成長分野","技術研究","生成ai","画像生成","最新テクノロジー"]

# ストップワード設定
stopwords = set([
    "の", "と", "して", "は", "ます", "です", "など", "する", "ある", "いる", "こと", "これ", "それ", "あれ",
    "この", "その", "ため", "対し", "まで", "いう", "できる", "から", "のみ", "なく", "ところ", "しか", "いずれ",
    "用い", "プロジェクト", "スキル", "サービス", "持っ", "おり", "以上", "利用", "システム", "アプリケーション",
    "また", "案件", "クライアント", "must", "エンジニア", "内容", "プロダクト", "向け", "アプリ", "仕事", "事業",
    "条件", "使用", "顧客", "いただき", "でき", "関する", "会社", "企業", "知識", "知見", "担当", "ながら", "可能",
    "メンバー", "使っ", "おけ", "よる", "好き", "活用", "行い", "自社", "当社", "領域", "不問", "高い", "社内",
    "もしくは", "作成", "関連", "行える", "取り組める", "自己", "持つ", "歓迎", "必須要件", "必須条件",
    "業務内容", "仕事内容", "概要", "具体的には", "プロジェクト例", "の知識", "必須スキル", "必須経験","たい",
    "必須スキル・経験", "目安", "の利用経験", "いずれか必須", "歓迎要件", "求める","人物像", "want","分野",
    "構築", "および", "あり", "行っ", "なり", "ない", "よう", "組織", "お任せ", "必要", "ませ", "言語",
    "含む","いただける","られる","より","いく","つい","持ち","いき","こんな","含む","おい","お客様"
    "進め", "行う", "世の中", "必須", "要件", "経験", 
])


# テキスト分類関数
def classify_lines(text):
    if pd.isna(text) or not isinstance(text, str) or not text.strip():
        return "", "", ""

    categorized_texts = {"必須条件": [], "歓迎条件": [], "求める人物像": []}
    current_category = None

    for line in text.split('\n'):
        for category, kw_list in keywords.items():
            if any(keyword in line for keyword in kw_list):
                current_category = category
                categorized_texts[current_category].append(line)
                break

        if current_category:
            categorized_texts[current_category].append(line)

    return (
        '\n'.join(categorized_texts["必須条件"]),
        '\n'.join(categorized_texts["歓迎条件"]),
        '\n'.join(categorized_texts["求める人物像"]),
    )

# CSVファイルの読み込みと分類
with open(file_paths["skills_data"], newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)

    categorized_files = {
        "必須条件": open(file_paths["requisite_data"], 'w', newline='', encoding='utf-8'),
        "歓迎条件": open(file_paths["welcome_data"], 'w', newline='', encoding='utf-8'),
        "求める人物像": open(file_paths["character_data"], 'w', newline='', encoding='utf-8')
    }

    writers = {key: csv.writer(file) for key, file in categorized_files.items()}
    
    for key in writers:
        writers[key].writerow([key])

    for row in reader:
        必須条件, 歓迎条件, 求める人物像 = classify_lines(row.get('必要なスキル・経験', ''))

        if 必須条件:
            writers["必須条件"].writerow([必須条件])
        if 歓迎条件:
            writers["歓迎条件"].writerow([歓迎条件])
        if 求める人物像:
            writers["求める人物像"].writerow([求める人物像])

    for file in categorized_files.values():
        file.close()

# データフレームを読み込み
data_frames = {name: pd.read_csv(path).fillna("") for name, path in file_paths.items() if name != "skills_data"}

# テキスト前処理関数
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff]", " ", text).strip()
    tokens = [m.surface() for m in tokenizer_obj.tokenize(text, mode) if m.surface() not in ["・", "\n"]]

    new_tokens = []
    i = 0
    while i < len(tokens):
        matched = False
        for phrase in phrase_list:
            phrase_parts = [m.surface() for m in tokenizer_obj.tokenize(phrase, mode)]
            phrase_length = len(phrase_parts)

            if tokens[i:i+phrase_length] == phrase_parts:
                new_tokens.append(phrase)
                i += phrase_length
                matched = True
                break

        if not matched:
            new_tokens.append(tokens[i])
            i += 1

    filtered_tokens = [word for word in new_tokens if word not in stopwords and len(word) > 1]
    return " ".join(filtered_tokens)

# 各データフレームに前処理を適用
for key in ["job_data", "requisite_data", "welcome_data", "character_data"]:
    data_frames[key].iloc[:, 0] = data_frames[key].iloc[:, 0].apply(preprocess_text)

# CSVへ保存
for key in data_frames:
    data_frames[key].to_csv(f"processed_csv/processed_{key}.csv", index=False, encoding="utf-8")