import csv
import re

from driver import Driver


class Fleet:
    INPUT_DATA_FOLDER = 'input_test_data'

    def __init__(self):
        self.drivers = []

    def add_driver(self, driver):
        if not self.get_driver_by_id(driver.id):
            self.drivers.append(driver)

    def get_driver_by_id(self, id):
        return next(filter(lambda driver: driver.id == str(id), self.drivers), None)

    def retrieve_data_from_csv(self, file_name):
        with open(f'{self.INPUT_DATA_FOLDER}/{file_name}.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                d = self.get_driver_by_id(row['driverid'])
                if not d:
                    d = Driver(row['driverid'])

                for k, v in row.items():
                    if(file_name == 'pref_work_shift'):
                        if k != 'driverid':
                            index = int(re.findall('\d+', k )[0])
                            d.pref_shifts[index] = v

                    else:
                        if k != 'driverid' and bool(int(v)):
                            index = int(re.findall('\d+', k )[0])
                            if file_name == 'pref_day_off':
                                d.pref_days_off.append(index)
                            if file_name == 'qualified_route':
                                d.qualified_route.append(index)
                            if file_name == 'forced_day_off':
                                d.forced_days_off.append(index)

                self.add_driver(d)