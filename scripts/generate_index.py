import glob
import json
import os
import sys

OUTPUT_FILENAME = "./data/index.json"


def create_file_list() -> list[dict]:
    file_list = []

    for file_path in glob.glob("./data/*/*.json"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {file_path}", file=sys.stderr)
            continue

        rel_path = os.path.relpath(file_path, "./data")
        normalized_path = rel_path.replace("\\", "/")
        file_info = {
            "path": normalized_path,
            "departmentCode": data.get("departmentCode", None),
            "department": data.get("department", None),
            "admissionYear": data.get("admissionYear", None),
        }
        file_list.append(file_info)

    return file_list


def main() -> None:
    file_list = create_file_list()

    with open(OUTPUT_FILENAME, "w", encoding="utf-8") as output_file:
        json.dump(file_list, output_file, ensure_ascii=False, indent=4)

    print(f"Index file created at {OUTPUT_FILENAME}")


if __name__ == "__main__":
    main()
