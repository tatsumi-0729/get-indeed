from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class GetPopularity:

    """
    indeedのスクレイピングを行う。
    """

    def get(self):

        option = webdriver.ChromeOptions()
        option.add_argument('--headless')
        driver = webdriver.Chrome(options=option)
        # 暗黙的待機
        driver.implicitly_wait(10)
        driver.get('https://www.google.com/')

        # indeedをクロームで検索
        search_box = driver.find_element_by_name("q")
        search_box.send_keys("indeed")
        search_box.submit()

        # indeedのサイトにアクセス
        driver.find_element_by_css_selector('h3.LC20lb.DKV0Md').click()

        # 勤務地を入力
        work_place_box = driver.find_element_by_name("l")
        work_place_box.send_keys("東京都")

        # 検索したい言語dictを作成
        languages = {"Java": 0, "C": 0, "Ruby": 0, "Python": 0, "JavaScript": 0,
                     "TypeScript": 0, "Go": 0, "Vue": 0, "React": 0, "AWS": 0}

        # 各言語の検索数を順番に取得
        for i, language in enumerate(languages):

            # 言語を入力
            key_word_box = driver.find_element_by_name("q")
            key_word_box.send_keys(language)

            # 検索ボタンをクリック
            if i == 0:
                driver.find_element_by_css_selector(
                    'button.icl-Button.icl-Button--primary.icl-Button--md.icl-WhatWhere-button').send_keys(Keys.ENTER)
            else:
                driver.find_element_by_css_selector(
                    'input.input_submit').send_keys(Keys.ENTER)

            # 求人件数を取得
            search_text = driver.find_element_by_id(
                'searchCountPages').text

            # 求人件数から数字部分のみを取得
            result = self.__char(search_text)
            languages[language] = int(result.replace(',', ''))

            # ページ遷移後のキーワード入力欄を取得
            after_key_word_box = driver.find_element_by_name("q")
            after_key_word_box.clear()

        driver.quit()

        for key, val in languages.items():
            print(f"'{key}'の求人件数は'{val}'件です。")

    """
    求人件数から数字部分のみ取得する。
    """

    def __char(self, search_text):

        result_text = ""
        flag = False

        for char in search_text:
            if char == " " and flag == True:
                break
            elif char == " ":
                flag = True
                continue
            elif flag == True:
                result_text += char

        return result_text
