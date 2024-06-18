# Display a menu for a game (snake in this case)
# Imports
import curses
from curses import color_pair, wrapper

import game_snake, scoreboard
# --------------------- Clases -----------------
class DisplayMenu():
    def __init__(self, name:str, menu:dict) -> None:
        self.name = name
        self.menu = menu

    def _print_menu(self, stdscr, selected_row_idx):
        # Clear the window
        stdscr.clear()
        stdscr.addstr(self.name)
        # Getting hight and wight of the screen
        h, w = stdscr.getmaxyx()
        
        # Obtain the mid of the screen to center the text
        for idx, row in enumerate(self.menu.keys()):
            x = w//2 - len(row)//2
            y = h//2 - len(self.menu)//2 + idx
            if idx == selected_row_idx:
                stdscr.attron(color_pair(1))
                stdscr.addstr(y, x, ' ' + row + ' ')
                stdscr.attroff(color_pair(1))
            else:
                stdscr.addstr(y, x, ' ' + row + ' ')
      
        stdscr.refresh()

    def menu_action(self, stdscr, menu_row):
        if menu_row in self.menu.keys() and menu_row != 'Exit':
            self.menu[menu_row].main(stdscr)
        else:
            self.menu[menu_row]()

    def main(self, stdscr):
        # set the cursor in position 0
        curses.curs_set(0)
        # Colors pairs
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

        # Initialize the selection
        current_row = 0

        # Print Menu
        self._print_menu(stdscr, current_row)


        while 1:
            key = stdscr.getch()
            stdscr.clear()

            match key:
                case curses.KEY_UP:
                    if current_row > 0:
                        current_row -=1
                case curses.KEY_DOWN:
                    if current_row < len(self.menu.keys())-1:
                        current_row +=1
                case 10 | curses.KEY_ENTER | 13:
                    stdscr.clear()
                    menu_act = list(self.menu.keys())
                    self.menu_action(stdscr, menu_act[current_row])
                    stdscr.refresh()

            self._print_menu(stdscr, current_row)

    def wrapp(self):
        wrapper(self.main)


# --------------------- Main --------------------

if __name__ == "__main__":
    menu_name = '''
    00       00
    0 0     0 0
    0  0   0  0   000   0       0    0
    0   0 0   0  0   0  00000   0    0
    0    0    0  0000   0    0  0    0
    0         0  0      0    0  0    0
    0         0   000   0    0   0000'''
    game = game_snake.SnakeGame('snaky')
    score_board = scoreboard.ScoreBoard('Score Board top 10','scoreboard.txt')
    menu_items = {'Play': game, 'Scoreboard': score_board, 'Exit':quit}
    menu = DisplayMenu(menu_name, menu_items)
    menu.wrapp()
