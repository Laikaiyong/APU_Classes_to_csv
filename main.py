import requests
import json
from datetime import datetime, date
import csv

EXCLUDE_CLASSES = [
    "MAE",
    "FWDD",
    "BMK2"
]

today = date.today()
api_url = "https://s3-ap-southeast-1.amazonaws.com/open-ws/weektimetable"

response = requests.get(url=api_url)

timeschedule = json.loads(response.text)
# classes = [
#     d
#     for d in timeschedule
#     if d['INTAKE'] == "APD2F2211SE"
# ]

classes = []
for schedule in timeschedule:
    if schedule['INTAKE'] == "APD2F2211SE":
        proceedable: bool = True
        for class_code in EXCLUDE_CLASSES:
            if class_code in schedule["MODID"]:
                proceedable = False
                
        if proceedable: classes.append(schedule)


headers = ["Course", "Date", "From", "To"]
filename = f'Vandyck_classes({today}).csv'
with open(filename, 'w', newline="") as file:
    csvwriter = csv.writer(file)
    csvwriter.writerow(headers)
    for my_class in classes:
        csvwriter.writerow([
            my_class["MODULE_NAME"],
            my_class["DATESTAMP_ISO"],
            my_class["TIME_FROM"],
            my_class["TIME_TO"]
        ]) 