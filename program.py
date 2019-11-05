class Planner:
    def __init__(self, total_storeys):
        self.levels = [Level(i) for i in range(total_storeys)]
        # index 0: upwards; index 1: downwards
        self.direction_indicator = [False, False]

    def press_button(self, level, direction):
        # TODO turn the light on this level on
        pass


class Level:
    def __init__(self, number):
        self.number = number
        # direction UP: 0, DOWN: 1
        self.queues = [[], []]

    def person_come(self, person, direction):
        self.queues[direction].append(person)


class Person:
    def __init__(self, start_level, destination_level, planner):
        self.start_level = start_level
        self.destination_level = destination_level
        self.direction = 0 if destination_level - start_level > 0 else 1
        self.planner = planner

    def press_button(self):
        self.planner.press_button(self.start_level, self.direction)
