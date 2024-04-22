from Utils.prediction import attendance_predictor, bunk_predictor
from datetime import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re


def get_user_bio(cookies):
    bio_url = "https://samvidha.iare.ac.in/home?action=std_bio"
    bio_table_selector = "body > div > div.content-wrapper > section.content > div > div.card-body > table"
    r = requests.get(bio_url, cookies=cookies)
    soup = BeautifulSoup(r.text, 'html.parser')
    full_table = soup.select_one(bio_table_selector)
    if not full_table:
        return None
    table_header = [re.sub(r'[^\x00-\x7F]+', ' ', th.text.strip()) for th in full_table.select("th")]
    table_data = []
    for element in full_table.select("tr")[1:-1]:
        row_data = []
        for value in element.select("td"):
            value = re.sub(r'[^\x00-\x7F]+', ' ', value.text.strip())
            row_data.append(value)
        if len(row_data) == 0:
            continue
        row_data.pop(-1)
        table_data.append(row_data)
    unwanted_columns = {"JNTUH - AEBAS", "Class Attendance(out of 7 periods)"}
    table_header = [col for col in table_header if col not in unwanted_columns]
    df = pd.DataFrame(table_data, columns=table_header)
    df.loc[df["In Time"] == "", "In Time"] = "-"
    return df


def display_bio_update_info(df):
    updated_date_df = df.iloc[0]
    updated_date = {
        "date": updated_date_df["Date"],
        "In Time": updated_date_df["In Time"],
        "Out Time": updated_date_df["Out Time"],
        "Status": updated_date_df["Status"]
    }
    today_date = datetime.now().strftime("%d-%b-%Y")
    today_day = datetime.now().strftime("%A")
    if today_day == "Sunday":
        today_date = (datetime.now() - pd.DateOffset(days=1)).strftime("%d-%b-%Y")
    if updated_date["date"] != today_date:
        return f"Your attendance is not latest *{today_date}*. Last updated on *{updated_date['date']}*"

    else:
        return None


def calculate_bio_attendance(df, absent_count=0):
    status = df["Status"].value_counts()
    present = status["Present"]
    absent = status["Absent"]
    total = present + absent + absent_count
    percentage = present / total * 100
    return percentage


def calculate_bio_attend_or_bunk(df, kind, being_absent=0):
    status = df["Status"].value_counts()
    present = int(status["Present"])
    absent = int(status["Absent"])
    total = present + absent
    if kind == "attend":
        attend = attendance_predictor(present, total + being_absent, 80)
        return attend
    else:
        bunk = bunk_predictor(present, total + being_absent, 80)
        return bunk
