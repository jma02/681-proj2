constraint4x4 = set()
boxes = {
    1: [11, 12, 21, 22], 
    2: [13, 14, 23, 24], 
    3: [31, 32, 41, 42], 
    4: [33, 34, 43, 44]
}



def addRowArcs(row: int):
    for i in range(1,4):
        for j in range(i+1, 5):
            constraint4x4.add((int(f'{row}{i}'), int(f'{row}{j}')))
            constraint4x4.add((int(f'{row}{j}'), int(f'{row}{i}')))

def addColArcs(col: int):
    for i in range(1,4):
        for j in range(i+1, 5):
            constraint4x4.add((int(f'{i}{col}'), int(f'{j}{col}')))
            constraint4x4.add((int(f'{j}{col}'), int(f'{i}{col}')))

def addBoxArcs(box: int):
    for i in range(0,3):
        for j in range(i + 1, 4):
            fst = boxes[box][i]
            snd = boxes[box][j]
            constraint4x4.add((fst, snd))
            constraint4x4.add((snd, fst))

for i in range(1,5):
    addRowArcs(i)
    addColArcs(i)
    addBoxArcs(i)

with open('sudoku_constraint4x4.py', 'w') as f:
    f.write('constraint4x4 = {\n')
    for constraint in sorted(constraint4x4):
        f.write(f"    {constraint},\n")
    f.write('}')