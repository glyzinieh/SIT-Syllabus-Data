# SIT-Syllabus-Data

本リポジトリは、芝浦工業大学のシラバスデータをJSON形式で管理するためのものです。

## ファイル構成・命名規則

- データは `data/[入学年度]/[学科].json` などにまとめて格納します。
- 例: `data/2025/AL.json`

## JSONフォーマット例

```jsonc
{
    // 学科名(必須)
    "department": "情報工学コース",
    // 入学年度(必須)
    "admissionYear": 2025,
    // 時間割(任意)
    "timetables": [
        {
            // 年度(必須)
            "year": 2025,
            // 学期(必須)
            "semester": "春学期"
        }
    ],
    // 科目リスト(必須)
    "courses": [
        {
            // 科目名(必須)
            "courseName": "線形代数1",
            // シラバスリンク(必須)
            "syllabusLink": "http://syllabus.sic.shibaura-it.ac.jp/syllabus/2025/ko1/148281.html?y=2025&g=LL0",
            // 科目コード(必須)
            "courseCode": "11731100",
            // 系列(必須)
            "series": "数理基礎",
            // 単位数(必須)
            "credits": 2,
            // 配当学年(必須)
            "grade": 1,
            // 学期(必須)
            "semester": "春学期",
            //単位区分(必須)
            "creditType": "必修",
            // 講義区分(必須)
            "category": "講義",
            // 授業情報リスト(任意)
            "classes": {
                // 年度(必須)
                "2025": {
                    // 学期(必須)
                    "春学期": {
                            // 担当教員(必須)
                            "instructor": "芝浦太郎",
                            // キャンパス(必須)
                            "campus": "大宮地区",
                            // 備考(必須)
                            "note": "Lコース対象（必修）",
                            // 週コマ情報(必須)
                            "weeklySlots": [
                                // 曜日・時限(必須)
                                { "day": "月", "period": 1 }
                            ],
                    }
                }
            }
        }
    ],
    // 要件リスト(必須)
    "requirements": [
        {
            // 要件名(必須)
            "requirementName": "卒業要件",
            // 総取得単位数(任意)
            "totalCredits": 124,
            // 系列別取得単位数リスト(任意)
            "seriesCredits": [
                // 系列名・単位数(必須)
                { "seriesName": "数理基礎科目", "credits": 14 }
            ],
            // 対象科目リスト(任意)
            "courses": [
                // 科目コード(必須)
                { "courseCode": "L0001000" }
            ]
        }
    ]
}
```
