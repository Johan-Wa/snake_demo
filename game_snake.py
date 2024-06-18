# ----------------- Imports ------------------
import curses
from curses import wrapper, textpad
from random import randint

from add_score import inpbox, save_score 

# ----------------- Classes ------------------
class SnakeGame():
    def __init__(self, name):
        self.name = name
        # Dimentions
        self.sh = 0 
        self.sw = 0

    def get_size(self,stdscr):
        return stdscr.getmaxyx()

    def create_food(self, snake, box):
        food = None
        
        while food is None:
            food = [randint(box[0][0] + 1, box[1][0] - 1),
                    randint(box[0][1] + 1, box[1][1] - 1)]
            if food in snake:
                food = None
        return food
        
    def main(self,stdscr):
        self.sh, self.sw = self.get_size(stdscr)
        curses.curs_set(0)

        # Giving no delay
        stdscr.nodelay(1)
        stdscr.timeout(150)

        # Screen height and wight
        sh = self.sh
        sw = self.sw

        # Create the area of the game
        box = [[3, 3], [sh - 3, sw - 3]]
        textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])

        # Define the snake
        snake = [[sh//2, sw//2 + 1],[sh//2, sw//2],[sh//2, sw//2 - 1]]
        direction = curses.KEY_RIGHT

        for y, x in snake:
            stdscr.addstr(y, x, '#')

        food = self.create_food(snake, box)
        stdscr.addstr(food[0], food[1], '*')

        score = 0
        score_text = f'Score: {score}'
        stdscr.addstr(2, sw//2 - len(score_text)//2, score_text )

        while 1:
            score_text = f'Score: {score}'
            stdscr.addstr(2, sw//2 - len(score_text)//2, score_text )
            key = stdscr.getch()
            match key:
                case 27:
                    break
                case curses.KEY_RIGHT | curses.KEY_UP | curses.KEY_DOWN | curses.KEY_LEFT:
                    direction = key
            head = snake[0]

            match direction:
                case curses.KEY_RIGHT:
                    new_head = [head[0], head[1] + 1]
                case curses.KEY_LEFT:
                    new_head = [head[0], head[1] - 1]
                case curses.KEY_UP:
                    new_head = [head[0] - 1, head[1]]
                case curses.KEY_DOWN:
                    new_head = [head[0] + 1, head[1]]

                    
            snake.insert(0, new_head)
            stdscr.addstr(new_head[0], new_head[1], '#')

            if snake[0] == food:
                food = self.create_food(snake, box)
                stdscr.addstr(food[0],food[1], '*')
                score += 1
            else:
                stdscr.addstr(snake[-1][0], snake[-1][1], ' ')
                snake.pop()


            # Define the lose condition
            if (snake[0][0] in [box[0][0], box[1][0]] or
                snake[0][1] in [box[0][1], box[1][1]] or
                snake[0] in snake[1:]):
                msg = "GAME OVER"
                stdscr.addstr(sh//2, sw//2 - len(msg)//2, msg)
                stdscr.nodelay(0)
                stdscr.getch()
                p_name = inpbox(stdscr, 'Save your score')
                save_score(p_name, score, 'scoreboard.txt')
                stdscr.refresh()
                break

            stdscr.refresh()
    def wrapp(self):
        wrapper(self.main)
        

# ----------------- Main ---------------------

if __name__ == "__main__":
    snake = SnakeGame('snaky')
    snake.wrapp()
