def paths_calculator(data, path_addon, old_path):
  return old_path + data[path_addon]['l']

def weight_calculator(data, path_addon, old_path, old_weight):
  difference_period = (old_path + data[path_addon]['l']) - data[path_addon]['D']

  # Генерація результату для переходу після "дедлайну"
  if difference_period > 0:#past deadline
    return data[path_addon]['b'] * difference_period + old_weight

  # Генерація результату для переходу до "дедлайну"
  elif difference_period < 0:
    return data[path_addon]['a'] * abs(difference_period) + old_weight

  else:
      raise Exception("Період різниці є нулем - схоже, у вхідних даних допущено помилку.")