from rubiks.lib.consts import *
import numpy as np
from matplotlib import pyplot as plt, colors

def get_color(side):
    if side == WHITE:
        return "White"
    if side == RED:
        return "Red"
    if side == ORANGE:
        return "Orange"
    if side == YELLOW:
        return "Yellow"
    if side == GREEN:
        return "Green"
    if side == BLUE:
        return "Blue"

def get_matching_idx(pos):
    """
    Find the indicies of the piece on the facing side
    :param pos:
    :return:
    """

    color = pos[2]
    pos = tuple(pos[0:2])
    if pos == (1,1):
        raise ValueError("cannot get opposite side of center face")

    if color == WHITE:
        if pos == (0,0):
            return [0,2,BLUE,LEFT], [2,0,RED,UP]
        elif pos == (0,1):
            return [2,1,RED,UP], None
        elif pos == (0,2):
            return [2,2,RED,UP], [0,0,GREEN,RIGHT]
        elif pos == (1,0):
            return [1,2,BLUE,LEFT], None
        elif pos == (1,2):
            return [1,0,GREEN,RIGHT], None
        elif pos == (2,0):
            return [2,2,BLUE,LEFT], [0,0,ORANGE,DOWN]
        elif pos == (2,1):
            return [0,1,ORANGE,DOWN], None
        elif pos == (2,2):
            return [0,2,ORANGE,DOWN], [2,0,GREEN,RIGHT]
    elif color == RED:
        if pos == (2,0):
            return [0,2,BLUE,LEFT], [0,0,WHITE,DOWN]
        elif pos == (2,1):
            return [0,1,WHITE,DOWN], None
        elif pos == (2,2):
            return [0,2,WHITE,DOWN], [0,0,GREEN,RIGHT]
        elif pos == (1,0):
            return [0,1,BLUE,LEFT], None
        elif pos == (1,2):
            return [0,1,GREEN,RIGHT], None
        elif pos == (0,0):
            return [0,0,BLUE,LEFT], [0,2,YELLOW,UP]
        elif pos == (0,1):
            return [0,1,YELLOW,UP], None
        elif pos == (0,2):
            return [0,2,GREEN,RIGHT], [0,0,YELLOW,UP]
        pass
    elif color == ORANGE:
        if pos == (0,0):
            return [2,0,WHITE,UP], [2,2,BLUE,LEFT]
        elif pos == (0,1):
            return [2,1,WHITE,UP], None
        elif pos == (0,2):
            return [2,2,WHITE,UP], [2,0,GREEN,RIGHT]
        elif pos == (1,0):
            return [2,1,BLUE,LEFT], None
        elif pos == (1,2):
            return [2,1,GREEN,RIGHT], None
        elif pos == (2,0):
            return [2,0,BLUE,LEFT], [2,2,YELLOW,DOWN]
        elif pos == (2,1):
            return [2,1,YELLOW,DOWN], None
        elif pos == (2,2):
            return [2,2,GREEN,RIGHT], [2,0,YELLOW,DOWN]
    elif color == YELLOW:
        if pos == (0,0):
            return [0,2,GREEN,LEFT], [0,2,RED,UP]
        elif pos == (0,1):
            return [0,1,RED,UP], None
        elif pos == (0,2):
            return [0,0,RED,UP], [0,0,BLUE,RIGHT]
        elif pos == (1,0):
            return [1,2,GREEN,LEFT], None
        elif pos == (1,2):
            return [1,0,BLUE,RIGHT], None
        elif pos == (2,0):
            return [2,2,GREEN,LEFT], [2,2,ORANGE,DOWN]
        elif pos == (2,1):
            return [2,1,ORANGE,DOWN], None
        elif pos == (2,2):
            return [2,0,ORANGE,DOWN], [2,0,BLUE,RIGHT]
    elif color == GREEN:
        if pos == (0,0):
            return [0,2,WHITE,LEFT], [2,2,RED,UP]
        elif pos == (0,1):
            return [1,2,RED,UP], None
        elif pos == (0,2):
            return [0,2,RED,UP], [0,0,YELLOW,RIGHT]
        elif pos == (1,0):
            return [1,2,WHITE,LEFT], None
        elif pos == (1,2):
            return [1,0,YELLOW,RIGHT], None
        elif pos == (2,0):
            return [2,2,WHITE,LEFT], [0,2,ORANGE,DOWN]
        elif pos == (2,1):
            return [1,2,ORANGE,DOWN], None
        elif pos == (2,2):
            return [2,2,ORANGE,DOWN], [2,0,YELLOW,RIGHT]
    elif color == BLUE:
        if pos == (0,0):
            return [0,0,RED,UP], [0,2,YELLOW,LEFT]
        elif pos == (0,1):
            return [1,0,RED,UP], None
        elif pos == (0,2):
            return [0,0,WHITE,RIGHT],[2,0,BLUE,UP]
        elif pos == (1,0):
            return [1,2,YELLOW,LEFT], None
        elif pos == (1,2):
            return [1,0,WHITE,RIGHT], None
        elif pos == (2,0):
            return [2,2,YELLOW,LEFT], [2,0,ORANGE,DOWN]
        elif pos == (2,1):
            return [1,0,ORANGE,DOWN], None
        elif pos == (2,2):
            return [2,0,WHITE,RIGHT], [0,0,ORANGE,DOWN]
    else:
        raise ValueError("Invalid color")


def move(actions, func):
    lst = []
    add_to_last = False
    for c in actions:
        if c == ".":
            add_to_last = True
        elif c == '\n':
            break
        else:
            lst.append(c)
            if add_to_last:
                lst[-1] = '.' + str(lst[-1])
            add_to_last = False


    rets = []
    for action in lst:
        if action.isnumeric():
            rets.append(func(action))
        else:
            action_num = actionDict[action]
            rets.append(func(action_num))

    return rets

def rotate_state(state):
    state[:, :, WHITE] = np.rot90(state[:, :, WHITE], k=3)
    tmp = np.copy(state[:, :, RED])
    state[:, :, RED] = np.rot90(state[:, :, BLUE], k=3)
    state[:, :, BLUE] = np.rot90(state[:, :, ORANGE], k=3)
    state[:, :, ORANGE] = np.rot90(state[:, :, GREEN], k=3)
    state[:, :, GREEN] = np.rot90(tmp, k=3)
    state[:, :, YELLOW] = np.rot90(state[:, :, YELLOW], k=1)

    return np.array(state)

def rotate_state_rev(state):
    state[:, :, WHITE] = np.rot90(state[:, :, WHITE], k=1)
    tmp = np.copy(state[:, :, RED])
    state[:, :, RED] = np.rot90(state[:, :, GREEN], k=1)
    state[:, :, GREEN] = np.rot90(state[:, :, ORANGE], k=1)
    state[:, :, ORANGE] = np.rot90(state[:, :, BLUE], k=1)
    state[:, :, BLUE] = np.rot90(tmp, k=1)
    state[:, :, YELLOW] = np.rot90(state[:, :, YELLOW], k=3)

    return np.array(state)

def rotate_state_about_left(state):
    state[:,:,BLUE] = np.rot90(state[:,:,BLUE], k=3)
    state[:,:,GREEN] = np.rot90(state[:,:,GREEN], k=1)
    tmp = np.copy(state[:,:,WHITE])
    state[:,:,WHITE] = state[:,:,RED]
    state[:,:,RED] = np.flipud(np.fliplr(state[:,:,YELLOW]))
    state[:,:,YELLOW] = np.flipud(np.fliplr(state[:,:,ORANGE]))
    state[:,:,ORANGE] = tmp
    return np.array(state)

def rotate_state_about_right(state):
    state[:,:,BLUE] = np.rot90(state[:,:,BLUE], k=1)
    state[:,:,GREEN] = np.rot90(state[:,:,GREEN], k=3)
    tmp = np.copy(state[:,:,WHITE])
    state[:,:,WHITE] = state[:,:,ORANGE]
    state[:,:,ORANGE] = np.flipud(np.fliplr(state[:,:,YELLOW]))
    state[:,:,YELLOW] = np.flipud(np.fliplr(state[:,:,RED]))
    state[:,:,RED] = tmp
    return np.array(state)

def vis_state(state, ax=None):
    image = np.full((9, 12), 6)
    image[3:6, 0:3] = state[:, :, BLUE]  ## Blue side
    image[3:6, 3:6] = state[:, :, WHITE]  ## White side
    image[3:6, 6:9] = state[:, :, GREEN]  ## Green Side
    image[3:6, 9:12] = state[:, :, YELLOW]  ## Yellow side
    image[0:3, 3:6] = state[:, :, RED]  ## red side
    image[6:9, 3:6] = state[:, :, ORANGE]  ## orange side
    cmap = {WHITE: 'white', RED: 'red', ORANGE: 'orange', YELLOW: 'yellow', GREEN: 'green', BLUE: 'blue'}

    colorList = list(cmap.values()) + ["black"]
    cmape = colors.ListedColormap(colorList)

    if ax is None:
        ax = plt.gca()

    ax.imshow(image, cmap=cmape)
    ax.text(4, 4, 'U', fontsize='x-large', horizontalalignment='center', fontweight='bold',
             verticalalignment='center')
    ax.text(1, 4, 'L', fontsize='x-large', horizontalalignment='center', fontweight='bold',
             verticalalignment='center')
    ax.text(4, 1, 'B', fontsize='x-large', horizontalalignment='center', fontweight='bold',
             verticalalignment='center')
    ax.text(7, 4, 'R', fontsize='x-large', horizontalalignment='center', fontweight='bold',
             verticalalignment='center')
    ax.text(10, 4, 'D', fontsize='x-large', horizontalalignment='center', fontweight='bold',
             verticalalignment='center')
    ax.text(4, 7, 'F', fontsize='x-large', horizontalalignment='center', fontweight='bold',
             verticalalignment='center')

    if ax is None:
        plt.axis('off')

    return ax
