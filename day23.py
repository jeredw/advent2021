#!/usr/bin/env python3

from datetime import datetime
import heapq

test = [[c for c in line.strip('\n')]
        for line in open('day23-test.txt').readlines()]
data = [[c for c in line.strip('\n')]
        for line in open('day23-input.txt').readlines()]
test2 = [[c for c in line.strip('\n')]
         for line in open('day23-test2.txt').readlines()]
data2 = [[c for c in line.strip('\n')]
         for line in open('day23-input2.txt').readlines()]

room_column = {'A': 3, 'B': 5, 'C': 7, 'D': 9}
def dest_in_room(grid, p):
  i = room_column[p] 
  for j in range(len(grid)-2, 1, -1):
    if grid[j][i] == '.':
      return (j,i)
    if grid[j][i] != p:
      return

def moves(grid):
  for j in range(len(grid)):
    for i in range(len(grid[j])):
      p = grid[j][i]
      if p not in 'ABCD': continue
      if j == 1:  # move from hallway into room
        dest = dest_in_room(grid, p)
        if dest and is_hallway_clear(grid, i, dest[1]):
          yield p, j, i, dest[0], dest[1]
      else:  # move from room into hallway if not blocked
        if grid[j-1][i] != '.': continue
        for dest in ((1,1),(1,2),(1,4),(1,6),(1,8),(1,10),(1,11)):
          if is_hallway_clear(grid, i, dest[1]):
            yield p, j, i, dest[0], dest[1]

def is_hallway_clear(grid, x0, x1):
  assert x0 != x1
  dx = 1 if x1 > x0 else -1
  x = x0
  while True:
    x += dx
    if grid[1][x] != '.': return False
    if x == x1: return True

def make_move(move, grid):
  p, from_y, from_x, to_y, to_x = move
  new_grid = [row[:] for row in grid]
  new_grid[from_y][from_x] = '.' 
  new_grid[to_y][to_x] = p
  return new_grid

def print_grid(grid):
  for j in range(len(grid)):
    s = ''
    for i in range(len(grid[j])):
      s += grid[j][i]
    print(s)

def done(grid):
  for j in range(len(grid)-2, 1, -1):
    if grid[j][3] != 'A': return False
    if grid[j][5] != 'B': return False
    if grid[j][7] != 'C': return False
    if grid[j][9] != 'D': return False
  return True

cost_per_step = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

def cost(move):
  p, from_y, from_x, to_y, to_x = move
  steps = abs(from_x-to_x) + abs(from_y-to_y)
  return cost_per_step[p] * steps

def prune(grid, move):
  p, from_y, from_x, to_y, to_x = move
  i = room_column[p]
  return from_x == i and all(grid[j][i] == p for j in range(from_y+1, len(grid)-1))

def hashable(grid):
  return ''.join(''.join(row) for row in grid)

def search(grid):
  q = [(0, 0, grid)]
  visited = set()
  while q:
    cur_sort, cur_cost, cur_grid = heapq.heappop(q)
    visited.add(hashable(cur_grid))
    if done(cur_grid):
      return cur_cost
    for move in moves(cur_grid):
      if not prune(cur_grid, move):
        new_grid = make_move(move, cur_grid)
        if hashable(new_grid) in visited: continue
        new_cost = cur_cost + cost(move)
        new_sort = new_cost + estimate_remaining_cost(new_grid)
        heapq.heappush(q, (new_sort, new_cost, new_grid))
  return -1

def blocking(grid, p, j0, i):
  return any(grid[j][i] != p for j in range(j0+1, len(grid)-1))

def estimate_remaining_cost(grid):
  cost = 0 
  for j in range(len(grid)):
    for i in range(len(grid[j])):
      p = grid[j][i]
      cost += (j+abs(i-3)        if p == 'A' and i != 3 else
               j                 if p == 'A' and i == 3 and blocking(grid, p, j, i) else
               10*(j+abs(i-5))   if p == 'B' and i != 5 else
               10*j              if p == 'B' and i == 5 and blocking(grid, p, j, i) else
               100*(j+abs(i-7))  if p == 'C' and i != 7 else
               100*j             if p == 'C' and i == 7 and blocking(grid, p, j, i) else
               1000*(j+abs(i-9)) if p == 'D' and i != 9 else
               1000*j            if p == 'D' and i == 9 and blocking(grid, p, j, i) else
               0)
  return cost

def time(fn):
  start = datetime.now()
  result = fn()
  end = datetime.now()
  print(f'{result}  (took {end-start})')

time(lambda: search(data2))
time(lambda: search(test2))