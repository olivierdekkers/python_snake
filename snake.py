import random
import curses


class Snake(object):

    def __init__(self, drawer, y_move, x_move):
        self.drawer = drawer
        self.movement_dic_y = y_move
        self.movement_dic_x = x_move
        self.prev_key =  list(self.movement_dic_x.keys())[2]
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
        self.direction={'up': curses.ACS_UARROW,
                        'left':curses.ACS_LARROW,
                        'right':curses.ACS_RARROW,
                        'down':curses.ACS_DARROW}


    def calc_direction(self, cord1, cord2):
        if cord1[0]<cord2[0]:
            return 'up'
        elif cord1[0]>cord2[0]:
            return 'down'

        if cord1[1]<cord2[1]:
            return 'left'
        elif cord1[1]>cord2[1]:
            return 'right'


    def get_snake(self):
         snake_body=curses.ACS_BLOCK

         directionHead = self.calc_direction(self.snake[0],self.snake[1])
         directionTail = self.calc_direction(self.snake[-1],self.snake[-2])
         snake_head=self.direction[directionHead]
         snake_tail=self.direction[directionTail]

         snake_head = ([self.snake[0]], snake_head)
         snake_body = (self.snake[1:-1], snake_body)
         snake_tail = ([self.snake[-1]], snake_tail)
         return (snake_head,snake_body,snake_tail)

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
            for body_part in self.get_snake():
                for location in body_part[0]:
                    self.drawer.addch(location[0], location[1], body_part[1])

    def remove_from_field(self):
        for location in self.snake:
            self.drawer.addch(location[0], location[1], ' ')
