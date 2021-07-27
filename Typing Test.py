# ToDo: Don't count incorrectly typed words

import keyboard as kb, win32api, winsound, random, time, tkinter as tk, winsound as ws
from pynput import keyboard

def pickagain():
    global noofwords
    noofwords = int(input('No. of words? [Between 10 and 10000]: '))
    if not noofwords in range(10, 10001):
        print('Sorry ,invalid range. Pick again...\n')
        pickagain()
    else:
        play()

def play():
    global i, incorrectct, remaining, starttime, endtime, incorrectchars
    specialchars = [
    'alt_l', 'backspace', 'correct', 'ctrl_l', 'delete', 'end', 'enter', 'esc', 'home',\
    'insert', 'num_lock', 'page_down', 'page_up', 'print_screen', 'shift', 'shift_r',\
    'tab', 'f1', 'f12', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', '_',
    'left', 'up', 'down', 'right', 'media_play_pause', 'media_volume_mute', 'media_volume_up', 'media_volume_down', None, 'cmd', 'caps_lock'
    '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '~', '`', '_', '+', '-', '+', '|', '\\', '/', '?', '"', "'", '<', '>', ',', '.', ';', ':',\
    '[', ']', '{', '}'
    ]

    with open(r"D:\AI Training Text Files\Project Gutenberg's Frankenstein, by Mary Wollstonecraft (Godwin) Shelley.txt", 'r', encoding = 'utf-8-sig') as f:
        content = f.read()
        alphacontent = ''.join(x for x in content if x.isalpha() or x == ' ' or x == '\n').replace('\n', ' ')
        words = alphacontent.split()

    words = [i for i in words if len(i) > 4]
    random.shuffle(words)
    out = ' _ '.join(words[:noofwords])

    sentence = out
    sentence = sentence.replace('\n', ' ')
    print(sentence+'\n')

    sentence = sentence.replace('_ ', '')
    words = sentence.split(' ')
    remainingwords = sentence.split()
    rawin = []
    remaining = list(sentence)
    incorrectct = 0
    incorrectchars = []

    i = remaining[0]
    wordtimes = []

    def on_press(key):
        global i, incorrectct, remaining, starttime, endtime
        try:
            k = key.char # single-char keys
        except:
            k = key.name # other keys
            if key == keyboard.Key.space:
                k = ' '
        rawin.append(key)
        if k == i:  # correct key entered
            del remaining[0]
            if len(remaining) == len(sentence)-1:
                starttime = time.time()
            if k == ' ':
                wordtimes.append(time.time())
                del words[0]

        else:   # incorrect key entered
            if not k in specialchars:
                incorrectct += 1
                incorrectchars.append(k)
                print('Incorrect "'+k+'" instead of '+i)
        try:
            i = remaining[0]
        except:
            i = sentence[-1]

        if remaining == [] or k == keyboard.Key.esc:
            wordtimes.append(time.time())
            endtime = time.time()
            words.pop()
            return False  # stop listener

    listener = keyboard.Listener(on_press=on_press)
    listener.start()  # start to listen on a separate thread
    listener.join()  # remove if main thread is polling self.keys

    precision = 5
    worddurations = [(wordtimes[n]-wordtimes[n-1]) for n in range(1, len(wordtimes))]
    #print(worddurations)
    del worddurations[0] #Don't count duration to type the first word [discard this value]
    avgwordduration = sum(worddurations)/len(worddurations)

    TIME = endtime - starttime
    sTIME = (str(TIME).split('.')[0]+'.'+str(TIME).split('.')[1][:precision])

    CPS = len(sentence)/float(sTIME)
    sCPS = (str(CPS).split('.')[0]+'.'+str(CPS).split('.')[1][:precision])

    CPM = float(CPS)*60
    sCPM = (str(CPM).split('.')[0]+'.'+str(CPM).split('.')[1][:precision])

    WPM = CPM/5
    sWPM = (str(WPM).split('.')[0]+'.'+str(WPM).split('.')[1][:precision])

    print('\n\n')
    print('CPS:', sCPS)
    print('CPM:', sCPM)
    print('TIME TAKEN:', sTIME, 's')
    print('Incorrect attempts:', incorrectct)
    print('WPM', sWPM)

    print()
    print('Incorrect chars:', incorrectchars)

    #print(locals().keys())

pickagain()
