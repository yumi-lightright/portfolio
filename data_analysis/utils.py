import requests
from bs4 import BeautifulSoup

def fetch_html(url, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # HTTPステータスコードが200以外の場合は例外を発生
        return BeautifulSoup(response.content, "html.parser")
    except requests.exceptions.RequestException as e:
        print(f"リクエストエラー: {e}")
        return None

def extract_data(soup, tag, class_name):
    try:
        elements = soup.find_all(tag, {'class': class_name})
        if not elements:
            raise Exception(f"指定したクラス'{class_name}'のデータが見つかりませんでした。HTML構造を確認してください。")
        return [element.text for element in elements]
    except Exception as e:
        print(f"データ抽出エラー: {e}")
        return []

def main():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    
    # 最初のURLでデータを抽出
    url1 = "https://freelance-start.com/jobs/skill-3?utm_source=google&utm_medium=cpc&utm_campaign=google_cpc_03-Skill_03-Skill-01-ProgrammingLanguage_20240606&utm_term=b_python%20%E3%82%A8%E3%83%B3%E3%82%B8%E3%83%8B%E3%82%A2%20%E6%B1%82%E4%BA%BA&RefID=google_cpc_03-Skill_03-Skill-01-ProgrammingLanguage_20240606_b_python%20%E3%82%A8%E3%83%B3%E3%82%B8%E3%83%8B%E3%82%A2%20%E6%B1%82%E4%BA%BA&gad_source=1&gclid=Cj0KCQjwzYLABhD4ARIsALySuCTrSZ6ZjD8gOS-p3wAywZB-_i6OzXrCDoSE0MeDZqH7IJ9Sx4VCZccaAtjtEALw_wcB"
    soup1 = fetch_html(url1, headers)
    if soup1:
        job_details = extract_data(soup1, 'p', 'text-break-all fs-14')
        print("ジョブ詳細:")
        for job in job_details:
            print(job)

    # 次のURLでデータを抽出
    url2 = "https://jp.indeed.com/jobs?q=python+%E3%83%95%E3%83%AB%E3%83%AA%E3%83%A2%E3%83%BC%E3%83%88&l=&from=searchOnDesktopSerp&vjk=aead0b930e4cf37a&advn=2245789821892914"
    soup2 = fetch_html(url2, headers)
    if soup2:
        skills = extract_data(soup2, 'button', 'btn btn-sm btn-outline-light-green-gray border-w-1 fs-12 text-dark font-weight-light py-1 px-2')
        print("\nスキル:")
        for skill in skills:
            print(skill)

if __name__ == "__main__":
    main()