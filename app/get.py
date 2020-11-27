from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import matplotlib.pyplot as plt


class GetPopularity:

    """
    indeedのスクレイピングを行う。
    """

    def get(self):

        # docker内で起動するためのoptionを作成
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)
        # 暗黙的待機
        driver.implicitly_wait(10)
        driver.get('https://jp.indeed.com/')

        # 勤務地を入力
        work_place_box = driver.find_element_by_name("l")
        work_place_box.send_keys("東京都")

        # 検索したい言語リストを作成
        targets = {"C": 0, "Java": 0, "Ruby": 0, "Python": 0, "JavaScript": 0,
                   "Go": 0, "Vue": 0, "React": 0, "TypeScript": 0, "AWS": 0, }

        # 各言語の検索数を順番に取得
        for i, target in enumerate(targets):

            # 言語を入力
            key_word_box = driver.find_element_by_name("q")
            key_word_box.send_keys(target)

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
            targets[target] = int(result.replace(',', ''))

            # ページ遷移後のキーワード入力欄を取得
            after_key_word_box = driver.find_element_by_name("q")
            after_key_word_box.clear()

        driver.quit()

        # valueの昇順で並び替え
        sorted_targets = sorted(targets.items(), key=lambda x: x[1])

        target_keys = []
        target_vals = []

        for target in sorted_targets:
            target_keys.append(target[0])
            target_vals.append(target[1])

        # 求人件数順のグラフを作成
        self.__make_graph(target_keys, target_vals)

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

    """
    求人件数順のグラフを作成する
    """

    def __make_graph(self, target_keys, target_vals):

        plt.bar(target_keys, target_vals)
        plt.title("ranking of programing languages 2020")
        plt.xlabel("programing languages")
        plt.ylabel("the number of jobs available")
        plt.show()
