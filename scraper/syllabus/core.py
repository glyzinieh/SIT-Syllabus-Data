import time

from bs4 import BeautifulSoup
from selenium import webdriver

from ..utils import Map
from .utils import expand_colspan, extract_grade_semester, extract_syllabus_link

MATRIX_URL = "http://syllabus.sic.shibaura-it.ac.jp/syllabus/{admission_year}/Matrix{department_code}.html"


DEPARTMENT_CODE_MAP = Map(
    {
        # 工学部
        # 機械工学課程
        "AA": "AA01",  # 基幹機械コース
        "AB": "BB01",  # 先進機械コース
        # 物質化学課程
        "AC": "CC01",  # 環境・物質工学コース
        "AD": "DD01",  # 化学・生命工学コース
        # 電気電子工学課程
        "AE": "EE01",  # 電気・ロボット工学コース
        "AG": "GG01",  # 先端電子工学コース
        # 情報・通信工学課程
        "AF": "FF01",  # 情報通信コース
        "AL": "LL01",  # 情報工学コース
        # 土木工学課程
        "AH": "HH01",  # 都市・環境コース
        # システム理工学部(非対応)
        # デザイン工学部(非対応)
        # 建築学部(非対応)
        # 大学院理工学研究科修士課程(非対応)
        # 大学院理工学研究科博士(後期)課程(非対応)
    }
)

CREDIT_TYPE_MAP = {
    "◎": "必修",
    "○": "選択必修",
    "△": "選択",
    "□": "自由",
    "☆": "必須認定",
}


def fetch_matrix_html_by_department(admission_year: int, department: str) -> str:
    department_code = DEPARTMENT_CODE_MAP.get(department)
    url = MATRIX_URL.format(
        admission_year=admission_year, department_code=department_code
    )

    with webdriver.Chrome() as driver:
        driver.get(url)
        time.sleep(3)  # Wait for the page to load
        html = driver.page_source

    return html


def parse_subject_matrix_table(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.select("tr.subject")
    if not rows:
        raise ValueError("No subjects found in the table.")

    subjects = []
    for row in rows:
        tds = row.find_all("td")
        if not tds:
            raise ValueError("No columns found in the row.")
        logical_cols = expand_colspan(tds)
        syllabus_link = extract_syllabus_link(row)
        grade, semester, credit_type_mark = extract_grade_semester(logical_cols)
        if not credit_type_mark or credit_type_mark not in CREDIT_TYPE_MAP:
            raise ValueError("Unknown credit type mark.")
        credit_type = CREDIT_TYPE_MAP[credit_type_mark]
        subject = {
            "courseName": logical_cols[3].text.strip(),
            "syllabusLink": syllabus_link,
            "courseCode": logical_cols[2].text.strip(),
            "series": logical_cols[0].text.strip(),
            "credits": int(logical_cols[4].text.strip()),
            "grade": grade,
            "semester": semester,
            "creditType": credit_type,
            "category": logical_cols[15].text.strip(),
        }
        subjects.append(subject)
    return subjects
