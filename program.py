import threading
import time
import logging

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
        self.current_location = 0
        self.pressed_levels = [] # levels pressed by passengers on board
        self.calling_levels = [] # levels passed from the planner
        self.passengers = []
        threading.Thread(target=self.move).start()

    def call_to_level(self, level_index):
        if level_index not in self.calling_levels:
            self.calling_levels.append(level_index)

    def move(self):
        while True:
            time.sleep(self.speed)
            self.current_location += self.speed * self.moving_direction
            # passengers get out
            if self.current_location in self.pressed_levels:
                self.passengers = [p for p in self.passengers if p.destination_level != self.current_location]
                self.pressed_levels.remove(self.current_location)
            # passengers get in
            if self.current_location in self.calling_levels:
                new_passengers = self.planner.levels[self.current_location].get_passengers(self.moving_direction)
                for p in new_passengers:
                    p.press_button_destination(self)
                self.passengers += new_passengers
                self.calling_levels.remove(self.current_location)
            # decide whether to move upwards or downwards
            all_levels = self.pressed_levels + self.calling_levels
            all_levels.sort()
            if len(all_levels) > 0:
                if self.moving_direction == 1 and self.current_location < all_levels[-1]:
                    pass # keep the same direction: upwards
                else:
                    self.moving_direction = -1
                if self.moving_direction == -1 and self.current_location > all_levels[0]:
                    pass # keep the same direction: downwards
                else:
                    self.moving_direction = 1
            else:
                self.moving_direction = 0





        

class Level:
    def __init__(self, position):
        self.position = position
        # direction UP: 1, DOWN: -1; 0 is undefined
        self.queues = [None, [], []]
        # index 1: upwards; index -1: downwards; index 0: undefined
        self.direction_indicator = [None, False, False]

    def person_come(self, person, direction):
        self.queues[direction].append(person)

    # get all the passengers who want to go the "direction"
    def get_passengers(self, direction):
        ret = self.queues[direction]
        self.queues[direction] = []
        return ret


class Person:
    def __init__(self, start_level, destination_level, planner):
        self.start_level = start_level
        self.destination_level = destination_level
        self.direction = 1 if destination_level - start_level > 0 else -1
        self.planner = planner

    def press_button_call_cart(self):
        self.planner.press_button(self.start_level, self.direction)
    
    def press_button_destination(self, cart):
        if self.destination_level not in cart.pressed_levels and self.destination_level != cart.current_location:
            cart.pressed_levels.append(self.destination_level)