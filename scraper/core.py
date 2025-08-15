import json
import os
import sys

from .syllabus import fetch_matrix_html_by_department, parse_subject_matrix_table
from .timetable import fetch_timetable_html, parse_timetable_html

from .utils import Map

DEPARTMENT_CODE_MAP = Map(
    {
        "AA": "工学部 機械工学課程 基幹機械コース",
        "AB": "工学部 機械工学課程 先進機械コース",
        "AC": "工学部 物質化学課程 環境・物質工学コース",
        "AD": "工学部 物質化学課程 化学・生命工学コース",
        "AE": "工学部 電気電子工学課程 電気・ロボット工学コース",
        "AG": "工学部 電気電子工学課程 先進電子工学コース",
        "AF": "工学部 情報・通信工学課程 情報通信コース",
        "AL": "工学部 情報・通信工学課程 情報工学コース",
        "AH": "工学部 土木工学課程 都市・環境コース",
    }
)


def integrate_timetable_to_syllabus(
    subjects: list[dict], year: int, department: str, grade: int, semester_code: int
) -> list[dict]:
    timetable_html = fetch_timetable_html(year, department, grade, semester_code)
    timetable = parse_timetable_html(timetable_html)

    subjects_index = {
        subject["courseName"]: index for index, subject in enumerate(subjects)
    }

    for class_ in timetable:
        class_name = class_["name"]
        index = subjects_index.get(class_name)
        if index is None:
            print(
                f"Subject '{class_name}' not found in subjects.",
                file=sys.stderr,
            )
            continue
        if "classes" not in subjects[index]:
            subjects[index]["classes"] = {}
        if str(year) not in subjects[index]["classes"]:
            subjects[index]["classes"][str(year)] = []
        subjects[index]["classes"][str(year)].append(class_["details"])

    return subjects


def download_syllabus(
    admission_year: int, department: str, save_path: str | None = None
) -> None:
    html = fetch_matrix_html_by_department(admission_year, department)
    subjects = parse_subject_matrix_table(html)

    department_code = department.upper()

    data = {
        "departmentCode": department_code,
        "department": DEPARTMENT_CODE_MAP.get(department_code),
        "admissionYear": admission_year,
        "courses": subjects,
    }

    if save_path is None:
        save_path = f"./data/{admission_year}/{department.lower()}.json"

    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def download_timetable(
    admission_year: int,
    department: str,
    year: int,
    grade: int,
    semester_code: int,
    save_path: str | None = None,
) -> None:
    if save_path is None:
        save_path = f"./data/{admission_year}/{department.lower()}.json"

    if not os.path.exists(save_path):
        print(f"File not found: {save_path}", file=sys.stderr)
        return

    with open(save_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        subjects = data.get("courses", [])

    subjects = integrate_timetable_to_syllabus(
        subjects, year, department, grade, semester_code
    )

    data["courses"] = subjects

    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
