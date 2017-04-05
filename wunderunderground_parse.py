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
    with open('wunderground_test.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=column_names)
        writer.writeheader()

        url = 'https://www.wunderground.com/history/airport/KNYC/2017/4/3/DailyHistory.html'
        r = requests.get(url)

        # soup = BeautifulSoup(r.content, 'html.parser')
        soup = BeautifulSoup(r.content.decode('utf-8','ignore'),'html.parser')
        # print(soup.prettify('utf-8'))
        # test = soup.find_all('table')
        # # print(test[4])

        table = soup.find('table',id="obsTable")
        # print(type(table))
        # print(table)

        rows = table.find_all('tr')[1:]
        # print(rows[1].prettify())
        for row in rows:
            columns = row.find_all('td')
            # print(len(columns))

            col_dict = {}
            for col_index, column in enumerate(columns):
                col_dict[column_names[col_index]] = str(column.getText().strip()).replace('\xa0',' ')
            # print(col_dict)
            writer.writerow(col_dict)

def scrap_daily_wunder_csv():
    with open('wunderground_test.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # writer.writeheader()

        url = 'https://www.wunderground.com/history/airport/KNYC/2017/4/3/DailyHistory.html?format=0'
        r = requests.get(url)
        contents = str(r.content).split("<br />\\n")
        header = contents[0][4:].split(',')
        writer.writerow(header)
        rows = [list(row.split(',')) for row in contents[1:]]
        for row in rows:
            # print(row)
            writer.writerow(row)

# scrap_daily_wunder_html()
scrap_daily_wunder_csv()