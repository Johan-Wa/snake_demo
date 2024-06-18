import curses
from curses import wrapper
from os import write

# Add Window
def inpbox(scr, prompt):
    ''' Generates a screen tha capture the text entry of the user and return it.
    Praramns:
        -scr --> a screen object (stdscr, pad or win)
        -promt --> a string that is showed in the generated window
    Returns:
        -The string ingrssed by the user
    '''
    scr.clear()
    scr.refresh()
 
    # Parent window
    width = 42
    height = 5
    top = (curses.LINES - height) // 2
    left = (curses.COLS - width) // 2
    box = curses.newwin(height, width, top, left)
    box.bkgd(curses.color_pair(2))
    box.border()
    box.addstr(0, 2,' ' + prompt + ' ')
    box.refresh()
   
    # Input box
    txt = curses.newwin(1, width - 4, top + height - 2, left + 2)
    txt.bkgd(curses.color_pair(1))
    txt.refresh()
    txt.keypad(1)
    curses.echo()
    new = txt.getstr().decode('UTF-8')
    curses.noecho()
 
    scr.clear()
    scr.refresh()
    return new

def save_score(name, score, file):
    with open(file, 'a') as f:
        f.write(f'{name},{score}')
    with open(file, 'r') as f:
        data = f.readlines()
    with open(file, 'w') as f:
        try:
            data = sorted(data, key=lambda x: int(x.split(',')[1]), reverse=True )
            #data.sort(key=lambda x: x.split(',')[1], reverse=True)
            for i in data:
                if i[-1] == '\n':
                    f.write(i)
                else:
                    f.write(i + '\n')
        finally:
            pass

# ---------------------- Main -------------------
def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    inpbox(stdscr, "Prueba")

if __name__ == "__main__":
    pass

