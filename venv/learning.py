from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

# Chromeドライバのセットアップ
driver = webdriver.Chrome()

try:
    # サイトのログインページにアクセス
    driver.get("https://www.green-japan.com/login")

    # ログイン処理
    try:
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "user[mail]"))
        )
        email_input.send_keys("yt08301192@icloud.com")  # メールアドレスを入力

        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "user[password]"))
        )
        password_input.send_keys("Q8FxAv3fLVSN7a")  # パスワードを入力

        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "commit"))
        )
        login_button.click()
        print("ログイン成功！")
    except Exception as e:
        print(f"ログイン時にエラーが発生しました: {e}")

    # ポップアップクローズ処理
    try:
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "user-motivation-submit-button"))
        )
        submit_button.click()
        print("サブミットボタンをクリックしました！")
    except Exception as e:
        print(f"サブミットボタンをクリックする際にエラーが発生しました: {e}")

    # 検索処理
    try:
        search_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "user_search[keyword]"))
        )
        search_field.clear()
        search_field.send_keys("AI") # 検索ワードを入力
        print("検索ワードを入力しました！")

        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "header-search-form-v2--submit-button"))
        )
        submit_button.click()
        print("検索ボタンをクリックしました！")
    except Exception as e:
        print(f"検索処理中にエラーが発生しました: {e}")

    # 無限スクロール + リンク収集
    try:
        href_list = set()  # URLを格納するセット（重複排除）
        last_height = driver.execute_script("return document.body.scrollHeight")  # 現在のページ高さを取得

        while True:
            # スクロールを実行
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # ページの読み込みを待つ

            # ページ内のリンクを取得
            link_elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/company/')]")
            for element in link_elements:
                href_value = element.get_attribute("href")
                if href_value and href_value not in href_list:  # 新しいリンクのみ追加
                    href_list.add(href_value)

            # ページの高さを再度取得
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:  # 高さが変わらなければ終了
                break
            last_height = new_height

        print(f"リンク収集完了！取得したリンク数: {len(href_list)}")
    except Exception as e:
        print(f"リンク収集時にエラーが発生しました: {e}")

    # 各リンクから情報抽出
    data_to_save = []  # CSVに保存するデータリスト
    for href_value in href_list:
        try:
            driver.get(href_value)  # 各リンクにアクセス
            WebDriverWait(driver, 20).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            print(f"現在のページ: {driver.current_url}")

            job_description_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".MuiTypography-root.MuiTypography-body1"))
            )
            job_description = job_description_element.text

            skills_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(By.XPATH, 
              "//p[contains(@class, 'MuiTypography-body2') and ("
              "contains(., '必須') or contains(., '求める人物像') or contains(., '開発経験') or contains(., '歓迎条件') or "
              "contains(., '必要な資格') or contains(., '自然言語処理') or contains(., 'マネジメント経験') or contains(., '統計学') or "
              "contains(., '要件定義スキル') or contains(., '研究経験') or contains(., '求める人材') or contains(., 'システム開発を行った経験')"
         ")]"))


            skills_description = skills_element.text
            print(f"仕事内容: {skills_description}")

            data_to_save.append([href_value, job_description, skills_description])
        except Exception as e:
            print(f"情報抽出中にエラーが発生しました: {e}")

   # CSVファイルに分けて保存
    try:
        # リンクの保存
        with open("csv/links.csv", "w", newline="", encoding="utf-8") as link_file:
            link_writer = csv.writer(link_file)
            link_writer.writerow(["リンク"])  # ヘッダー行
            for row in data_to_save:
                link_writer.writerow([row[0]])  # リンク列のみ保存
        print("リンクデータを保存しました: links.csv")

        # 仕事内容の保存
        with open("csv/仕事内容.csv", "w", newline="", encoding="utf-8") as job_file:
            job_writer = csv.writer(job_file)
            job_writer.writerow(["仕事内容"])  # ヘッダー行
            for row in data_to_save:
                job_writer.writerow([row[1]])  # 仕事内容列のみ保存
        print("仕事内容データを保存しました: csv/仕事内容.csv")

        # 必要なスキル・経験の保存
        with open("csv/skills_and_experience.csv", "w", newline="", encoding="utf-8") as skill_file:
            skill_writer = csv.writer(skill_file)
            skill_writer.writerow(["必要なスキル・経験"])  # ヘッダー行
            for row in data_to_save:
                skill_writer.writerow([row[2]])  # 必要なスキル・経験列のみ保存
        print("必要なスキル・経験データを保存しました: skills_and_experience.csv")

    except Exception as e:
        print(f"CSVファイル保存中にエラーが発生しました: {e}")

finally:
    # ブラウザを閉じる
    driver.quit()
    print("ブラウザを閉じました。")