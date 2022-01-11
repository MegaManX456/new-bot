import numpy as np
import time
import pyautogui as pag
import win32api,win32con
import keyboard
import subprocess as sp
#-------------------------------------------------------
CREATE_NO_WINDOW = 0x08000000
engine = sp.Popen('pbrain-em&bryo21_e.exe',stdin = sp.PIPE,stdout = sp.PIPE,stderr = sp.PIPE\
                  ,bufsize = 1,universal_newlines= True,creationflags = CREATE_NO_WINDOW)
engine.stdin.write('start 15\n')
print(engine.stdout.readline())
infos = ('max_memory 500000000',
         'timeout_turn 60000',
         'timeout_match 60000',
         'time_left 60000','rule 1')
for info in infos:
    engine.stdin.write(f"info {info}\n")
def receive():
    while True:
        line = engine.stdout.readline().strip()
        if 'D' not in line and 'M' not in line:
            return line
def turn(x,y):
    engine.stdin.write(f"turn {x},{y}\n")
    return receive()
def begin():
    engine.stdin.write('begin\n')
    return receive()
def undo(move1,move2):
    engine.stdin.write(f'takeback {move1[0]},{move1[1]}\n')
    engine.stdout.readline()
    print(f'{move1} taken back')
    engine.stdin.write(f'takeback {move2[0]},{move2[1]}\n')
    engine.stdout.readline()
    print(f'{move2} taken back')
def kill():
    engine.stdin.write('end\n')
    engine.kill()

##-------------------------------------------------------
board_x = [284, 322, 360, 398, 436, 474, 512, 550, 588, 626, 664, 702, 740, 778, 816]

board_y = [666, 628, 590, 552, 514, 476, 438, 400, 363, 325, 287, 249, 211, 173, 135]
undo_pos = (1009,289)
'''
for i in range(len(board_y)//2):
    t = board_y[i]
    board_y[i] = board_y[-i-1]
    board_y[-i-1] = t
    '''
def click(x,y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
def str_to_xy(string):
    x = int(string.split(',')[0])
    y = int(string.split(',')[1])
    return x,y
def lgs(data):
    for i in range(len(data)):
        rule = [[1, 0], [0, 1], [1, -1], [1, 1]]
        for rx, ry in rule:
            lst = [data[i]]
            if (lst[0][0] + rx * 4, lst[0][1] + ry * 4) not in data or \
               (lst[0][0] + rx * 3, lst[0][1] + ry * 3) not in data or \
               (lst[0][0] + rx * 2, lst[0][1] + ry * 2) not in data or \
               (lst[0][0] + rx * 1, lst[0][1] + ry * 1) not in data \
               or (lst[0][0] + rx * 5, lst[0][1] + ry * 5) in data or (lst[0][0] - rx, lst[0][1] - ry) in data:
                continue
            else:
                return True
    return False
def opp_go_first():
    list_of_moves = []
    while True:
        board = pag.screenshot()
        if board.getpixel(undo_pos)[0]==34 and board.getpixel(undo_pos)[1]==34:
            click(undo_pos[0],undo_pos[1])
            print(f'undo was pressed and undo moves r {list_of_moves[-2]},{list_of_moves[-1]}')
            undo(list_of_moves[-2],list_of_moves[-1])
            del list_of_moves[-2:]
            print(f'current list: {list_of_moves}')
        for x_cord,x_screen in enumerate(board_x):
            for y_cord,y_screen in enumerate(board_y):
                if (x_cord,y_cord) not in list_of_moves and \
                   board.getpixel((x_screen,y_screen))[0] == 255 and \
                       board.getpixel((x_screen,y_screen))[1] == 0 :
                    print(f'opp move is: {x_cord,y_cord}')
                    output = turn(x_cord,y_cord)
                    list_of_moves.append((x_cord,y_cord))
                    print(f'current list: {list_of_moves}')
                    x,y = str_to_xy(output)
                    print(f'bot move is: {x,y}')
                    list_of_moves.append((x,y))
                    print(f'current list: {list_of_moves}')
                    click(board_x[x],board_y[y])
                    if lgs(list_of_moves[1::2]) == True:
                        print('match has ended')
                        engine.stdin.write('restart\n')
                        receive()
                        return list_of_moves

def me_go_first():
    list_of_moves = []
    first_move=begin()
    x,y = str_to_xy(first_move)
    list_of_moves.append((x,y))
    click(board_x[x],board_y[y])
    while True:
        board = pag.screenshot()
        if board.getpixel(undo_pos)[0]==34 and board.getpixel(undo_pos)[1]==34:
            click(undo_pos[0],undo_pos[1])
            print(f'undo was pressed and undo moves r {list_of_moves[-2]},{list_of_moves[-1]}')
            undo(list_of_moves[-2],list_of_moves[-1])
            del list_of_moves[-2:]
            print(f'current list: {list_of_moves}')
        for x_cord,x_screen in enumerate(board_x):
            for y_cord,y_screen in enumerate(board_y):
                if (x_cord,y_cord) not in list_of_moves and \
                   board.getpixel((x_screen,y_screen))[0] == 255 and \
                       board.getpixel((x_screen,y_screen))[1] == 0 :
                    print(f'opp move is: {x_cord,y_cord}')
                    output = turn(x_cord,y_cord)
                    list_of_moves.append((x_cord,y_cord))
                    print(f'current list: {list_of_moves}')
                    x,y = str_to_xy(output)
                    print(f'bot move is: {x,y}')
                    list_of_moves.append((x,y))
                    print(f'current list: {list_of_moves}')
                    click(board_x[x],board_y[y])
                    
                    if lgs(list_of_moves[::2]) == True:
                        print('match has ended')
                        engine.stdin.write('restart\n')
                        receive()
                        
                        return list_of_moves

        
keyboard.add_hotkey('alt+1',me_go_first)
keyboard.add_hotkey('alt+2',opp_go_first)







                
