class Shift:
    def __init__(self, route, day, daytime):
        self.route = route
        self.day = day
        self.daytime = daytime
        self.driver = None

    def allocate_driver(self, driver):
        if not self.driver and not driver.is_already_allocated(self.day):
            if (self.daytime == 2 and len(driver.night_allocated_shifts) < 5) or self.daytime == 1:
                self.driver = driver
                self.driver.allocate(self)