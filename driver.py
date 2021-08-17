class Driver:
    def __init__(self, id):
        self.id = id
        self.qualified_route = []
        self.pref_days_off = []
        self.forced_days_off = []
        self.pref_shifts = {}
        self.allocated_shifts = []
        self.night_allocated_shifts = []

    def allocate(self, shift):
        self.allocated_shifts.append(shift)
        if shift.daytime == 2:
            self.night_allocated_shifts.append(shift)

    def remove_shift(self, shift):
        self.allocated_shifts.pop(shift)
        if shift.daytime == 2:
            self.night_allocated_shifts.pop(shift)

    def is_already_allocated(self, day):
        return any(filter(lambda x: x.day == day, self.allocated_shifts))

    def __str__(self):
        return f"Driver #{self.id}"