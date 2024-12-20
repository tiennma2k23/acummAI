import time
from agorithm.bfs_AI import *


def check(r, c):
    global table, num_cols, num_rows
    if (r < 0 or r == num_rows or c < 0 or c == num_cols):
        return False
    if (table[r][c] == '.'):
        return True
    else:
        return False


def print_table():
    global table
    print()
    for i in table:
        print(*i)


def move(r, c):
    print("move", r, c)
    global near, table, step, y, oritable
    step.append([r, c])
    if (check(r, c+y)):
        table[r][c+y] = "X"
        move(r, c+y)
    else:
        z = c
        if (c+y >= 0 and c+y < num_cols):
            z = c+y
        w = r
        while (check(r, z) == False and z+y >= 0 and z+y < num_cols):
            z += y
        if (check(r, z) == False or z == c):
            r += 1
            if (y == 1):
                z = num_cols-1
            else:
                z = 0
            y = -y
        while (check(r, z) == False and z >= 0 and z < num_cols):
            z += y
        if (check(r, z)):
            path = initialize_bfs(oritable, (w, c), (r, z))
            for i in path:
                step.append(i)
            move(r, z)


def initialize_SLAM(ta, st):
    global row, col, num_cols, num_rows, table, step, near, oritable, y
    oritable = ta
    row = st[0]
    col = st[1]
    num_rows = len(ta)
    num_cols = len(ta[0])
    step = []
    near = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    table = []
    for i in ta:
        tmp = []
        for j in i:
            if (j == 1):
                tmp.append('X')
            else:
                tmp.append('.')
        table.append(tmp)
    y = 1
    table[row][col] = "X"
    move(row, col)

    # print_table()
    return step
