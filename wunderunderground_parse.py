import requests
from bs4 import BeautifulSoup
import csv


column_names = [
'Time(EDT)',
'Temp.',
'Dew Point',
'Humidity',
'Pressure',
'Visibility',
'Wind Dir',
'Wind Speed',
'Gust Speed',
'Precip',
'Events',
'Conditions',]

def scrap_daily_wunder_html():
    # writer = csv.DictWriter(csvfile, fieldnames=column_names)
    # writer.writeheader()

    url = 'https://www.wunderground.com/history/airport/KNYC/2017/4/3/DailyHistory.html'
    r = requests.get(url)
    # soup = BeautifulSoup(r.content, 'html.parser')
    soup = BeautifulSoup(r.content.decode('utf-8','ignore'),'html.parser')
    table = soup.find('table',id="obsTable")
    rows = table.find_all('tr')[1:]
    for row in rows:
        columns = row.find_all('td')
        col_dict = {}
        for col_index, column in enumerate(columns):
            col_dict[column_names[col_index]] = str(column.getText().strip()).replace('\xa0',' ')
        # print(col_dict)
        writer.writerow(col_dict)

def scrap_daily_wunder_csv(year, month, day):
    # writer = csv.writer(csvfile)
    url = 'https://www.wunderground.com/history/airport/KNYC/{0}/{1}/{2}/DailyHistory.html?format=0'.format(year, month, day)
    r = requests.get(url)
    contents = str(r.content).split("<br />\\n")
    header = contents[0][4:].split(',')
    # print(header)
    # writer.writerow(header)
    rows = [list(row.split(',')) for row in contents[1:]]
    for row in rows:
        print(row)
        writer.writerow(row)



# scrap_daily_wunder_csv(2017,4,3)

with open('wunderground_test.csv', 'w', newline='') as csvfile:
    header = ['TimeEDT', 'TemperatureF', 'Dew PointF', 'Humidity', 'Sea Level PressureIn', 'VisibilityMPH', 'Wind Direction', 'Wind SpeedMPH', 'Gust SpeedMPH', 'PrecipitationIn', 'Events', 'Conditions', 'WindDirDegrees', 'DateUTC']
    writer = csv.writer(csvfile)
    writer.writerow(header)

    monthswith30days = [4,6,9,11]
    year = 2016
    if year%4 == 0:
        leap_day = 29
    else:
        leap_day = 28

    for month in range(1,13):
        for day in range(1, 32):
            if month == 2 and day > leap_day:
                break
            if month in monthswith30days and day > 30:
                break

            # print(year, month, day)
            scrap_daily_wunder_csv(year, month, day)
