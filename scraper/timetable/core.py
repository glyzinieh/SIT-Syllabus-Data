import sys
import time

from bs4 import BeautifulSoup
from selenium import webdriver

from ..utils import Map

TIMETABLE_URL = "http://timetable.sic.shibaura-it.ac.jp/table/{year}/Timetable{faculty_code}{department_code}{semester_code}{grade}.html"

FACULTY_CODE_MAP = Map(
    {
        # 工学部
        "A": 1
        # システム理工学部(非対応)
        # デザイン工学部(非対応)
        # 建築学部(非対応)
        # 大学院理工学研究科修士課程(非対応)
        # 大学院理工学研究科博士(後期)課程(非対応)
    }
)

DEPARTMENT_CODE_MAP = Map(
    {
        # 工学部
        # 機械工学課程
        "AA": "AA0",  # 基幹機械コース
        "AB": "BB0",  # 先進機械コース
        # 物質化学課程
        "AC": "CC0",  # 環境・物質工学コース
        "AD": "DD0",  # 化学・生命工学コース
        # 電気電子工学課程
        "AE": "EE0",  # 電気・ロボット工学コース
        "AG": "GG0",  # 先端電子工学コース
        # 情報・通信工学課程
        "AF": "FF0",  # 情報通信コース
        "AL": "LL0",  # 情報工学コース
        # 土木工学課程
        "AH": "HH0",  # 都市・環境コース
        # システム理工学部(非対応)
        # デザイン工学部(非対応)
        # 建築学部(非対応)
        # 大学院理工学研究科修士課程(非対応)
        # 大学院理工学研究科博士(後期)課程(非対応)
    }
)


def fetch_timetable_html(
    year: int, department: str, grade: int, semester_code: int
) -> str:
    faculty_code = FACULTY_CODE_MAP.get(department[0])
    department_code = DEPARTMENT_CODE_MAP.get(department)
    url = TIMETABLE_URL.format(
        year=year,
        faculty_code=faculty_code,
        department_code=department_code,
        semester_code=semester_code,
        grade=grade,
    )

    with webdriver.Chrome() as driver:
        driver.get(url)
        time.sleep(3)  # Wait for the page to load
        html = driver.page_source

    return html


def parse_timetable_html(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")

    days = [
        ("mon", "月"),
        ("tue", "火"),
        ("wed", "水"),
        ("thu", "木"),
        ("fri", "金"),
        ("sat", "土"),
        ("oth", "その他"),
    ]

    classes_map = {}

    for day, jp_day in days:
        timetable_table = soup.select_one(f"table#{day} table")
        if not timetable_table:
            raise ValueError(f"Table for {jp_day} not found in the HTML.")

        rows = timetable_table.select("tr")
        for row in rows[2:]:
            classes = row.select("td#Subject")

            for class_ in classes:
                try:
                    period = int(str(class_.get("row"))) + 1
                except (ValueError, TypeError):
                    period = None
                    print(f"Error parsing period for class: {class_}", file=sys.stderr)

                class_table = class_.select_one("table")
                if not class_table:
                    print(f"Class table not found for class: {class_}", file=sys.stderr)
                    continue

                class_rows = class_table.select("tr")
                course_name = class_rows[1].get_text(strip=True)
                instructor = class_rows[0].select("td")[1].get_text(strip=True)

                splited_td = list(class_rows[2].stripped_strings)
                campus = splited_td[0]
                note = splited_td[2] if len(splited_td) > 2 else ""

                class_key = (
                    (course_name, instructor, campus, note, day, period)
                    if "ペア" not in note
                    else (course_name, instructor, campus, note)
                )

                if class_key not in classes_map:
                    classes_map[class_key] = {
                        "name": course_name,
                        "details": {
                            "instructor": instructor,
                            "campus": campus,
                            "note": note,
                            "weeklySlots": [],
                        },
                    }

                if period is None:
                    classes_map[class_key]["details"]["weeklySlots"].append(
                        {"day": jp_day, "period": None}
                    )
                    continue

                try:
                    colspan = int(str(class_.get("colspan", "1")))
                except (ValueError, TypeError):
                    colspan = 1

                if colspan >= 2:
                    for i in range(colspan):
                        classes_map[class_key]["details"]["weeklySlots"].append(
                            {"day": jp_day, "period": period + i}
                        )
                else:
                    classes_map[class_key]["details"]["weeklySlots"].append(
                        {"day": jp_day, "period": period}
                    )

    return [*classes_map.values()]
