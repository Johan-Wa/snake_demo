import curses
from curses import wrapper
# -------------- Classes ---------------
class ScoreBoard():
    def __init__(self, name, file) -> None:
        self.name = name
        self.score_file = file
    
    def _get_score_list(self):
        with open(self.score_file) as f:
            s_list = f.readlines()
        s_list = [ [i.split(',')[0], i.split(',')[1]] for i in s_list]
        return s_list


    def main(self,stdscr):
        curses.curs_set(0)
        sh , sw = stdscr.getmaxyx()
        score_list = self._get_score_list()
        y = sh//2 - len(score_list)//2

        stdscr.clear()
        stdscr.addstr(self.name)
        for i in score_list[:10]:
            text = f"{i[0]} _____ {i[1]}"
            x = sw//2 - len(text)
            stdscr.addstr(y, x, text)
            y += 1
        stdscr.refresh()
        stdscr.getch()

    def wrapp(self):
        wrapper(self.main)

# --------------- Main -----------------
if __name__ == "__main__":
    score = ScoreBoard('Score Board','scoreboard.txt')
    score.wrapp()
