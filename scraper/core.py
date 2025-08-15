import json
import os
import sys

from .syllabus import fetch_matrix_html_by_department, parse_subject_matrix_table
from .timetable import fetch_timetable_html, parse_timetable_html


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

    if save_path is None:
        save_path = f"./data/{admission_year}/{department}.json"

    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(subjects, f, ensure_ascii=False, indent=4)


def download_timetable(
    admission_year: int,
    department: str,
    year: int,
    grade: int,
    semester_code: int,
    save_path: str | None = None,
) -> None:
    if save_path is None:
        save_path = f"./data/{admission_year}/{department}.json"

    if not os.path.exists(save_path):
        print(f"File not found: {save_path}", file=sys.stderr)
        return

    with open(save_path, "r", encoding="utf-8") as f:
        subjects = json.load(f)

    subjects = integrate_timetable_to_syllabus(
        subjects, year, department, grade, semester_code
    )

    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(subjects, f, ensure_ascii=False, indent=4)
