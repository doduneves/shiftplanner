import unittest

from driver import Driver
from fleet import Fleet
from schedule import Schedule
from score import Score
from shift import Shift

from main import *


# Global data
DAYS = 14
ROUTES = 3
SHIFTS = 2

class TestOverall(unittest.TestCase):
    def _generate_fleet_from_csv(self):
        fleet = Fleet()
        fleet.retrieve_data_from_csv('pref_work_shift')
        fleet.retrieve_data_from_csv('qualified_route')
        fleet.retrieve_data_from_csv('forced_day_off')
        fleet.retrieve_data_from_csv('pref_day_off')

        return fleet

    def _allocate_shifts(self):
        fleet = self._generate_fleet_from_csv()

        schedule = Schedule()
        schedule.populate_shifts(DAYS, ROUTES, SHIFTS)

        return schedule, fleet


    def test_retrieving_csv(self):
        fleet = Fleet()

        fleet.retrieve_data_from_csv('pref_work_shift')
        fleet.retrieve_data_from_csv('qualified_route')
        fleet.retrieve_data_from_csv('forced_day_off')
        fleet.retrieve_data_from_csv('pref_day_off')

        self.assertEqual(len(fleet.drivers), 11)

        for k, d in enumerate(fleet.drivers):
            self.assertEqual(d.__str__(), f"Driver #{k+1}")


    def test_generating_shifts(self):
        schedule = Schedule()
        schedule.populate_shifts(DAYS, ROUTES, SHIFTS)

        self.assertEqual(len(schedule.shifts), DAYS * ROUTES * SHIFTS)


    def test_allocating_shifts(self):
        schedule, fleet = self._allocate_shifts()

        for shift in schedule.shifts:
            self.assertIsNone(shift.driver)

        scores = generate_scores(fleet, schedule)
        self.assertEqual(len(scores), DAYS * ROUTES * SHIFTS * len(fleet.drivers))

        for s in scores:
            self.assertIsNone(shift.driver)

        for score in sorted(scores, key = lambda x: x.score, reverse=True):
            score.shift.allocate_driver(score.driver)

        for s in scores:
            self.assertIsNotNone(s.driver)
            self.assertLess(len(s.driver.night_allocated_shifts), 5)



if __name__ == '__main__':
    unittest.main()