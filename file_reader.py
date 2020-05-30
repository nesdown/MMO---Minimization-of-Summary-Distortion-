import json

def read_file(filename):
  with open(filename, 'r') as file:
    return json.load(file)