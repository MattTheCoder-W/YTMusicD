#!/usr/bin/python3
import curses
import yt_dlp
from time import sleep

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
curses.curs_set(False)
rows, cols = stdscr.getmaxyx()

def on_resize():
    stdscr.clear()
    print_help(stdscr)

def update_size():
    global rows
    global cols
    nrows, ncols = stdscr.getmaxyx()
    if nrows != rows or ncols != cols:
        rows, cols = (nrows, ncols)
        on_resize()

def print_help(win):
    global rows
    global cols
    win.addstr(rows-2, 0, "a - add new link, d - delete selected link")
    win.addstr(rows-1, 0, "c - download, +/- - move links")
    win.refresh()

print_help(stdscr)
stdscr.addstr(0, 0, f"Current Window Size is {rows}, {cols}")
stdscr.refresh()

links = []
cursor = 0

while True:
    update_size()
    stdscr.addstr(0, 0, f"Current Window Size is {rows}, {cols}. Links: {len(links)}")
    for i in range(1, rows-2):
        stdscr.addstr(i, 0, " "*cols)
    for i, link in enumerate(links):
        text = f"[{i}] {link}"
        if cursor == i:
            stdscr.addstr(1+i, 0, text, curses.A_BOLD)
        else:
            stdscr.addstr(1+i, 0, text)

    stdscr.refresh()
    c = stdscr.getkey()
    if c == "q":
        break
    elif c == "a":
        stdscr.addstr(rows-3, 0, "URL: ")
        curses.echo()
        url = stdscr.getstr(rows-3, len("URL: "), 128)
        curses.noecho()
        stdscr.addstr(rows-3, 0, " "*cols)
        links.append(str(url.decode()))
    elif c == "d":
        while True:
            stdscr.addstr(rows-3, 0, " "*cols)
            stdscr.addstr(rows-3, 0, f"Delete {cursor}? [y/n]: ")
            curses.echo()
            answ = stdscr.getstr(rows-3, len(f"Delete {cursor}? [y/n]: "), 1)
            curses.noecho()
            if str(answ.decode()).lower() == "y":
                links.pop(cursor)
                break
            elif str(answ.decode()).lower() == "n":
                break
        stdscr.addstr(rows-3, 0, " "*cols)
    elif c == "+":
        if not cursor == len(links)-1:
            tomove = links[cursor]
            links[cursor] = links[cursor+1]
            links[cursor+1] = tomove
            cursor += 1
    elif c == "-":
        if not cursor == 0:
            tomove = links[cursor]
            links[cursor] = links[cursor-1]
            links[cursor-1] = tomove
            cursor -= 1
    elif c in ["KEY_UP", "k"]:
        cursor -= 1
        if cursor not in range(0, len(links)):
            cursor += 1
    elif c in ["KEY_DOWN", "j"]:
        cursor += 1
        if cursor not in range(0, len(links)):
            cursor -= 1



curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()