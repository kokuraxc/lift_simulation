class Level:
    def __init__(self, number):
        self.number = number
        # direction UP: 0, DOWN: 1
        self.queues = [[], []]

    def person_come(self, person, direction):
        self.queues[direction].append(person)


class Person:
    def __init__(self, start_level, destination_level):
        self.start_level = start_level
        self.destination_level = destination_level


