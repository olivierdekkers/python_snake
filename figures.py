import random
import curses

class Snake_figure(object):

    def __init__(self, drawer, y_move, x_move):
        self.drawer = drawer
        self.movement_dic_y = y_move
        self.movement_dic_x = x_move
        self.prev_key = None
        self.undraw = []

    def init(self, sw_start, sw, sh_start, sh):
        self.sh_start = sh_start
        self.sh = sh
        self.sw_start = sw_start
        self.sw= sw
        snk_x = random.randint(self.sw_start, self.sw)
        snk_y = random.randint(self.sh_start, self.sh)
        self.snake= [
            [int(snk_y), int(snk_x)],
            [int(snk_y), int(snk_x-1)],
            [int(snk_y), int(snk_x-2)],
        ]

    def move(self,key):
        try:
            if key not in self.movement_dic_y:
                key = self.prev_key

            self.new_head = [self.snake[0][0], self.snake[0][1]]
            self.new_head= [self.new_head[0]+self.movement_dic_y[key], self.new_head[1] + self.movement_dic_x[key]]
            if self.new_head == self.snake[1]:
                self.new_head[0] = self.snake[0][0] + (self.snake[0][0] - self.snake[1][0])
                self.new_head[1] = self.snake[0][1] + (self.snake[0][1] - self.snake[1][1])
            self.snake.insert(0, self.new_head)
            self.prev_key = key
        except:
            pass

    def encounter_snakes(self, snakes):
        if self.snake[0][0] in [0, self.sh] or \
              self.snake[0][1] in [0, self.sw]:
                return True
        for snake in snakes:
             if self.snake[0] in snake.snake[1:]:
                    return True

        return False

    def encounter_food(self, food_locations):
        if self.snake[0] in food_locations:
            food_locations.remove(self.snake[0])
        else:
            self.undraw = [self.snake.pop()]
        return food_locations

    def draw(self):
        for x in self.undraw:
            self.drawer.addch(int(x[0]),int(x[1]), ' ')
        self.undraw = []
        for location in self.snake:
            self.drawer.addch(location[0], location[1],curses.ACS_CKBOARD)

    def remove_from_field(self):
        for location in self.snake:
            self.drawer.addch(location[0], location[1], ' ')
        
