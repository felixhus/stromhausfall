path = 'test_file.txt'

with open(path, 'r') as file:
    text = file.read()

length = len(text)
print(length)
