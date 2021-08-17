from fleet import Fleet
from schedule import Schedule
from score import Score

# Global data
DAYS = 14
ROUTES = 3
SHIFTS = 2
GENERATE_CSV = True


def generate_scores(fleet, schedule):
    list_scores = []
    for shift in schedule.shifts:
        for driver in fleet.drivers:
            s = Score(driver, shift)

            if (
                shift.route in driver.qualified_route and
                shift.day not in driver.forced_days_off
            ):
                # Preferred workshift: Yes [10], No [0]
                if driver.pref_shifts[shift.day] == str(shift.daytime):
                    s.score += 10

                # Preferred day off: Yes [0], No [5]
                if shift.day not in driver.pref_days_off:
                    s.score += 5

                # Also giving some point to who preferred to work at night
                if shift.daytime == 2:
                    s.score += 2

            list_scores.append(s)

    return list_scores


def main():
    fleet = Fleet()
    fleet.retrieve_data_from_csv('pref_work_shift')
    fleet.retrieve_data_from_csv('qualified_route')
    fleet.retrieve_data_from_csv('forced_day_off')
    fleet.retrieve_data_from_csv('pref_day_off')

    schedule = Schedule()
    schedule.populate_shifts(ROUTES, DAYS, SHIFTS)

    # Listing all the scores for (driver, shift)
    list_scores = generate_scores(fleet, schedule)

    # Schedulling ordering by greatest scores first
    for score in sorted(list_scores, key = lambda x: x.score, reverse=True):
        score.shift.allocate_driver(score.driver)

    if(GENERATE_CSV):
        schedule.to_csv()


if __name__ == '__main__':
    main()