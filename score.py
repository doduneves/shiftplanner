class Score:
    def __init__(self, driver, shift):
        self.driver = driver
        self.shift = shift
        self.score = 0

    def __str__(self):
        return f"{self.driver} - {self.shift.route},{self.shift.day},{self.shift.daytime} = {self.score}"
