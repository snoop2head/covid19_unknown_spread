"""
Copyright 2020 YoungjinAhn

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import platform
import os
import os.path as osp
from datetime import date
from selenium import webdriver
import time
import pandas as pd
import numpy as np


def detect_OS():
    """ 
    OS Detection and chromedriver allocation 
    Code Source: YoongiKim AutoCrawler
    """

    if platform.system() == "Windows":
        print("Detected OS : Windows")
        executable = "./chromedriver/chromedriver_win32.exe"
    elif platform.system() == "Linux":
        print("Detected OS : Linux")
        executable = "./chromedriver/chromedriver_linux64"
    elif platform.system() == "Darwin":
        print("Detected OS : Mac")
        executable = "./chromedriver/chromedriver_mac64"
    else:
        raise OSError("Unknown OS Type")

    if not osp.exists(executable):
        raise FileNotFoundError(
            "Chromedriver file should be placed at {}".format(executable)
        )
    return executable


def crawl_covid19_data(executable_chromedriver, url):
    # chrome driver options
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": "./dataset_created",
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        },
    )

    # set up driver
    driver = webdriver.Chrome(executable_chromedriver, options=options)

    # target url for the covid19 data: Seoul City
    driver.get(url)

    """ From the most recent patient ~ Patient number 10001 """
    # get the last page as index range
    button_last_page = driver.find_element_by_xpath(
        '//*[@id="DataTables_Table_0_paginate"]/span/a[6]'
    )
    str_last_index = button_last_page.text
    int_last_index = int(str_last_index)
    print(int_last_index)

    list_patient_data_total = []

    for num in range(int_last_index):
        list_patient_data_100 = []
        # get first page table
        tables = pd.read_html(driver.page_source)

        for table in tables:
            if "연번" in table:
                list_patient_data_100.append(table)

        print(list_patient_data_100[0])
        list_patient_data_total.append(list_patient_data_100[0])

        button_paginate_next = driver.find_element_by_xpath(
            '//*[@id="DataTables_Table_0_next"]'
        )
        button_paginate_next.click()
        time.sleep(1.5)

    df_now = pd.concat(list_patient_data_total, axis=0)
    print(df_now.head())
    print(df_now.tail())

    """ From patient number 10000 ~ Patient number 1 """
    # move to 1 to 10000 section
    patient_1_to_10000 = driver.find_element_by_css_selector(
        "#move-cont1 > div:nth-child(2) > div.tab-cont-wrap > div.new-tab > ul > li:nth-child(2) > button"
    )
    patient_1_to_10000.click()

    # get the last page as index range
    button_last_page_2 = driver.find_element_by_xpath(
        "/html/body/div[2]/div[2]/div[2]/div/div[9]/div[2]/div[3]/div[3]/div/div[2]/div[5]/span/a[6]"
    )
    str_last_index = button_last_page_2.text
    int_last_index = int(str_last_index)
    print(int_last_index)

    list_patient_data_total_10000 = []

    for num in range(int_last_index):
        list_patient_data_100 = []

        tables = pd.read_html(driver.page_source)
        for table in tables:
            if "연번" in table:
                list_patient_data_100.append(table)
        print(list_patient_data_100[-1])
        list_patient_data_total_10000.append(list_patient_data_100[-1])

        paginate_next_2 = driver.find_element_by_xpath(
            "/html/body/div[2]/div[2]/div[2]/div/div[9]/div[2]/div[3]/div[3]/div/div[2]/div[5]/a[2]"
        )
        paginate_next_2.click()
        time.sleep(1.5)

    df_10000 = pd.concat(list_patient_data_total_10000, axis=0)
    print(df_10000.head())
    print(df_10000.tail())

    """ Combine those two crawled dataframes """
    df = pd.concat([df_now, df_10000], axis=0)
    print(df.head())
    print(df.tail())

    # most upto-date data
    last_day = df["확진일"].iloc[0]
    last_day = last_day.replace(".", "_")
    print(last_day)

    # naming file and setting the path
    dataset_path = "./dataset/"
    file_name = f"seoul_covid_{last_day}.csv"
    file_path = dataset_path + file_name
    print(file_path)

    df = df.sort_values(["연번"], ascending=False)
    return df


def main():
    """ run functions defined above """

    # print date for today
    today = date.today()
    print("Today's date:", today)

    # detect OS
    chrome_driver = detect_OS()

    # run crawler twice to resolve data duplicate problem
    url = "http://www.seoul.go.kr/coronaV/coronaStatus.do"
    list_df = []
    for i in range(2):
        df_temp = crawl_covid19_data(chrome_driver, url)
        list_df.append(df_temp)

    # resolve duplicate problem
    df = pd.concat(list_df, axis=0)
    df = df.drop_duplicates()
    df = df.sort_values(["연번"], ascending=False)

    # check data shape and values
    print(df.shape)
    print(df.head())
    print(df.tail())

    # export data to csv file
    cwd = os.getcwd()
    file_name = "seoul_covid_" + str(today) + ".csv"
    file_path = cwd + "/dataset/" + file_name
    df.to_csv(file_path, index=False)


if __name__ == "__main__":
    main()
