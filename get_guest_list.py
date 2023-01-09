import requests
import json
import re
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


def get_lex_guests(URL, class_, save_path):
    page = requests.get(URL)
    html = page.content
    soup = BeautifulSoup(html, "html.parser")
    guest_list = soup.find_all('div', class_)
    guests = []

    for guest in guest_list:
        name = guest.text
        guests.append(name)


    with open(save_path, "w") as f:
        json.dump(guests, f)

    print(f'Saved {len(guests)} records into {save_path}')


def get_JRE_guests(save_path):
    # Download spreadshit as csf to you machine
    spreadsheet_url = "https://docs.google.com/spreadsheets/d/12iTobpwHViCIANFSX3Pc_dGMdfod-0w3I5P5QJL45L8/edit#gid=543723238"
    
    # Reading file into pandas dataframe
    file_path = 'data/JREdata.csv'
    df = pd.read_csv(file_path)

    # Saving guests to json file
    df_guests= df['Guest(s)']
    df_guests.to_json(save_path, orient='values')
    print(f'Saved {len(df_guests)} records into {save_path}')


def get_full_send_data(URL, save_path):
    page = requests.get(URL)
    html = page.content
    html_content = str(BeautifulSoup(html, "html.parser"))

    pattern = r'alt="(\b[A-Z]\w+\b \b[A-Z]\w+\b)"'
    guests = re.findall(pattern, html_content)

    # Saving data to json
    with open(save_path, "w") as f:
        json.dump(guests, f)
    print(f'Saved {len(guests)} records into {save_path}')


def main():
    url = 'https://lexfridman.com/podcast/'
    class_name = "vid-person"
    lex_path = 'data/LEXguests.json'

    get_lex_guests(
        URL=url,
        class_=class_name,
        save_path=lex_path)
    
    jre_save_path = 'data/JREguests.json'
    get_JRE_guests(jre_save_path)

    # getting fullsend data throught wesite sourse search
    url = 'https://www.imdb.com/title/tt15423300/fullcredits/?ref_=tt_cl_sm'
    fs_path = 'data/FULLSENDguests.json'
    get_full_send_data(url, fs_path)


if __name__ == '__main__':
    main()