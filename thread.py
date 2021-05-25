import sys, os, psutil

sys.path.append(os.path.dirname(os.path.abspath(__file__))+os.path.sep+"lib")

import pynput, model, pyperclip


p = psutil.Process(os.getpid())
p.nice(10)
clips = model.Cola()

COPY_COMBINATION = {pynput.keyboard.Key.ctrl, pynput.keyboard.KeyCode.from_char('c')}
PASTE_COMBINATION = {pynput.keyboard.Key.ctrl, pynput.keyboard.KeyCode.from_char('v')}

current = set()

def on_press(key):
    try:
        if key in COPY_COMBINATION:
            current.add(key)
            if all(k in current for k in COPY_COMBINATION):
                print('Tried to copy')
                if(not(clips.isThere(pyperclip.paste()))):
                	clips.addElement(pyperclip.paste())
                for elem in range(0, clips.getLength()):
                    print(clips.getElementByPos(elem))

        if key in PASTE_COMBINATION:
            current.add(key)
            if all(k in current for k in PASTE_COMBINATION):
                print("Tried to paste")
                a = int(os.popen("pidof cp").read())
                os.system("ps")
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    try:
        current.remove(key)
    except KeyError:
        pass

# Collect events until released
with pynput.keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
listener = pynput.keyboard.Listener(
    on_press=on_press,
    on_release=on_release)

listener.start()
