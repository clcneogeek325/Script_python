#!/usr/bin/python
# -*- coding: utf-8 -*-

import curses

def main(stdscr):
    win = curses.newwin(1, 20, 10, 20);
    win.addstr('hello world')
    win.getch()

if __name__ == '__main__':
    curses.wrapper(main)
