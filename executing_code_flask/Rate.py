import json
from datetime import datetime

# Price model of toll system of different vehicles

def parse_toll_data(filename):

    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    all_booths = []

    def parse_html(booth):

        for row in booth['html'].splitlines():
            if 'Fee Effective Date' in row:

                date_str = row.split('Fee Effective Date')[
                    1].split('</p>')[0].split('</b>')[1]
                booth['fee_effective_date'] = datetime.strptime(
                    date_str, '%d-%b-%Y').strftime('%Y-%m-%d')

            elif any(column in row for column in ['Single Journey', 'Return Journey', '7 or more Axle']):
                columns = row.strip().split(' ')
                car, lcv, bus, three, fourtosix, hcm, seven = columns

                booth['rates']['car_multi'] = float(car.split('Single Journey')[
                                                    1] if 'Single Journey' in car else None)
                booth['rates']['car_monthly'] = float(car.split('Return Journey')[
                                                      1] if 'Return Journey' in car else None)

                booth['rates']['lcv_multi'] = float(lcv.split('Single Journey')[
                                                    1] if 'Single Journey' in lcv else None)
                booth['rates']['lcv_monthly'] = float(lcv.split('Return Journey')[
                                                      1] if 'Return Journey' in lcv else None)

                booth['rates']['bus_multi'] = float(bus.split('Single Journey')[
                                                    1] if 'Single Journey' in bus else None)
                booth['rates']['bus_monthly'] = float(bus.split('Return Journey')[
                                                      1] if 'Return Journey' in bus else None)

                booth['rates']['multiaxle_single'] = float(three.split(
                    '7 or more Axle')[1] if '7 or more Axle' in three else None)
                booth['rates']['multiaxle_multi'] = float(three.split(
                    'Single Journey')[1] if 'Single Journey' in three else None)
                booth['rates']['multiaxle_monthly'] = float(three.split(
                    'Return Journey')[1] if 'Return Journey' in three else None)

                booth['rates']['hcm_single'] = float(hcm.split('7 or more Axle')[
                                                     1] if '7 or more Axle' in hcm else None)
                booth['rates']['hcm_multi'] = float(hcm.split('Single Journey')[
                                                    1] if 'Single Journey' in hcm else None)
                booth['rates']['hcm_monthly'] = float(hcm.split('Return Journey')[
                                                      1] if 'Return Journey' in hcm else None)

                booth['rates']['four_six_axle_single'] = float(fourtosix.split(
                    '7 or more Axle')[1] if '7 or more Axle' in fourtosix else None)
                booth['rates']['four_six_axle_multi'] = float(fourtosix.split(
                    'Single Journey')[1] if 'Single Journey' in fourtosix else None)
                booth['rates']['four_six_axle_monthly'] = float(fourtosix.split(
                    'Return Journey')[1] if 'Return Journey' in fourtosix else None)

                booth['rates']['seven_plus_axle_single'] = float(seven.split(
                    '7 or more Axle')[1] if '7 or more Axle' in seven else None)
                booth['rates']['seven_plus_axle_multi'] = float
