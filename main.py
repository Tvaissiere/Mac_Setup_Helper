import curses
import subprocess

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
    homebrew_installed = (run_menu("Do you have Homebrew already installed?", ["Yes I do", "No I don't", "I don't know"]))
    if homebrew_installed == 0:
        pass
    elif homebrew_installed == 1:
        subprocess.run('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"', shell=True, check=True)
    else:
        brew_check = subprocess.run('brew --version', shell=True, capture_output=True, text=True)
        if brew_check.returncode == 0 and "Homebrew" in brew_check.stdout:
            print("Homebrew Installed")
        else:
            install_homebrew = run_menu("Could not detect Homebrew, would you like to install it? ", ["Yes", "No"])
            if install_homebrew == 0:
                subprocess.run('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"', shell=True, check=True)
            else:
                print("Sorry, this script requires Homebrew")
    
main()
