import requests
from bs4 import BeautifulSoup

def fetch_list_page(url, headers=None):
    """
    一覧ページからリンクを取得する関数
    """
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # ステータスコードを確認
        soup = BeautifulSoup(response.text, 'html.parser')

        # 一覧ページのリンクを収集
        links = [link['href'] for link in soup.find_all('a', class_='p-search-job-media__title c-media__title')]
        base_url = "https://www.lancers.jp"
        full_links = [base_url + link for link in links]  # 完全なURLを生成
        return full_links
    except requests.exceptions.RequestException as e:
        print(f"Error fetching list page: {e}")
        return None

def fetch_detail_page(url, headers=None):
    """
    詳細ページから情報を取得する関数
    """
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # タイトルと <dd class="c-definition-list__description"> の内容を取得
        title = soup.find('h1', class_='c-heading')
        description_section = soup.find('dd', class_='c-definition-list__description')
        description = description_section.decode_contents().strip() if description_section else "No description found"

        return {
            'title': title.text.strip() if title else "No title found",
            'description': description  # HTML構造を保持して抽出
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching detail page {url}: {e}")
        return None

if __name__ == "__main__":
    # 一覧ページのURL
    list_page_url = "https://www.lancers.jp/work/search?keyword=Python&ref=header_search&searchType=recommend&sort=client&work_rank%5B0%5D=2&work_rank%5B1%5D=3&work_rank%5B2%5D=0&show_description=1&page=2"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # 一覧ページからリンクを取得
    links = fetch_list_page(list_page_url, headers=headers)
    if links:
        print(f"Found {len(links)} links:")
        for link in links:
            print(link)

        # 各詳細ページの情報を取得
        for link in links:
            details = fetch_detail_page(link, headers=headers)
            print(f"Details for {link}:")
            print(details)
    else:
        print("No links found on the list page.")