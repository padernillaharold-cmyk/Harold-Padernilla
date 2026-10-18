import requests

url = "https://paclibarjosilp-2.onrender.com/student"

response = requests.get(url, timeout=30)

if response.status_code != 200:
    print("Request failed.")
    print("Status Code:", response.status_code)
    print("Response:", response.text[:500])
else:
    data = response.json()
    if isinstance(data, dict):
        for key, value in data.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
    else:
        print(data)