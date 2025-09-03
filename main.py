import re
import json
from collections import defaultdict

INPUT_FILE = "3sep.txt"
OUTPUT_FILE = "purchases.json"

def parse_payments():
    # regex से username और mobile निकालेंगे
    username_pattern = re.compile(r"Username:\s*(.+)")
    mobile_pattern = re.compile(r"Mobile:\s*(\d+)")

    purchases = defaultdict(lambda: {"mobile": "", "purchases": 0})

    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()

        username = None
        mobile = None

        for line in lines:
            line = line.strip()

            # username match
            u_match = username_pattern.search(line)
            if u_match:
                username = u_match.group(1).strip()

            # mobile match
            m_match = mobile_pattern.search(line)
            if m_match:
                mobile = m_match.group(1).strip()

            # जब दोनों मिल जाएं तो purchase count बढ़ा दो
            if username and mobile:
                key = f"{username}_{mobile}"
                purchases[key]["mobile"] = mobile
                purchases[key]["username"] = username
                purchases[key]["purchases"] += 1

                # reset next payment के लिए
                username, mobile = None, None

    except Exception as e:
        print("Error reading/parsing file:", e)

    # dict → list + sorting by purchases
    purchase_list = list(purchases.values())
    purchase_list.sort(key=lambda x: x["purchases"], reverse=True)

    return purchase_list


def save_to_json(data):
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f" Data saved to {OUTPUT_FILE}")
    except Exception as e:
        print("Error saving JSON:", e)


if __name__ == "__main__":
    data = parse_payments()
    save_to_json(data)
    print(json.dumps(data, indent=4, ensure_ascii=False))
