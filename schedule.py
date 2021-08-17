import csv

from shift import Shift

class Schedule:
    def __init__(self):
        self.shifts = []

    def add_shift(self, shift):
        self.shifts.append(shift)

    def populate_shifts(self, routes, days, daytimes):
        for route in range(1, routes+1):
            for day in range(1, days+1):
                for daytime in range(1, daytimes+1):
                    s = Shift(route, day, daytime)
                    self.add_shift(s)

    def to_csv(self, file = 'schedule.csv'):
        with open(file, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)

            fieldnames = ['driver_id', 'day', 'route_id', 'shifts_id']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for s in sorted(self.shifts, key = lambda x: (x.driver.id, x.route, x.day), reverse = False):
                writer.writerow({'driver_id': s.driver.id, 'day': s.day, 'route_id': s.route, 'shifts_id': s.daytime})



    def __str__(self):
        str_res = ''
        for s in self.shifts:
            str_res += f'{s.route}, {s.day}, {s.daytime}, {s.driver}\n'

        return str_res