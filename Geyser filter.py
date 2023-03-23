import time


class Filter:
    def __init__(self, date):
        self.date = date

    def __setattr__(self, key, value):
        if key == 'date' and key in self.__dict__:
            return
        super().__setattr__(key, value)


class Mechanical(Filter):
    name = 'Mechanical'


class Aragon(Filter):
    name = 'Aragon'


class Calcium(Filter):
    name = 'Calcium'


class GeyserClassic:
    MAX_DATE_FILTER = 100

    def __init__(self):
        self.slots = [None, None, None]

    def add_filter(self, slot_num, filter):
        if slot_num in (1, 2, 3) and isinstance(filter, Filter) and self.slots[slot_num-1] is None:
            self.slots[slot_num-1] = filter

    def remove_filter(self, slot_num):
        if slot_num in (1, 2, 3) and self.slots[slot_num-1] is not None:
            self.slots[slot_num-1] = None

    def get_filters(self):
        return tuple(self.slots)

    def water_on(self):
        end = time.time()
        if None in self.slots:
            return False
        for slot in self.slots:
            if end - slot.date > self.MAX_DATE_FILTER:
                return False
        return True


