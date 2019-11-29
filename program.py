import threading
import time
import logging
import math

class Planner:
    def __init__(self, total_storeys, total_carts_number):
        self.levels = [Level(i) for i in range(total_storeys)]
        self.carts = [Cart(i, self) for i in range(total_carts_number)]

    def passenger_calls_cart(self, level, direction):
        # TODO turn the light on this level on
        self.levels[level].direction_indicator[direction] = True
        # TODO call the cart to come
        # This part is the most import logic part
        # it decides which cart to send to the Level if there are more than one cart
        # for now, assume there is only one cart

        # pass the planner object to cart method
        self.carts[0].call_to_level(level)
        pass
    def stopAll(self):
        for c in self.carts:
            c.stop()	


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
        # start moving the cart when it's initialized
        # of course, it will remain at the same place if there is no passengers
        self.stop_thread = False
        self.running_thread = threading.Thread(target=self.move)
        self.running_thread.start()

    def call_to_level(self, level):
        if level not in self.calling_levels:
            self.calling_levels.append(level)

    def stop(self):
        self.stop_thread = True

    def move(self):
        while True:
            if self.stop_thread:
            	break

            time.sleep(self.speed)
            self.current_location += self.speed * self.moving_direction

            # fix the float number not precise to 0.1 error
            if abs(self.current_location - math.ceil(self.current_location)) < 0.05:
                self.current_location = math.ceil(self.current_location)
            elif abs(self.current_location - math.floor(self.current_location)) < 0.05:
                self.current_location = math.floor(self.current_location)

            if self.moving_direction != 0:
                print('######')
                print('current direction:', self.moving_direction, '; current location:', self.current_location)
            # passengers get out
            if self.current_location in self.pressed_levels:
                print('at level', self.current_location)
                print('before passengers get OUT, passenger count:', len(self.passengers))
                self.passengers = [p for p in self.passengers if p.destination_level != self.current_location]
                print('after passengers get OUT, passenger count:', len(self.passengers))
                self.pressed_levels.remove(self.current_location)

            # passengers get in # cart is not moving
            if self.current_location in self.calling_levels and len(self.passengers) == 0 and self.moving_direction == 0:
                new_passengers = self.planner.levels[self.current_location].get_passengers(1) # upwards
                _direction = 1
                if len(new_passengers) == 0:
                    new_passengers = self.planner.levels[self.current_location].get_passengers(-1) # downwards
                    _direction = -1
                if len(new_passengers) > 0:
                    for p in new_passengers:
                        p.press_button_destination(self)
                    print('before passengers going', _direction, 'get IN, passenger count:', len(self.passengers))
                    self.passengers += new_passengers
                    print('after passengers going', _direction, 'get IN, passenger count:', len(self.passengers))
                    self.planner.levels[self.current_location].direction_indicator[_direction] = False
            # passengers get in # original direction # cart is moving
            elif self.current_location in self.calling_levels:
                new_passengers = self.planner.levels[self.current_location].get_passengers(self.moving_direction)
                for p in new_passengers:
                    p.press_button_destination(self)
                print('before passengers going', self.moving_direction, 'get IN, passenger count:', len(self.passengers))
                self.passengers += new_passengers
                print('after passengers going', self.moving_direction, 'get IN, passenger count:', len(self.passengers))
                self.planner.levels[self.current_location].direction_indicator[self.moving_direction] = False
            # passengers get in # original direction # after all other passengers get out
            if self.current_location in self.calling_levels and len(self.passengers) == 0 and self.moving_direction != 0:
                self.moving_direction = -self.moving_direction
                new_passengers = self.planner.levels[self.current_location].get_passengers(self.moving_direction)
                for p in new_passengers:
                    p.press_button_destination(self)
                print('before passengers going', self.moving_direction, 'get IN, passenger count:', len(self.passengers))
                self.passengers += new_passengers
                print('after passengers going', self.moving_direction, 'get IN, passenger count:', len(self.passengers))
                self.planner.levels[self.current_location].direction_indicator[self.moving_direction] = False
            
            if self.current_location in self.calling_levels and self.planner.levels[self.current_location].direction_indicator[1] == False and self.planner.levels[self.current_location].direction_indicator[-1] == False:
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
        self.planner.levels[start_level].person_come(self, self.direction)
        print('New Passenger from', start_level, 'to', destination_level)
        self.press_button_call_cart()

    def press_button_call_cart(self):
        self.planner.passenger_calls_cart(self.start_level, self.direction)

    def press_button_destination(self, cart):
        if self.destination_level not in cart.pressed_levels and self.destination_level != cart.current_location:
            cart.pressed_levels.append(self.destination_level)


if __name__ == '__main__':
    stop_threads = False
    planner = Planner(5, 1)
    while True:
        try:
            lvl_from = int(input())
            lvl_to = int(input())
        except:
            planner.stopAll()
            break
        Person(lvl_from, lvl_to, planner)