WHITE=0
RED=1
ORANGE=2
YELLOW=3
GREEN=4
BLUE=5

color_vals = {
        0: "W",
        1: "R",
        2: "O",
        3: "Y",
        4: "G",
        5: "B"
}


UP=0
DOWN=1
LEFT=2
RIGHT=3

actionDict = {
            'f':  0, # orange
            'r':  1, # green
            'l':  2, # blue
            'u':  3, # white
            'd':  4, # yellow
            'b':  5, # red
            '.f': 6,
            '.r': 7,
            '.l': 8,
            '.u': 9,
            '.d': 10,
            '.b': 11
        }

actionDictInv = {val:key for key,val in actionDict.items()}

actionList = [
        'f',
        'r',
        'l',
        'u',
        'd',
        'b',
        '.f',
        '.r',
        '.l',
        '.u',
        '.d',
        '.b'
]