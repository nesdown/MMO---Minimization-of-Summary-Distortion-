import sys
import math

import file_reader as fr
import path_creator as pc
import path_utils as pu
import calculation_generator as cg
import duplicate_searcher as ds

sampleTasks = [ {'l':5,  'D':30, 'a':8,  'b':2},
                {'l':13, 'D':19, 'a':3,  'b':2},
                {'l':17, 'D':11, 'a':10, 'b':4},
                {'l':3,  'D':27, 'a':6,  'b':4}]

def start_processing(data_file):
  data = fr.read_file(data_file)

  # Встановимо найбільше можливе значення для ваги
  max_weight = sys.maxsize
  optimum_path = None
  path_common = []

  path_common = pc.start_path_generator(data, path_common, cg.weight_calculator)

  while len(list(filter(lambda path_dictionary_converted: (path_dictionary_converted['alive'] == True) and (len(path_dictionary_converted['path']) < len(data)), path_common))) > 0:
    
    short_path_dictionary_converted = sorted(path_common, key=lambda path: path['weight'])[0]
    path_common.remove(short_path_dictionary_converted)
    
    removed_connections = [i for i in range(len(data))  if short_path_dictionary_converted['path'].count(i) == 0]
    
    for connection in removed_connections:
      path_common, max_weight, optimum_path = pu.path_inserter(data, path_common, connection, short_path_dictionary_converted, max_weight, optimum_path, cg.paths_calculator, cg.weight_calculator, ds.duplicate_searcher)

  maximum_solutions = math.factorial(len(data))
  unexplored_percentage = (maximum_solutions - len(path_common)) / maximum_solutions * 100
  
  result = ""
  paths_string = ""

  for path in path_common:
    result = result + 'Шлях: {}, Вага: {}, C: {}'.format([x+1 for x in path['path']], path['weight'], path['C']) + "\n"
  
  # for x in optimum_path:
  result = result + '\nВага найкращого шляху: ' +  str(max_weight)
  result = result + '\nНайкращий шлях: ' + str([x+1 for x in optimum_path])
  result = result + '\n% Відсічення: ' + '{}%'.format(int(unexplored_percentage))

  return result