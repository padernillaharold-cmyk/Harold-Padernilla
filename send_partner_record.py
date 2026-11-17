import requests


PARTNER_URL = "https://paclibarjosilp-2.onrender.com/api/students"
RECORD = {
    "student_id": "EXT-001",
    "name": "Sample Exchange Record",
    "program": "BSIT",
    "year": 1,
    "section": "A",
    "source": "Partner API",
}


if __name__ == "__main__":
    response = requests.post(PARTNER_URL, json=RECORD, timeout=15)
    print(response.status_code)
    print(response.text)
