import random
import curses
from figures import Snake_figure

class Snake(object):

    def __init__(self, drawer):
        self.drawer = drawer
        self.snk_x = None
        self.snk_y = None
        self.snake= None
        self.new_head = None
        self.food = None
        self.food_len = 1
        self.number_of_snakes = 1

    def in_snakes(self, snake, snakes):
        for location in snake.snake:
            if location in [location for snakey in snakes for location in snakey.snake]:
                return True
        return False

    def init(self, sw, sh):
        self.sh = sh
        self.sw= sw
        self.food = [[int(self.sh/2), int(self.sw/2)]]
        self.snakes=[]
        while len(self.snakes) < self.number_of_snakes:
            up = self.drawer.getch()
            left = self.drawer.getch()
            down = self.drawer.getch()
            right = self.drawer.getch()
            self.movement_dic_y = {
                down : 1,
                up : -1,
                left : 0,
                right : 0
            }
            self.movement_dic_x = {
                down : 0,
                up :  0,
                left : -1,
                right : 1
            }
            snake = Snake_figure(self.drawer, self.movement_dic_y,self.movement_dic_x)
            snake.init(1,self.sw,1,self.sh)
            snake.prev_key = right
            while self.in_snakes(snake, self.snakes):
                snake=Snake(self.drawer)
            self.snakes.append(snake)
        while len(self.food) < self.food_len:
            nf = [ random.randint(1, self.sh-1), 
                   random.randint(1, self.sw-1)
                 ]
            if nf not in self.snakes and nf not in self.food:
                self.food.append(nf)


    def move(self,key):
        for snake in self.snakes:
            snake.move(key)
            if snake.encounter_snakes(self.snakes):
                snake.remove_from_field()
                self.snakes.remove(snake)
            self.food = snake.encounter_food(self.food)

        while len(self.food) < self.food_len:
            nf = [ random.randint(1, self.sh-1), 
                   random.randint(1, self.sw-1)
                 ]
            if nf not in [location for snake in self.snakes for location in snake.snake] and nf not in self.food:
                self.food.append(nf)

    def get_state(self):
        if len(self.snakes) == 0:
            return False
        else:
            return True

    def draw(self):
        for x in self.food:
            self.drawer.addch(int(x[0]),int(x[1]),curses.ACS_PI)
        for x in self.snakes:
            x.draw()
        for x in range(self.sw):
            self.drawer.addch(0,x,curses.ACS_CKBOARD)
            self.drawer.addch(int(self.sh),x,curses.ACS_CKBOARD)
        for x in range(self.sh):
            self.drawer.addch(x,0, curses.ACS_CKBOARD)
            self.drawer.addch(x,int(self.sw), curses.ACS_CKBOARD)
