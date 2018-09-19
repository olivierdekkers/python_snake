import random
import curses

s = curses.initscr()
curses.curs_set(0)
sh , sw = s.getmaxyx()
w = curses.newwin(sw, sw, 0,0)
w.keypad(1)
w.timeout(100)

snk_x = sw/4
snk_y = sh/2
snake = [
    [snk_y, snk_x],
    [snk_y, snk_x-1],
    [snk_y, snk_x-2]
]

food = [int(sh/2), int(sw/2)]

print(food)
w.addch(food[0], food[1], curses.ACS_PI)

key = curses.KEY_RIGHT


while True:
    next_key = w.getch()
    key = key if next_key == -1 else next_key

    if snake[0][0] in [0, sh] or snake[0][1] in [0, sw] or snake[0] in snake[1:]:
        curses.endwin()
        quit()

    new_head = [snake[0][0], snake[0][1]]

    movement_dic_y = {
        curses.KEY_DOWN : 1,
        curses.KEY_UP : -1,
        curses.KEY_LEFT : 0,
        curses.KEY_RIGHT : 0
    }
    movement_dic_x = {
        curses.KEY_DOWN : 0,
        curses.KEY_UP :  0,
        curses.KEY_LEFT : -1,
        curses.KEY_RIGHT : 1
    }

    new_head = [new_head[0] + movement_dic_y[key], new_head[1] + movement_dic_x[key]]

    snake.insert(0, new_head)

    if snake[0] == food:
        food = None
        while food is None:
            nf = [ random.randint(1, sh-1), 
                   random.randint(1, sw-1)
                 ]
            food = nf if nf not in snake else None

        w.addch(food[0], food[1], curses.ACS_PI)
    else:
        tail = snake.pop()
        w.addch(int(tail[0]), int(tail[1]), ' ')

    w.addch(int(snake[0][0]), int(snake[0][1]), curses.ACS_CKBOARD)
