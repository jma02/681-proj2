constraint9x9 = set()
boxes = {
    1: [11,12,13,21,22,23,31,32,33],
    2: [14,15,16,24,25,26,34,35,36],
    3: [17,18,19,27,28,29,37,38,39],
    4: [41,42,43,51,52,53,61,62,63],
    5: [44,45,46,54,55,56,64,65,66],
    6: [47,48,49,57,58,59,67,68,69],
    7: [71,72,73,81,82,83,91,92,93],
    8: [74,75,76,84,85,86,94,95,96],
    9: [77,78,79,87,88,89,97,98,99],
}


def addRowArcs(row: int):
    for i in range(1,9):
        for j in range(i+1, 10):
            constraint9x9.add((int(f'{row}{i}'), int(f'{row}{j}')))
            constraint9x9.add((int(f'{row}{j}'), int(f'{row}{i}')))

def addColArcs(col: int):
    for i in range(1,9):
        for j in range(i+1, 10):
            constraint9x9.add((int(f'{i}{col}'), int(f'{j}{col}')))
            constraint9x9.add((int(f'{j}{col}'), int(f'{i}{col}')))

def addBoxArcs(box: int):
    for i in range(0,8):
        for j in range(i + 1, 9):
            fst = boxes[box][i]
            snd = boxes[box][j]
            constraint9x9.add((fst, snd))
            constraint9x9.add((snd, fst))

for i in range(1,10):
    addRowArcs(i)
    addColArcs(i)
    addBoxArcs(i)

with open('new_sudoku_constraint9x9.py', 'w') as f:
    f.write('constraint9x9 = {\n')
    for constraint in sorted(constraint9x9):
        f.write(f"    {constraint},\n")
    f.write('}')