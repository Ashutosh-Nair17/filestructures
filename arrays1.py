import json

# open output file for reading
with open('listfile.txt', 'r') as filehandle:
    basicList = json.load(filehandle)

print(basicList)