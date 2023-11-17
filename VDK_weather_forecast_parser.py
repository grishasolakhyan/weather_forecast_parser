from bs4 import BeautifulSoup
import requests
import json
import csv

url = "https://www.gismeteo.ru/weather-vladivostok-4877/month/"

headers = {
    "Accept": "*/*",
    "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 YaBrowser/23.3.4.603 Yowser/2.5 Safari/537.36"
}

req = requests.get(url, headers=headers)
src = req.text

with open("index.html", "w", encoding='utf-8') as file:
    file.write(src)

with open("index.html", encoding='utf-8') as file:
    src = file.read()

soup = BeautifulSoup(src, "lxml")

#собираем заголовки таблицы

Mon = 'Monday'
Tue = 'Tuesday'
Wed = 'Wednesday'
Thu = 'Thursday'
Fri = 'Friday'
Sat = 'Saturday'
Sun = 'Sunday'

week = [Mon, Tue, Wed, Thu, Fri, Sat, Sun]

with open(f"weather_report.csv", "w", encoding="cp1251", newline='') as file:
    writer = csv.writer(file, delimiter=";")
    writer.writerow(week)

all_weather_days = soup.find_all(class_="row-item")
all_days = []
for weather_day in all_weather_days:
    date_weather_day = weather_day.find(class_="date").text
    maxt_weather_day = "Днём: " + weather_day.find(class_="maxt").find(class_="unit unit_temperature_c").text
    mint_weather_day = "Ночью: " + weather_day.find(class_="mint").find(class_="unit unit_temperature_c").text
    day_data = []
    day_data.extend([date_weather_day, maxt_weather_day, mint_weather_day])
    all_days.append(day_data)

for item in range (0, len(all_days)-1):
    if ' ' in all_days[item][0]:
        check_day = all_days[item][0]
        ind_space = check_day.index(' ')
        month_name = check_day[ind_space+1:]
        if ' ' not in all_days[item+1][0]:
            all_days[item+1][0] = all_days[item+1][0] + " " + month_name

k = 7
for item in range (0, len(all_days), k):

    with open(f'weather_report.csv', 'a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(all_days[item:item + k])