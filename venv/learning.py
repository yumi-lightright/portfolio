from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

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
        password_input.send_keys("kiyoko09")  # パスワードを入力

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
        search_field.send_keys("python フルリモート")
        print("検索ワードを入力しました！")

        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "header-search-form-v2--submit-button"))
        )
        submit_button.click()
        print("検索ボタンをクリックしました！")
    except Exception as e:
        print(f"検索処理中にエラーが発生しました: {e}")

    # リンク収集
    try:
        href_list = []  # リンクリストを初期化
        link_elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/company/')]")
        for element in link_elements:
            href_value = element.get_attribute("href")
            if href_value:  # 有効なリンクのみ追加
                href_list.append(href_value)
        print("リンクリストを収集しました！")
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

            skills_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".MuiTypography-root.MuiTypography-body2"))
            )
            skills_description = skills_element.text

            data_to_save.append([href_value, job_description, skills_description])
        except Exception as e:
            print(f"情報抽出中にエラーが発生しました: {e}")

    # CSVファイルに保存
    try:
        with open("job_data.csv", "w", newline="", encoding="utf-8") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["リンク", "仕事内容", "必要なスキル・経験"])
            csvwriter.writerows(data_to_save)
        print("データをCSVファイルに保存しました！")
    except Exception as e:
        print(f"CSVファイル保存中にエラーが発生しました: {e}")

finally:
    driver.quit()
    print("ブラウザを終了しました！")