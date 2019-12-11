import sys
from itertools import product
import pandas as pd
import neal

#######################################################################
# I referd to the following website for writing this program.         #
#   https://quantum.fixstars.com/techresouces/application/sudoku/     #
#######################################################################

class Sudoku:
  def __init__(self, initialCondition):
    self.selectList = dict()
    for i, j in product(range(9), range(9)):
      if (initialCondition[i])[j*4+2] == '1': self.selectList[(i,j)] = [1,0,0,0,0,0,0,0,0]
      if (initialCondition[i])[j*4+2] == '2': self.selectList[(i,j)] = [0,1,0,0,0,0,0,0,0]
      if (initialCondition[i])[j*4+2] == '3': self.selectList[(i,j)] = [0,0,1,0,0,0,0,0,0]
      if (initialCondition[i])[j*4+2] == '4': self.selectList[(i,j)] = [0,0,0,1,0,0,0,0,0]
      if (initialCondition[i])[j*4+2] == '5': self.selectList[(i,j)] = [0,0,0,0,1,0,0,0,0]
      if (initialCondition[i])[j*4+2] == '6': self.selectList[(i,j)] = [0,0,0,0,0,1,0,0,0]
      if (initialCondition[i])[j*4+2] == '7': self.selectList[(i,j)] = [0,0,0,0,0,0,1,0,0]
      if (initialCondition[i])[j*4+2] == '8': self.selectList[(i,j)] = [0,0,0,0,0,0,0,1,0]
      if (initialCondition[i])[j*4+2] == '9': self.selectList[(i,j)] = [0,0,0,0,0,0,0,0,1]
      if (initialCondition[i])[j*4+2] == ' ': self.selectList[(i,j)] = [1,1,1,1,1,1,1,1,1]
    self.check()
    self.show()
    self.q = dict()

  def preAnnealing(self):
    isContinue = True
    while isContinue:
      updatedCount = 0
      for i, j in product(range(9), range(9)):
        for _ in self.searchConnect(i,j):
          (i2, j2) = _
          if self.selectList[(i2,j2)].count(1) == 1:
            _ = self.selectList[(i2,j2)].index(1)
            if (self.selectList[(i,j)])[_] == 1:
              (self.selectList[(i,j)])[_] = 0
              updatedCount += 1
              if self.selectList[(i,j)].count(1) == 0:
                print(f'#ERROR(no number): i={i+1} j={j+1}')
                self.show()
                sys.exit()

      if updatedCount == 0:
        isContinue = False 
    self.show()

  def genQubo(self):
    # xijk = 1 (number k is selected for row i, column j)
    # xijk = 0 (otherwise)

    # select just one number from  selectable numbers p, ... q for (i,j)
    #
    # (xijp + ... + xijq - 1)**2

    for i, j in product(range(9), range(9)):
      _ = self.klist(i, j)
      if len(_) == 1: continue
      for k1, k2 in product(_, _):
        if k1 == k2: self.addValueToQubo(((i, j, k1), (i, j, k2)), -1)
        if k1 <  k2: self.addValueToQubo(((i, j, k1), (i, j, k2)),  2)

    # do not select same number for each (i1,j1) and (i2,j2)
    #   (i1,j1), (i2,j2) belong to same row or column or 3x3 subgrids
    #   p, ... q  : common　selectable numbers for (i1,j1) and (i2,j2) 
    #
    # xi1j1p * xi2j2p + ... + xi1j1q * xi2j2q

    for i1, j1 in product(range(9), range(9)):
      for _ in self.searchConnect(i1,j1):
        (i2, j2) = _
        if (i2, j2) < (i1, j1): continue;
        for k1, k2 in product(self.klist(i1, j1), self.klist(i2, j2)):
          if k1 == k2:
            self.addValueToQubo(((i1, j1, k1), (i2, j2, k2)), 1) 

  def show(self):
    for i in range(9):
      line1 = '|'
      for j in range(9):
        str1 = '   |'
        if self.selectList[(i,j)] == [1,0,0,0,0,0,0,0,0]: str1 = ' 1 |'
        if self.selectList[(i,j)] == [0,1,0,0,0,0,0,0,0]: str1 = ' 2 |'
        if self.selectList[(i,j)] == [0,0,1,0,0,0,0,0,0]: str1 = ' 3 |'
        if self.selectList[(i,j)] == [0,0,0,1,0,0,0,0,0]: str1 = ' 4 |'
        if self.selectList[(i,j)] == [0,0,0,0,1,0,0,0,0]: str1 = ' 5 |'
        if self.selectList[(i,j)] == [0,0,0,0,0,1,0,0,0]: str1 = ' 6 |'
        if self.selectList[(i,j)] == [0,0,0,0,0,0,1,0,0]: str1 = ' 7 |'
        if self.selectList[(i,j)] == [0,0,0,0,0,0,0,1,0]: str1 = ' 8 |'
        if self.selectList[(i,j)] == [0,0,0,0,0,0,0,0,1]: str1 = ' 9 |'
        if self.selectList[(i,j)] == [0,0,0,0,0,0,0,0,0]: str1 = ' ! |'
        line1 = line1 + str1
      print(line1)
    print('++++++++++++++++++++++++++++++++++++++++++++++')

  def check(self):
    for i, j in product(range(9), range(9)):
      if self.selectList[(i,j)].count(1) != 1:
        continue
      for _ in self.searchConnect(i,j):
        (i2, j2) = _
        if self.selectList[(i,j)] == self.selectList[(i2,j2)]:
          print(f'#ERROR(same number): i={i+1} j={j+1} i2={i2+1} j2={j2+1}')
          self.show()
          sys.exit()

  def searchConnect(self,i,j):
    list1 = []
    for i2, j2 in product(range(9), range(9)): 
      if (i,j) != (i2,j2):
        if i == i2:
          list1.append((i2,j2))
        elif j == j2:
          list1.append((i2,j2))
        elif (int(i/3) == int(i2/3)) and (int(j/3) == int(j2/3)):
          list1.append((i2,j2))
    return list1

  def addValueToQubo(self, _key, _val):
    if _key in self.q.keys():
      self.q[_key] += _val
    else:
      self.q[_key] = _val

  def klist(self, i, j):
    _list = []
    for k in range(9):
      if self.selectList[(i, j)][k] == 1:
        _list.append(k)
    return _list

  def mergeAnnealingResult(self, result):
    for key, value in result.items():
      if value == 0:
        (i, j, k) = key
        (self.selectList[(i,j)])[k] = 0       
    self.check()
    self.show()
    self.q = dict()

# main routine

initialCondition = [
  '| 2 |   | 5 | 1 | 3 |   |   |   | 4 |',
  '|   |   |   |   | 4 | 8 |   |   |   |',
  '|   |   |   |   |   | 7 |   | 2 |   |',
  '|   | 3 | 8 | 5 |   |   |   | 9 | 2 |',
  '|   |   |   |   | 9 |   | 7 |   |   |',
  '|   |   |   |   |   |   | 4 | 5 |   |',
  '| 8 | 6 |   | 9 | 7 |   |   |   |   |',
  '| 9 | 5 |   |   |   |   |   | 3 | 1 |',
  '|   |   | 4 |   |   |   |   |   |   |',
]

#initialCondition = [
#  '|   |   |   |   |   |   |   |   | 1 |',
#  '|   |   | 2 | 1 |   |   | 9 | 6 |   |',
#  '|   |   |   | 6 | 5 |   | 7 |   |   |',
#  '| 6 |   |   | 2 |   | 1 |   |   | 3 |',
#  '|   |   | 9 | 4 | 8 |   |   | 5 |   |',
#  '| 7 |   |   |   |   |   |   | 2 |   |',
#  '|   |   | 8 |   |   |   |   |   |   |',
#  '| 2 | 1 |   | 8 |   |   |   |   | 7 |',
#  '|   | 7 |   | 5 |   | 4 |   |   |   |',
#]

#initialCondition = [
#  '|   |   |   |   |   |   |   |   |   |',
#  '|   |   |   |   |   |   |   |   |   |',
#  '|   |   |   |   |   |   |   |   |   |',
#  '|   |   |   |   |   |   |   |   |   |',
#  '|   |   |   |   |   |   |   |   |   |',
#  '|   |   |   |   |   |   |   |   |   |',
#  '|   |   |   |   |   |   |   |   |   |',
#  '|   |   |   |   |   |   |   |   |   |',
#  '|   |   |   |   |   |   |   |   |   |',
#]

sudoku = Sudoku(initialCondition)
sudoku.preAnnealing()
sudoku.genQubo()

sampler = neal.SimulatedAnnealingSampler()
response = sampler.sample_qubo(sudoku.q, num_reads=20)

sudoku.mergeAnnealingResult(response.first.sample)

