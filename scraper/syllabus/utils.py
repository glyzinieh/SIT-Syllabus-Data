import re

from bs4 import Tag

BASE_URL = "http://syllabus.sic.shibaura-it.ac.jp/syllabus"


def get_move_url(
    fn, base, gcd, sub, year, sid, kcd, did, fid, stat, rYear, rDID, rFID, rSFID, rStat
):
    bRecent = True  # 固定
    lng = ""  # 日本語なので空文字

    l = len(fn)
    if l > 1 and fn[-1] == "E" and fn[-2].isdigit():
        fn = fn[:-1]
        l -= 1
    c = fn[l - 1]
    if c.isdigit():
        c = None

    qs = f"y={year}&g={gcd}" + (f"&c={c}" if c else "")

    if bRecent and rYear and rStat == "1":
        url = f"{BASE_URL}/{rYear}/{base}/{rDID}"
        if sub == "true":
            url += f"-{rSFID}"
        url += f".html{lng}?{qs}"
    else:
        url = f"{BASE_URL}/{year}/{base}/{did}"
        if sub == "true":
            url += f"-{fid}"
        url += f".html{lng}?"
        if int(year) < 2017:
            url += str(gcd)
        else:
            url += qs
    return url


def expand_colspan(tds):
    logical_cols = []
    for td in tds:
        if isinstance(td, Tag):
            colspan_val = td.get("colspan")
            try:
                colspan = (
                    int(colspan_val[0])
                    if isinstance(colspan_val, list)
                    else int(colspan_val) if colspan_val else 1
                )
            except Exception:
                colspan = 1
        else:
            colspan = 1
        logical_cols.extend([td] * colspan)
    return logical_cols


def extract_syllabus_link(row):
    script = row.find("script")
    if not script:
        return None
    script_js = script.get_text()
    if not script_js:
        raise ValueError("No script content found in the script tag.")
    match = re.search(r"move\((.*?)\)", script_js)
    if not match:
        raise ValueError("No move function found in the script.")
    args = [arg.strip().strip("'\"") for arg in match.group(1).split(",")]
    return get_move_url(*args)


SEMESTER_MAP = {
    5: (1, "春学期"),
    6: (1, "秋学期"),
    7: (2, "春学期"),
    8: (2, "秋学期"),
    9: (3, "春学期"),
    10: (3, "秋学期"),
    11: (4, "春学期"),
    12: (4, "秋学期"),
}


def extract_grade_semester(logical_cols):
    for idx in range(5, 13):
        cell = logical_cols[idx]
        text = cell.text.strip()
        if not text:
            continue
        grade, semester = SEMESTER_MAP[idx]
        mark = text[0]
        if isinstance(cell, Tag) and cell.has_attr("colspan"):
            if len(text) > 1 and "(" in text and ")" in text:
                semester = text[text.find("(") + 1 : text.find(")")]
            elif len(text) > 1:
                semester = text[1:]
            else:
                semester = None
        return grade, semester, mark
    return None, None, None
