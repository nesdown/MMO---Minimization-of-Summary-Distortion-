# Цей пакет функцій призначений для пошуку дублікатів у наборі шляхів,
# Що згенеровані з віхдного файлу.

def duplicate_searcher(path_amount, path_array):
  unfiltered = map(lambda path: (path, path_amount.index(path)) if (sorted(path['path']) == sorted(path_array)) else False, path_amount)
  return (list(filter(lambda x: x != False, unfiltered)))

