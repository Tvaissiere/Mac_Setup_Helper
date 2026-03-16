import curses

def menu(stdscr, question, options):
    curses.curs_set(0)
    selected = 0
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, question)
        for i, option in enumerate(options):
            if i == selected:
                stdscr.addstr(i + 2, 0, option, curses.A_REVERSE)
            else:
                stdscr.addstr(i + 2, 0, option)
        key = stdscr.getch()
        if key == curses.KEY_UP:
            selected = (selected - 1) % len(options)
        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % len(options)
        elif key == 10:
            return selected
        stdscr.refresh()

def run_menu(question, options):
    return curses.wrapper(menu, question, options)

def main():
    run_menu("Do you have Homebrew already installed?", ["Yes I do", "No I don't", "I don't know"])
    
main()