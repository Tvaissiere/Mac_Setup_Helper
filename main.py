import curses
import subprocess

brew_install = ["node","python","llvm","openjdk","git","docker","postgresql","ollama"]
brew_install_cask = ["visual-studio-code","pycharm","intellij-idea","webstorm","clion","spyder","sublime-text","android-studio","arduino-ide","xcode","docker","postman","wireshark","gimp","inkscape","blender","arc","google-chrome","warp","iterm2","xampp","autopsy","lm-studio","chatgpt","microsoft-word","microsoft-excel","microsoft-powerpoint","microsoft-outlook","microsoft-onenote"]

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

def brew_options_select(stdscr, question, options):
    curses.curs_set(0)
    selected_index = 0
    selected_items = set()
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, question)
        for i, option in enumerate(options):
            checkbox = "[x]" if i in selected_items else "[ ]"
            line = f"{checkbox} {option}"
            if i == selected_index:
                stdscr.addstr(i + 2, 0, line, curses.A_REVERSE)
            else:
                stdscr.addstr(i + 2, 0, line)
        key = stdscr.getch()
        if key == curses.KEY_UP:
            selected_index = (selected_index - 1) % len(options)
        elif key == curses.KEY_DOWN:
            selected_index = (selected_index + 1) % len(options)
        elif key == ord(" "):
            if selected_index in selected_items:
                selected_items.remove(selected_index)
            else:
                selected_items.add(selected_index)
        elif key in (10, 13):
            return [options[i] for i in selected_items]
        stdscr.refresh()


def run_brew_options_select(question, options):
    return curses.wrapper(brew_options_select, question, options)

def main(brew_install):
    homebrew_installed = (run_menu("Do you have Homebrew already installed?", ["Yes I do", "No I don't", "I don't know"]))
    if homebrew_installed == 0:
        selection = []
        selection = (run_brew_options_select("Please select which command line applications and languages you wish to install (space to select), when done press enter", brew_install))
        for i in range(len(selection)):
            subprocess.run("brew install " + selection[i], shell=True, check=True)
    elif homebrew_installed == 1:
        subprocess.run('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"', shell=True, check=True)
    else:
        brew_check = (subprocess.run('brew --version', shell=True, check=True, capture_output=True))
        if "Homebrew" in str(brew_check.stdout):
            print("Homebrew Installed")
        else:
            # TODO: Check if this works (I have homebrew and don't want to remove XD)
            install_homebrew = (run_menu("Could not detect Homebrew, would you like to install it? ", "Yes", "No"))
            if install_homebrew == 0:
                subprocess.run('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"', shell=True, check=True)
            else:
                print("Sorry, this script requires Homebrew")

main(brew_install)