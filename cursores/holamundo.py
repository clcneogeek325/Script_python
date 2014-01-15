#!/usr/bin/python
# -*- coding: utf-8 -*-

import curses

def main(stdscr):
    stdscr.addstr('hola mundo cirsores')
    stdscr.getch()

if __name__ == '__main__':
	curses.wrapper(main)
