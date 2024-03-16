# %% [code] {"execution":{"iopub.status.busy":"2024-03-15T14:04:42.681896Z","iopub.execute_input":"2024-03-15T14:04:42.682387Z","iopub.status.idle":"2024-03-15T14:06:38.086965Z","shell.execute_reply.started":"2024-03-15T14:04:42.682342Z","shell.execute_reply":"2024-03-15T14:06:38.085821Z"},"jupyter":{"outputs_hidden":false}}
#Update
!apt-get update -y

#Installing the libraries used in this notebook
!apt-get install -y \
libglib2.0-0 \
libnss3 \
libdbus-glib-1-2 \
libgconf-2-4 \
libfontconfig1 \
gconf2-common \
libwayland-server0 \
libgbm1 \
udev \
libu2f-udev \
libjsoncpp25 \
libxnvctrl0

#Fix any broken dependencies that might occur during the installation process
!sudo apt --fix-broken install -y

#Install google chrome
!wget -nc -P /usr/lib https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
!dpkg -i /usr/lib/google-chrome-stable_current_amd64.deb

import subprocess
chrome_version = subprocess.check_output(["dpkg-query", "--show", "--showformat='${Version}'", "google-chrome-stable"]).decode("utf-8").strip("''").split("-")[0]
chrome_version

#Install chromedriver (Chrome driver version was manually inserted == 120.0.6099.109)
!wget -nc -P /usr/lib "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/121.0.6167.85/linux64/chromedriver-linux64.zip"
    
#Create new directory named "Chrome-browser"
!mkdir /usr/lib/chrome-browser

#Unzip chromedriver_linux64.zip and extracts its contents to "/usr/lib/chrome-browser/" directory
!unzip -o /usr/lib/chromedriver-linux64.zip -d /usr/lib/chrome-browser/

#Fix any broken dependencies that might occur during the installation process
!sudo apt --fix-broken install -y

#Install undetected chromedriver
!pip3 install undetected-chromedriver

#Install Packages
!pip3 install selenium\
selenium-wire\
selenium_authenticated_proxy\
selenium_stealth\
gspread\
gspread_dataframe

from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import InvalidSelectorException
from selenium.webdriver.common.keys import Keys
from selenium_stealth import stealth
from selenium_authenticated_proxy import SeleniumAuthenticatedProxy
from selenium.webdriver.support.ui import Select
import random
import undetected_chromedriver as uc
import re
import pandas as pd
from PIL import Image
import sys
import numpy as np
import time
from io import BytesIO
import datetime
import os
import requests
from tqdm.auto import tqdm
from kaggle_secrets import UserSecretsClient
from oauth2client.service_account import ServiceAccountCredentials
import json
import gspread
import math
from gspread_dataframe import set_with_dataframe
sys.path.insert(0,'/usr/lib/chrome-browser/chromedriver')
pd.set_option('display.max_columns', None)
pd.set_option('display.precision', 4)

# %% [code] {"execution":{"iopub.status.busy":"2024-03-15T14:06:38.089712Z","iopub.execute_input":"2024-03-15T14:06:38.090581Z","iopub.status.idle":"2024-03-15T14:06:38.102669Z","shell.execute_reply.started":"2024-03-15T14:06:38.090536Z","shell.execute_reply":"2024-03-15T14:06:38.101155Z"},"jupyter":{"outputs_hidden":false}}
def timestamp(date_value):
    # Define the mapping of month names to their numerical equivalents in Indonesian
    month_mapping = {
        'Januari': '01',
        'Februari': '02',
        'Maret': '03',
        'April': '04',
        'Mei': '05',
        'Juni': '06',
        'Juli': '07',
        'Agustus': '08',
        'September': '09',
        'Oktober': '10',
        'November': '11',
        'Desember': '12'
    }

    # Split the date value into components
    try:
        day, month_name, year, time = date_value.split()
        month_number = month_mapping.get(month_name)
    except:
        first_part, time = date_value.split()
        year, month_number, day = first_part.split('-')

    # Format the date
    formatted_date = f"{year}-{month_number}-{day} {time}"

    # Convert the formatted date string to datetime
    formatted_datetime = pd.to_datetime(formatted_date, format="%Y-%m-%d %H:%M:%S")

    return formatted_datetime

def send_messages(text):
    url = "https://gate.whapi.cloud/messages/text"

    payload = {
        "typing_time": 0,
        "to": "120363263203377737@g.us",
        "body": text
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer rQvLvlThc7outCPAEot0PVj5AYpm1xuA"
    }

    response = requests.post(url, json=payload, headers=headers)

# %% [code] {"execution":{"iopub.status.busy":"2024-03-15T14:06:38.104444Z","iopub.execute_input":"2024-03-15T14:06:38.104933Z","iopub.status.idle":"2024-03-15T14:06:52.662109Z","shell.execute_reply.started":"2024-03-15T14:06:38.104887Z","shell.execute_reply":"2024-03-15T14:06:52.660920Z"},"jupyter":{"outputs_hidden":false}}
#Initialize Webdriver w/ Proxies
proxies = requests.get(UserSecretsClient().get_secret("Proxy_List_Link_4").replace('"',""))

proxies_text = proxies.text
proxies_list = [proxy.split(':') for proxy in proxies_text.split('\r\n') if proxy]
        
selected_proxy = random.choice(proxies_list)
proxy_url = f"http://{selected_proxy[2]}:{selected_proxy[3]}@{selected_proxy[0]}:{selected_proxy[1]}"

#Create Connection
options = uc.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')                             
options.add_argument('--disable-dev-shm-usage')
options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36')
options.add_argument("--window-size=1920,1080")
proxy_helper = SeleniumAuthenticatedProxy(proxy_url)
proxy_helper.enrich_chrome_options(options)

driver = uc.Chrome(use_subprocess=True,options=options)

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

url = "https://www.idx.co.id/id/perusahaan-tercatat/keterbukaan-informasi/"
driver.get(url)

time.sleep(3) #Wait 3 seconds for the website to display perfectly so we can get a screenshot in the next code
  
#Take a screenshot of the website and display it.
Image.open(BytesIO(driver.get_screenshot_as_png()))

# %% [code] {"execution":{"iopub.status.busy":"2024-03-15T15:16:03.872360Z","iopub.execute_input":"2024-03-15T15:16:03.872945Z","iopub.status.idle":"2024-03-15T15:16:04.542175Z","shell.execute_reply.started":"2024-03-15T15:16:03.872908Z","shell.execute_reply":"2024-03-15T15:16:04.540812Z"},"jupyter":{"outputs_hidden":false}}
refresh_data = False

if not refresh_data:
    dataset = pd.read_csv("/kaggle/input/keterbukaan-informasi-idx/Keterbukaan Informasi.csv")
    dataset['Date'].apply(timestamp)

# %% [code] {"execution":{"iopub.status.busy":"2024-03-15T14:11:02.961799Z","iopub.execute_input":"2024-03-15T14:11:02.963115Z","iopub.status.idle":"2024-03-15T14:11:26.959879Z","shell.execute_reply.started":"2024-03-15T14:11:02.963031Z","shell.execute_reply":"2024-03-15T14:11:26.958915Z"},"jupyter":{"outputs_hidden":false}}
keylist = ["Date","Title","Link"]
database = {key: [] for key in keylist}

timeout=60
break_switch=False

proxies = requests.get(UserSecretsClient().get_secret("Proxy_List_Link_4").replace('"',""))

proxies_text = proxies.text
proxies_list = [proxy.split(':') for proxy in proxies_text.split('\r\n') if proxy]

attempt=1
max_attempt=20
resume_prompt = False
i = None
trash = 0

with tqdm(desc="Information Collected (on Process: ...)", unit=" items") as progress:
    while attempt<=max_attempt and trash<=30:

        #Initialize Webdriver w/ Proxies
        selected_proxy = random.choice(proxies_list)
        proxy_url = f"http://{selected_proxy[2]}:{selected_proxy[3]}@{selected_proxy[0]}:{selected_proxy[1]}"

        #Create Connection
        options = uc.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')                             
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36')
        options.add_argument("--window-size=1920,1080")
        proxy_helper = SeleniumAuthenticatedProxy(proxy_url)
        proxy_helper.enrich_chrome_options(options)

        driver = uc.Chrome(use_subprocess=True,options=options)

        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

        url = "https://www.idx.co.id/id/perusahaan-tercatat/keterbukaan-informasi/"
        
        try:    
            driver.get(url)
            WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH,"//*[@id='app']/div[2]/main/div/div/div[2]/span/ul/li[5]/button")))

            next_button = driver.find_element(By.XPATH, "//*[@id='app']/div[2]/main/div/div/div[2]/span/ul/li[5]/button")
            driver.execute_script("arguments[0].scrollIntoView();", next_button)

            while trash<=30:
                WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH,"//*[@id='app']/div[2]/main/div/div/div[2]/div[2]/div/div[1]")))
                WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH,"//*[@id='app']/div[2]/main/div/div/div[2]/span/ul/li[1]/select")))

                if resume_prompt:
                    dropdown = driver.find_element(By.XPATH, "//*[@id='app']/div[2]/main/div/div/div[2]/span/ul/li[1]/select")
                    Select(dropdown).select_by_value(page)
                    resume_prompt=False

                page = driver.find_element(By.XPATH, "//*[@id='app']/div[2]/main/div/div/div[2]/span/ul/li[1]/select").get_attribute("value")
                for i in range(10):
                    counter=0
                    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH,"//*[@id='app']/div[2]/main/div/div/div[2]/div[2]/div/div[1]")))

                    date_item = timestamp(driver.find_element(By.XPATH, f"//*[@id='app']/div[2]/main/div/div/div[2]/div[2]/div/div[{i+1}]").text.split("\n")[0])
                    title_item = driver.find_element(By.XPATH, f"//*[@id='app']/div[2]/main/div/div/div[2]/div[2]/div/div[{i+1}]/h6/a").text
                    link_item = driver.find_element(By.XPATH, f"//*[@id='app']/div[2]/main/div/div/div[2]/div[2]/div/div[{i+1}]/h6/a").get_attribute('href')
                    progress.set_description(f"Information Collected (on Process: {date_item}). Page {page}")
                    for key,new_value in zip(database.keys(), [date_item, title_item, link_item]):
                        if refresh_data:
                            if date_item < pd.to_datetime('2024-03-01 00:00:00',format='%Y-%m-%d %H:%M:%S'):
                                trash+=1
                                continue
                        else:
                            if date_item < pd.to_datetime(dataset.iloc[0].iloc[0],format='%Y-%m-%d %H:%M:%S'): #ganti tanggalnya
                                trash+=1
                                continue
                        database[key].append(new_value)
                        counter+=(1/3)
                        progress.update(math.floor(counter))

                    if break_switch:
                        break    

                if break_switch:
                    break

                next_button.click()

            if break_switch:
                break
                
        except:
            print(f"Timeout. Attempt {attempt+1}...")
            attempt+=1
            driver.quit()
            resume_prompt=True
            continue

# %% [code] {"execution":{"iopub.status.busy":"2024-03-15T14:12:00.239157Z","iopub.execute_input":"2024-03-15T14:12:00.239651Z","iopub.status.idle":"2024-03-15T14:12:00.259317Z","shell.execute_reply.started":"2024-03-15T14:12:00.239615Z","shell.execute_reply":"2024-03-15T14:12:00.257452Z"},"jupyter":{"outputs_hidden":false}}
table = pd.DataFrame.from_dict(database); table

# %% [code] {"execution":{"iopub.status.busy":"2024-03-15T14:54:30.611460Z","iopub.execute_input":"2024-03-15T14:54:30.611893Z","iopub.status.idle":"2024-03-15T14:54:30.628495Z","shell.execute_reply.started":"2024-03-15T14:54:30.611862Z","shell.execute_reply":"2024-03-15T14:54:30.627147Z"},"jupyter":{"outputs_hidden":false}}
keywords = ['HMETD',
            'PMTHMETD',
            'Penyampaian Informasi',
            'Transaksi Material',
            'Pengumuman RUPS',
            'Pengumuman Rapat Umum Pemegang Saham',
            'Buyback',
            'Pembelian Kembali',
            'Restrukturisasi Utang',
            'Daftar Efek Bersifat Ekuitas Dalam Pemantauan Khusus',
            'Penambahan Modal',
            'Transaksi Afiliasi']

def check_keywords(text, keywords):
    for keyword in keywords:
        if keyword in text:
            return True
    return False

filtered_table = table[table['Title'].apply(lambda x: check_keywords(x, keywords))]; filtered_table

# %% [code] {"execution":{"iopub.status.busy":"2024-03-15T15:02:52.844417Z","iopub.execute_input":"2024-03-15T15:02:52.844932Z","iopub.status.idle":"2024-03-15T15:02:54.207800Z","shell.execute_reply.started":"2024-03-15T15:02:52.844894Z","shell.execute_reply":"2024-03-15T15:02:54.206798Z"},"jupyter":{"outputs_hidden":false}}
for row in filtered_table.itertuples():
    send_messages(f"""
Tanggal: {row[1]}\n\nJudul: {row[2]}\n\nLink: {row[3]}
""")

# %% [code] {"execution":{"iopub.status.busy":"2024-03-15T15:18:33.168917Z","iopub.execute_input":"2024-03-15T15:18:33.169385Z","iopub.status.idle":"2024-03-15T15:18:33.185762Z","shell.execute_reply.started":"2024-03-15T15:18:33.169352Z","shell.execute_reply":"2024-03-15T15:18:33.184820Z"},"jupyter":{"outputs_hidden":false}}
if not refresh_data:
    table = pd.concat([table[:-1], dataset], ignore_index=True)    
table

# %% [code] {"execution":{"iopub.status.busy":"2024-03-15T05:06:37.296911Z","iopub.execute_input":"2024-03-15T05:06:37.297254Z","iopub.status.idle":"2024-03-15T05:06:37.313249Z","shell.execute_reply.started":"2024-03-15T05:06:37.297227Z","shell.execute_reply":"2024-03-15T05:06:37.311876Z"},"jupyter":{"outputs_hidden":false}}
#Save DataFrame to excel
table.to_csv("Keterbukaan Informasi.csv",
             date_format='%Y-%m-%d %H:%M:%S',
             index=False)

# %% [code] {"execution":{"iopub.status.busy":"2024-03-15T05:06:37.314825Z","iopub.execute_input":"2024-03-15T05:06:37.315169Z","iopub.status.idle":"2024-03-15T05:06:40.114027Z","shell.execute_reply.started":"2024-03-15T05:06:37.315141Z","shell.execute_reply":"2024-03-15T05:06:40.112837Z"},"jupyter":{"outputs_hidden":false}}
#Save DataFrame to Google Spreadsheets
credential = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(UserSecretsClient().get_secret("mycredential")))
gc = gspread.authorize(credential)

spreadsheet = gc.open_by_url(UserSecretsClient().get_secret("spreadsheet_link"))
set_with_dataframe(spreadsheet.worksheet('Keterbukaan Informasi'), table)
