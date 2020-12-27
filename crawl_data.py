from datetime import date
from selenium import webdriver
import time
import pandas as pd
import numpy as np

today = date.today()
print("Today's date:", today)

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
driver = webdriver.Chrome("./chromedriver", options=options)

# target url for the covid19 data: Seoul City
url = "http://www.seoul.go.kr/coronaV/coronaStatus.do"
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
df.to_csv(file_path, index=False)
