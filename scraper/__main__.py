from .core import download_syllabus, download_timetable


def main(*args):
    match args[1]:
        case "syllabus":
            if len(args[2:]) >= 2:
                admission_year = int(args[2])
                department = args[3]
                save_path = args[4] if len(args[2:]) >= 3 else None
            else:
                admission_year = int(input("Enter admission year: "))
                department = input("Enter department: ")
                save_path = input("Enter save path (optional): ") or None
            download_syllabus(
                admission_year=admission_year,
                department=department,
                save_path=save_path,
            )

        case "timetable":
            if len(args[2:]) >= 5:
                admission_year = int(args[2])
                department = args[3]
                year = int(args[4])
                grade = int(args[5])
                semester_code = int(args[6])
                save_path = args[7] if len(args[2:]) >= 6 else None
            else:
                admission_year = int(input("Enter admission year: "))
                department = input("Enter department: ")
                year = int(input("Enter year: "))
                grade = int(input("Enter grade: "))
                semester_code = int(input("Enter semester code: "))
                save_path = input("Enter save path (optional): ") or None
            download_timetable(
                admission_year=admission_year,
                department=department,
                year=year,
                grade=grade,
                semester_code=semester_code,
                save_path=save_path,
            )

        case _:
            pass


if __name__ == "__main__":
    import sys

    main(*sys.argv)
