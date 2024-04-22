import json
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
from Utils.prediction import attendance_predictor, bunk_predictor


def login_to_samvidha(username_f, password_f):
    url = "https://samvidha.iare.ac.in/pages/login/checkUser.php"
    payload = {
        "username": username_f.upper(),
        "password": password_f
    }
    response = requests.post(url, data=payload)
    login_status_json = json.loads(response.text)
    if login_status_json["status"] == "1":
        return {
            "status": True,
            "msg": login_status_json["msg"],
            "cookies": response.cookies
        }
    else:
        return {
            "status": False,
            "msg": login_status_json["msg"]
        }


def get_user_details(cookies):
    home_url = "https://samvidha.iare.ac.in/home?action=profile"
    res = requests.get(home_url, cookies=cookies)
    if res.status_code != 200:
        return {
            "Full Name": None,
            "image_url": None,
            "Branch": None,
            "Roll Number": None,
            "Semester": None,
            "Section": None
        }
    soup = BeautifulSoup(res.text, features="html.parser")
    scraped_data = soup.select(
        "body > div > div.content-wrapper > section.content > div > div > div:nth-child(1) > div:nth-child(2) > div.card-body > dl")
    if len(scraped_data) == 0:
        return {
            "Full Name": None,
            "image_url": None,
            "Branch": None,
            "Roll Number": None,
            "Semester": None,
            "Section": None
        }
    roll_number = scraped_data[0].select("dd")[0].text.strip().upper()
    img_url = f"https://iare-data.s3.ap-south-1.amazonaws.com/uploads/STUDENTS/{roll_number}/{roll_number}.jpg"
    full_name = scraped_data[0].select("dd")[3].text.strip().title()
    branch = scraped_data[0].select("dd")[5].text.strip().title()
    semester = scraped_data[0].select("dd")[6].text.strip().upper()
    section = scraped_data[0].select("dd")[7].text.strip().upper()
    return {
        "Full Name": full_name,
        "image_url": img_url,
        "Branch": branch,
        "Roll Number": roll_number,
        "Semester": semester,
        "Section": section
    }


def get_user_data_in_tables(cookies, url, table_selector):
    r = requests.get(url, cookies=cookies)
    soup = BeautifulSoup(r.text, features="html.parser")
    full_table = soup.select(table_selector)[0]
    if len(full_table) == 0:
        return None
    table_header = []
    table_data = []
    for element in full_table.select("th"):
        element = re.sub(r'[^\x00-\x7F]+', ' ', element.text.strip())
        table_header.append(element)
    for element in full_table.select("tr")[1:-1]:
        row_data = []
        for value in element.select("td"):
            value = re.sub(r'[^\x00-\x7F]+', ' ', value.text.strip())
            row_data.append(value)
        table_data.append(row_data)
    df = pd.DataFrame(table_data, columns=table_header)
    return df


def attendance_needed_subjects(df, given_percentage):
    needed_attendance = {}
    for index, row in df.iterrows():
        attended = int(row["Attended"])
        total = int(row["Conducted"])
        if total == 0:
            continue
        percentage = attended / total * 100
        if percentage < given_percentage:
            needed_attendance[row["Course Name"]] = attendance_predictor(attended, total, given_percentage)
    new_df = pd.DataFrame(needed_attendance.items(), columns=['Course Name', 'Attend'])
    new_df.insert(0, 'S.No', [i for i in range(1, len(new_df) + 1)], True)
    return new_df


def get_bunk_subjects(df, given_percentage):
    bunk_count = {}
    for index, row in df.iterrows():
        attended = int(row["Attended"])
        total = int(row["Conducted"])
        if total == 0:
            continue
        percentage = attended / (total+1) * 100
        if  percentage > given_percentage:
            bunk_count[row["Course Name"]] = bunk_predictor(attended, total, given_percentage)
    new_df = pd.DataFrame(bunk_count.items(), columns=['Course Name', 'Bunk'])
    new_df.insert(0, 'S.No', [i for i in range(1, len(new_df) + 1)], True)
    return new_df







