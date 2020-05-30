#DONE#implement test (> task)
#DONE#implement cut off (same pasth, diff weight)
#Read from file maybe

import sys
import math
import json

sampleTasks = [ {'l':5,  'D':30, 'a':8,  'b':2},
                {'l':13, 'D':19, 'a':3,  'b':2},
                {'l':17, 'D':11, 'a':10, 'b':4},
                {'l':3,  'D':27, 'a':6,  'b':4}]


def getDuplicates(pathsStorage, pathArr):
  #duplicates[0] - pathDict, duplicates[1] - pos in paths
  # print(pathsStorage, '||', pathArr)
  unfiltered = map(lambda path: (path, pathsStorage.index(path)) if (sorted(path['path']) == sorted(pathArr)) else False, pathsStorage)
  # print(list(unfiltered))
  return (list(filter(lambda x: x != False, unfiltered)))

def newCCalc(tasks, newPathAddition, oldC):
  return oldC + tasks[newPathAddition]['l']

def newWeightCalc(tasks, newPathAddition, oldC, oldWeight):
  timeDiff = (oldC + tasks[newPathAddition]['l']) - tasks[newPathAddition]['D']
  if timeDiff > 0:#past deadline
    return tasks[newPathAddition]['b'] * timeDiff + oldWeight
  elif timeDiff < 0:#pre deadline
    return tasks[newPathAddition]['a'] * abs(timeDiff) + oldWeight

#step 1
def createStartingPaths(tasks, pathsStorage):
  newPathsStorage = []
  for i in range(len(tasks)):
    toApp = {'path':[], 'C':0, 'weight':0, 'alive': True}
    toApp['path'].append(i)
    toApp['C'] = tasks[i]['l']
    toApp['weight'] = newWeightCalc(tasks, i, 0, 0)
    newPathsStorage.append(toApp)
  return newPathsStorage

#make list of tasks not in pathArr, iterate through them to add

def insertPath(tasks, pathsStorage, newPathAddition, oldPathDict, maxWeight, bestPath):
  newPathsStorage = addPath(tasks, pathsStorage, newPathAddition, maxWeight, oldPathDict)
  newMaxWeight, newBestPath = updateMaxWeightBestPath(tasks, newPathsStorage, maxWeight, bestPath)
  if newMaxWeight != maxWeight:
    newPathsStorage = removeOverweightPaths(newPathsStorage, newMaxWeight)
  return newPathsStorage, newMaxWeight, newBestPath

#get newPathAddition
def addPath(tasks, pathsStorage, newPathAddition, maxWeight, oldPathDict={'path':[], 'C':0, 'weight':0, 'alive': None}):
  newPathArr = oldPathDict['path'] + [newPathAddition]
  # print('NEWPATHARR: ', newPathArr)
  toAdd = {'path':newPathArr, 'C':None, 'weight':None, 'alive': None}
  toAdd['C'] = newCCalc(tasks, newPathAddition, oldPathDict['C'])
  toAdd['weight'] = newWeightCalc(tasks, newPathAddition, oldPathDict['C'], oldPathDict['weight'])
  if toAdd['weight'] < maxWeight:#if within allowed weight
    duplicates = getDuplicates(pathsStorage, newPathArr)
    if len(duplicates) == 0:#unique path
      toAdd['alive'] = True
    else:
      shorterDuplicates = list(filter(lambda x: x[0]['weight'] < toAdd['weight'], duplicates))
      if len(shorterDuplicates) == 0:#this is the shortest path
        toAdd['alive'] = True
        #delete duplicate:
        for dupl in duplicates:
          pathsStorage[dupl[1]]['alive'] = False
          # del pathsStorage[dupl[1]] - mark False not delete
      else:#this is not the shortest path  
        toAdd['alive'] = False
  else:#Too heavy
    toAdd['alive'] = False
  return pathsStorage + [toAdd]

def updateMaxWeightBestPath(tasks, pathsStorage, maxWeight, bestPath):
  newMaxWeight = maxWeight
  newBestPath = bestPath
  if len(pathsStorage[-1]['path']) == len(tasks):#full path found
    if pathsStorage[-1]['alive'] == True:
      newMaxWeight = pathsStorage[-1]['weight']
      newBestPath = pathsStorage[-1]['path']
      # pathsStorage[-1]['alive'] = False - cannot cause effiecency calc depends on it
  return newMaxWeight, newBestPath

def removeOverweightPaths(pathsStorage, maxWeight):
  # for i in range(len(pathsStorage)):
  #   if pathsStorage[i]['weight'] >= maxWeight:
  #     pathsStorage[i]['alive'] = False
  newPathsStorage = [pathDict if pathDict['weight'] <= maxWeight else
    {'path':pathDict['path'], 'C':pathDict['C'], 'weight':pathDict['weight'], 'alive': False} for pathDict in pathsStorage]
  return newPathsStorage

def readFile(filename):
  with open(filename, 'r') as file:
    return json.load(file)

def main():
  tasks = []
  if len(sys.argv) > 1:#input file specified
    tasks = readFile(sys.argv[1])
  else:
    tasks = sampleTasks

  maxWeight = 1000000#sufficiently large value
  bestPath = None
  pathsStorage = []

  pathsStorage = createStartingPaths(tasks, pathsStorage)

  while len(list(filter(lambda pathDict: (pathDict['alive'] == True) and (len(pathDict['path']) < len(tasks)), pathsStorage))) > 0:#there are alive banches that are not complete
    # print('------------------------------------------')
    lightestDict = sorted(pathsStorage, key=lambda path: path['weight'])[0]
    pathsStorage.remove(lightestDict)
    # print('oldPathDict: ', oldPathDict)
    # unusedNodes = [node for node in lightestDict['path'] if tasks.count(node) == 0]
    unusedNodes = [i for i in range(len(tasks))  if lightestDict['path'].count(i) == 0]
    # print('lightestDict: ', lightestDict, ' || unusedNodes: ', unusedNodes)
    for node in unusedNodes:
      pathsStorage, maxWeight, bestPath = insertPath(tasks, pathsStorage, node, lightestDict, maxWeight, bestPath)

  maxSolutions = math.factorial(len(tasks))
  percentUnexplored = (maxSolutions - len(pathsStorage)) / maxSolutions * 100
  
  print('Resulting solutions:\n')
  for path in pathsStorage:
    print('Path: {}, Weight: {}, C: {}'.format([x+1 for x in path['path']], path['weight'], path['C']))
  print('\n')
  print('Best Path Weight: ', maxWeight)
  print('Best Path: ', [x+1 for x in bestPath])
  print('Leaves cut off: ', '{}%'.format(percentUnexplored))

main()
print('===================================================================')
print('TO READ A TASK FROM FILE USE (file must be formated in valid JSON):')
print('python Branch&Bound.py file')
print('sample file sample.txt included')