import requests
from bs4 import BeautifulSoup
import csv
import datetime

# station = 'KNYNEWYO591'
station = 'KNYNEWYO421'
start_year = 2011
end_year = 2013
# filename = 'wunderground_{0}-{1}.csv'.format(start_year, end_year)
filename = 'amateur_{2}_{0}-{1}.csv'.format(start_year, end_year, station)

months_with_30days = [4, 6, 9, 11]

# header = ['TimeEDT', 'TemperatureF', 'Dew PointF', 'Humidity', 'Sea Level PressureIn', 'VisibilityMPH',
#           'Wind Direction', 'Wind SpeedMPH', 'Gust SpeedMPH', 'PrecipitationIn', 'Events', 'Conditions',
#           'WindDirDegrees', 'DateUTC']

# url = 'https://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID=KNYNEWYO591&day=21&month=04&year=2017&graphspan=day&format=1'

def scrap_daily_wunder_csv(year, month, day, station):
    # writer = csv.writer(csvfile)
    url = 'https://www.wunderground.com/weatherstation/WXDailyHistory.asp' \
                '?ID={3}&day={2}&month={1}&year={0}&graphspan=day&format=1'.format(year, month, day, station)

    r = requests.get(url)
    contents = str(r.content).split("<br>\\n")
    # header = contents[0][4:].split(',')

    rows = [list(row.split(','))[:-1] for row in contents[1:]][:-1]
    for row in rows:
        # print(row)
        writer.writerow(row)



def scrap_year(year):
    # check if leap year
    leap_day = 29 if year % 4 == 0 else 28
    for month in range(1, 13):
        for day in range(1, 32):
            # take care of feb
            if month == 2 and day > leap_day:
                break
            # take care of months with 30 days
            if month in months_with_30days and day > 30:
                break
            print('\r{0} {1} {2}'.format(year, month, day), end='')
            scrap_daily_wunder_csv(year, month, day, station)



with open(filename , 'w', newline='') as csvfile:
    # write header

    today_year= datetime.datetime.today().year
    today_month = datetime.datetime.today().month
    today_day = datetime.datetime.today().day

    url = 'https://www.wunderground.com/weatherstation/WXDailyHistory.asp' \
          '?ID={3}&day={2}&month={1}&year={0}&graphspan=day&format=1'.format(today_year, today_month, today_day, station)
    # print(today_year,today_month,today_day)

    r = requests.get(url)
    contents = str(r.content).split("<br>\\n")
    header = contents[0][4:].split(',')
    # print(header)
    writer = csv.writer(csvfile)
    writer.writerow(header)

    # rows = [list(row.split(','))[:-1] for row in contents[1:]][:-1]
    # for row in rows:
    #     print(row)
    #     writer.writerow(row)


    for year in range(start_year, end_year+1):
        scrap_year(year)

    print("finished")