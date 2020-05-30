# В рамках ціжї функції ми вносимо пакет задач і початковий набір шляхів, 
# і за допомогою анонімної функції вагів виконуємо формування оновленого пакету 
# результуючих даних. 

def start_path_generator(data, path_amount, weight_function): #weight_function - анонімна функція
  
  new_path_amount = []

  # Ітеруємо за вказівником довжини масиву
  for i in range(len(data)):
    result_provider = {'path':[], 'C':0, 'weight':0, 'alive': True}
    result_provider['path'].append(i)
    result_provider['C'] = data[i]['l']
    result_provider['weight'] = weight_function(data, i, 0, 0)

    new_path_amount.append(result_provider)
  
  return new_path_amount