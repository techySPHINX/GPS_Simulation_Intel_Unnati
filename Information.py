import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sys

def fetch_toll_info(id, callback):

    url = f"http://tis.nhai.gov.in/TollInformation?TollPlazaID={id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        info[id] = response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching info for ID {id}: {e}")
    finally:
        callback(None)


dates = [
    "Date of fee notification",
    "Commercial Operation Date"
]

tags = {
    "Date of fee notification": "date_fee_notification",
    "Commercial Operation Date": "date_commercial_operation",
    "Fee Rule": "fee_rule",
    "Capital Cost of Project (in Rs. Cr.)": "capital_cost",
    "Cumulative Toll Revenue (in Rs. Cr.)": "cumulative_revenue",
    "Concessions Period": "concessions_period",
    "Design Capacity (PCU)": "design_capacity",
    "Traffic (PCU/day)": "traffic_per_day",
    "Target Traffic (PCU/day)": "target_traffic_per_day",
    "Name of Concessionaire / OMT Contractor": "contractor_name",
    "Name / Contact Details of Incharge": "contact_details"
}


def parse_table(html, id):

    soup = BeautifulSoup(html, 'lxml')
    info_table = soup.find('table', class_='MT10')

    if info_table:
        this_info = {}
        for row in info_table.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) == 2:
                key, value = cells[0].text.strip(), cells[1].text.strip()
                this_info[key] = value

        this_toll = toll_lookup[id]
        for key in this_info:
            try:
                if key in dates:
                    this_toll[tags[key]] = datetime.strptime(this_info[key].split(
                    )[0], "%d-%b-%Y").strftime("%d-%m-%Y")  # Consistent date format
                elif key in ['Traffic (PCU/day)', 'Target Traffic (PCU/day)', 'Cumulative Toll Revenue (in Rs. Cr.)']:
                    this_toll[tags[key]] = float(this_info[key].split()[0])
                else:
                    this_toll[tags[key]] = this_info[key]
            except (ValueError, KeyError) as e:
                print(f"Error parsing key '{key}': {e}")

        del this_toll['traffic']
        del this_toll['target_traffic']
        del this_toll['html']

        this_toll['fee_effective_date'] = datetime.strptime(
            this_toll['fee_effective_date'], "%d-%b-%Y").strftime("%d-%m-%Y")


filename = sys.argv[1]
tolls = json.load(open(filename, 'r', encoding='utf-8'))

info = {}
toll_lookup = {toll['id']: toll for toll in tolls}

q = 10

for toll in tolls:
    fetch_toll_info(toll['id'], lambda: None)


for key in info:
    parse_table(info[key], key)


print(json.dumps(tolls, indent=4))
