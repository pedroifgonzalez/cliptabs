#!/usr/bin/env python3

"""Paste using multiple clipboard tabs"""

import sys
import os
import time
import functools
import tkinter
import threading

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path + os.path.sep + 'lib')

import pyperclip
from pynput import keyboard
from pynput.mouse import Listener
from model import Tooltip

BTN_HEIGHT = 38
ACTIVE_BACKGROUND_COLOR = "lightgreen"
BACKGROUND = "white"

gui = tkinter.Tk(className='ClipTabs')
gui.geometry("200x200-30-50")
gui.resizable(False, False)
pixelVirtual = tkinter.PhotoImage(width=200, height=1)

kb = keyboard.Controller()
keys = keyboard.Key
TABS = ('tab1','tab2','tab3','tab4')
tabs = dict(tab1='', tab2='', tab3='', tab4='')
cursor = 0
lock = threading.Lock()
mouse_moving = False

def tab_action(tab):
    global tabs, lock
    content = tabs[tab]
    if content:
        with lock:
            pyperclip.copy(content)
            change_window_and_paste()

def reduce_label(label):
    return label[:12]+" ..."+label[-7:]

def handle_focus_in(event):
    global gui
    if event.widget == gui:
        gui.wm_attributes('-alpha',1.0)

def handle_focus_out(event):
    global gui
    if event.widget == gui:
        gui.wm_attributes('-alpha',0.1)

tab1_action = functools.partial(tab_action, tab='tab1')
tab2_action = functools.partial(tab_action, tab='tab2')
tab3_action = functools.partial(tab_action, tab='tab3')
tab4_action = functools.partial(tab_action, tab='tab4')

tab1 = tkinter.Button(gui, text = ' ', image=pixelVirtual,
                    height=BTN_HEIGHT,compound="c",
                    background=BACKGROUND,
                    activebackground=ACTIVE_BACKGROUND_COLOR, command = tab1_action)

tab2 = tkinter.Button(gui, text = ' ', image=pixelVirtual,
                    height=BTN_HEIGHT,compound="c",
                    background=BACKGROUND,
                    activebackground=ACTIVE_BACKGROUND_COLOR, command = tab2_action)

tab3 = tkinter.Button(gui, text = ' ', image=pixelVirtual,
                    height=BTN_HEIGHT,compound="c",
                    background=BACKGROUND,
                    activebackground=ACTIVE_BACKGROUND_COLOR, command = tab3_action)

tab4 = tkinter.Button(gui, text = ' ', image=pixelVirtual,
                    height=BTN_HEIGHT,compound="c",
                    background=BACKGROUND,
                    activebackground=ACTIVE_BACKGROUND_COLOR, command = tab4_action)

tab_buttons = [tab1, tab2, tab3, tab4]

tab1.pack()
tab2.pack()
tab3.pack()
tab4.pack()

def update_tabs_text():
    global tabs, TABS, tab_buttons, cursor, lock, mouse_moving

    while True:
        if lock.locked() is False and mouse_moving:
            pyperclip_content = pyperclip.paste()

            if pyperclip_content not in tabs.values():
                tabs[TABS[cursor]] = pyperclip_content

                if len(pyperclip_content)>=23:
                    pyperclip_content = reduce_label(pyperclip_content)
                    t1 = Tooltip(tab_buttons[cursor], tabs[TABS[cursor]])
                    tab_buttons[cursor].bind('<FocusIn>', t1.enter)

                tab_buttons[cursor]['text'] = pyperclip_content
                gui.wm_attributes('-alpha',1.0)
                tab_buttons[cursor].config(bg=ACTIVE_BACKGROUND_COLOR)
                time.sleep(1)
                gui.wm_attributes('-alpha',0.1)
                tab_buttons[cursor].config(bg=BACKGROUND)
                cursor += 1

            if cursor>3:
                cursor = 0

def change_window_and_paste():
    with kb.pressed(keys.alt):
        kb.press(keys.tab)
        kb.release(keys.tab)

    time.sleep(0.8)

    with kb.pressed(keys.ctrl):
        kb.press('v')
        kb.release('v')

def mouse_is_moving(x,y):
    global mouse_moving
    mouse_moving = True

mouse_listener = Listener(on_move=mouse_is_moving)
read_clipboard = threading.Thread(target=update_tabs_text, daemon=True)
icon = "@" + dir_path + os.path.sep + "bitmaps.xmb"

if __name__ == "__main__":
    # gui.wait_visibility(gui)
    # gui.wm_attributes('-alpha',0.1)
    gui.bind("<Enter>", lambda *ignore: gui.wm_attributes('-alpha',1.0))
    gui.bind("<Leave>", lambda *ignore: gui.wm_attributes('-alpha',0.1))
    # gui.iconbitmap(icon)
    gui.bind("<Escape>", lambda *ignore: gui.destroy())
    mouse_listener.start()
    read_clipboard.start()
    gui.mainloop()
