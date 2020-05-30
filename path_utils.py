# Модуль описує пакет функцій, що будуть використані далі для роботи зі шляхами

def path_creator(data, path_common, new_path_common, max_weight, path_calculator_function, weight_calculator_function, duplicate_search_function, old_path_dictionary_converted={'path':[], 'C':0, 'weight':0, 'alive': None}):
  new_path_array = old_path_dictionary_converted['path'] + [new_path_common]
  
  # Додамо дані для внесення, використовуючи попередньо створені функції
  creator_addon = {'path' : new_path_array, 'C' : None, 'weight' : None, 'alive' : None}
  creator_addon['C'] = path_calculator_function(data, new_path_common, old_path_dictionary_converted['C'])
  creator_addon['weight'] = weight_calculator_function(data, new_path_common, old_path_dictionary_converted['C'], old_path_dictionary_converted['weight'])
  
  # шукати найкоротший шлях будемо методом виключення, виконуючи декілька вкоадених перевірок
  if creator_addon['weight'] < max_weight:
    duplicates = duplicate_search_function(path_common, new_path_array)
    
    if len(duplicates) == 0:
      creator_addon['alive'] = True
    
    # На даному етапі всі можливі дублікати будемо зменшувати:
    else:
      duplicates_simplified = list(filter(lambda x: x[0]['weight'] < creator_addon['weight'], duplicates))
      
      #  Перевіряємо варіант для найкоротшого шляху
      if len(duplicates_simplified) == 0:
        creator_addon['alive'] = True
        
        # І видаляємо усі повтори
        for dupl in duplicates:
          path_common[dupl[1]]['alive'] = False

      # Упс, шлях не найкоротший :(
      else: 
        creator_addon['alive'] = False
  
  else:
    creator_addon['alive'] = False

  return path_common + [creator_addon]

# Видаляємо шляхи із завищеними вагами
def big_weight_path_deleter(path_common, max_weight):
  new_path_common = [path_dictionary_converted if path_dictionary_converted['weight'] <= max_weight else
    {'path':path_dictionary_converted['path'], 'C':path_dictionary_converted['C'], 'weight':path_dictionary_converted['weight'], 'alive': False} for path_dictionary_converted in path_common]
  
  return new_path_common

# Шукаємо оптимальтний шлях (найкоротший) згідно ваг
def find_optimum_path_over_weight(data, path_common, max_weight, optimum_path):
  # Встановимо значення для подальшого оновлення
  max_weight_updated = max_weight
  optimum_path_updated = optimum_path

  # Виконаємо ітераційний пошук за шляхами
  if len(path_common[-1]['path']) == len(data):
    if path_common[-1]['alive'] == True:
      # Відповідно вкажемо показники для оновлення
      max_weight_updated = path_common[-1]['weight']
      optimum_path_updated = path_common[-1]['path']

  return max_weight_updated, optimum_path_updated

def path_inserter(data, path_common, new_path_addon, old_path_dictionary_converted, max_weight, optimum_path, path_calculator_function, weight_calculator_function, duplicate_search_function):
#   Оновимо шляхи та найбільший показник ваг
  path_common_updated = path_creator(data, path_common, new_path_addon, max_weight, path_calculator_function, weight_calculator_function, duplicate_search_function, old_path_dictionary_converted)
  max_weight_updated, optimum_path_updated = find_optimum_path_over_weight(data, path_common_updated, max_weight, optimum_path)
  
  if max_weight_updated != max_weight:
    path_common_updated = big_weight_path_deleter(path_common_updated, max_weight_updated)
  
  return path_common_updated, max_weight_updated, optimum_path_updated