import requests

url = "https://harold-padernilla-4.onrender.com/course"
response = requests.get(url, timeout=15)

response.raise_for_status()
data = response.json()
print("Course code:", data["course_code"])
print("Course name:", data["course_name"])
print("Program:", data["program"])
print("Year level:", data["year_level"])
