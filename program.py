class Planner:
    def __init__(self, total_storeys, total_carts_number):
        self.levels = [Level(i) for i in range(total_storeys)]
        self.carts = [Cart(i, self) for i in range(total_carts_number)]

    def press_button(self, level_index, direction):
        # TODO turn the light on this level on
        self.levels[level_index].direction_indicator[direction] = True
        # TODO call the cart to come
        # This part is the most import logic part
        # it decides which cart to send to the Level if there are more than one cart
        # for now, assume there is only one cart

        # pass the planner object to cart method
        self.carts[0].call_to_level(level_index)
        pass


class Cart:
    """ need to implement the move method with threading
    so that it won't interfere with other functions """
    def __init__(self, index, planner):
        self.id = index
        self.planner = planner
        self.max_capacity = 15
        self.speed = 0.1  # randomly choose this speed, doesn't necessarily reflect actual speed
        self.moving_direction = 0  # 1: upwards, -1: downwards, 0: rest
        self.destinations = []
        self.current_location = 0
        self.calling_levels = []

    def call_to_level(self, level_index):
        if level_index not in self.calling_levels:
            self.calling_levels.append(level_index)

    def move(self, moving_direction):
        pass

class Level:
    def __init__(self, position):
        self.position = position
        # direction UP: 1, DOWN: -1; 0 is undefined
        self.queues = [None, [], []]
        # index 1: upwards; index -1: downwards; index 0: undefined
        self.direction_indicator = [None, False, False]

    def person_come(self, person, direction):
        self.queues[direction].append(person)


class Person:
    def __init__(self, start_level_index, destination_level_index, planner):
        self.start_level_index = start_level_index
        self.destination_level_index = destination_level_index
        self.direction = 1 if destination_level_index - start_level_index > 0 else -1
        self.planner = planner

    def press_button(self):
        self.planner.press_button(self.start_level_index, self.direction)