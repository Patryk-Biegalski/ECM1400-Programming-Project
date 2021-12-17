import csv
from uk_covid19 import Cov19API
import sched
import time
import logging

logging.basicConfig(filename='logger.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s - %(module)s - %(lineno)s ')


# turns a csv file into a list of lists
# removes the top line of the csv, that is the column headers
def parse_csv_data(csv_filename):
    rows = []
    with open(csv_filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            rows.append(row)
    return (rows)

# returns the hospital cases from the most recent date (top line)
# adds up the new cases for 7 days starting after the first non-null value
# excluding said value as it may be incomplete
# returns the cumulative deaths from the first non-null line
def process_covid_csv_data(covid_csv_data):
    last7days_cases = 0
    total_deaths = 0
    count = 1000
    for idx, row in enumerate(covid_csv_data):
        if idx != 0:
            if idx == 1:
                current_hospital_cases = int((row[5]))
            if bool(row[6])== True:
                if count == 1000:
                    count = idx
                if idx > count and idx < (count + 8):
                    last7days_cases += int(row[6])
            if (bool((row[4]))) == True:
                if total_deaths == 0:
                    total_deaths = int(row[4])
    return (last7days_cases, current_hospital_cases, total_deaths)

# unfinished
def schedule_covid_updates(update_interval, update_name, repeat = False):
    scheduler = sched.scheduler(time.time, time.sleep)
    #alarm = scheduler.enterabs(update_interval, 1, update_covid_data)
    #scheduler.run()
    #print(alarm)


# defines location to base data on
# defines data to fetch {assigned name: API name}
# fetches data from API in json format
# returns data as a dictionary 
def covid_API_request(location ="Exeter" , location_type="ltla"):
    myfilters = ['areaType='+(location_type),'areaName='+(location)]
    mystructure = {"areaCode": "areaCode",
                   "areaName": "areaName",
                   "areaType": "areaType",
                   "date": "date",
                   "cumDailyNsoDeathsByDeathDate": "cumDailyNsoDeathsByDeathDate",
                   "hospitalCases": "hospitalCases",
                   "newCasesBySpecimenDate": "newCasesBySpecimenDate",
                   }
    api = Cov19API(filters=myfilters, structure=mystructure)
    data = api.get_json()
    return (data)


# uses covid_API_request to get updated covid data
# processes the data to return deaths, cases, and hospitalisations 
def update_covid_data(location = 'Exeter', location_type='ltla'):
    try:
        data = (covid_API_request(location, location_type)["data"])
    except Exception as e:
        logging.exception("Covid data API could not be accessed")
        return("Data unavailable","Data unavailable","Data unavailable")
    last7days_cases = 0
    total_deaths = 0
    first = True
    count = -1
    for dictionary in data:
        if first == True:
            current_hospital_cases = dictionary["hospitalCases"]
            location = dictionary["areaName"]
            first = False
        if bool(dictionary["newCasesBySpecimenDate"]) == True:
            count += 1
            if count > 0 and count < 8:
                last7days_cases += int(dictionary["newCasesBySpecimenDate"])
        if bool(dictionary["cumDailyNsoDeathsByDeathDate"]) == True:
            if total_deaths == 0:
                total_deaths = dictionary["cumDailyNsoDeathsByDeathDate"]
    return(last7days_cases, current_hospital_cases, total_deaths,location)

