import curses
from figures import Snake_figure
from game import Snake


class Driver(object):

    def __init__(self):
        self.game = None
        s = curses.initscr()
        curses.curs_set(0)
        self.sh , self.sw = s.getmaxyx()
        self.sh = int(self.sh/2)
        self.sw = int(self.sw / 2)
        self.drawer = curses.newwin(self.sh+1, self.sw+1, 0,0)
        self.drawer.keypad(1)


    def start(self):
        self.game.init(self.sw, self.sh)
        self.drawer.timeout(100)
        self.run()

    def run(self):
        key = curses.KEY_RIGHT
        while True:
            next_key = self.drawer.getch()
            key = key if next_key == -1 else next_key

            self.game.move(key)
            
            if self.game.get_state():
                self.game.draw()
            else:
                curses.endwin()
                quit()

driver = Driver()
driver.game = Snake(driver.drawer)
driver.game.food_len =5
driver.game.number_of_snakes = 2
driver.start()
