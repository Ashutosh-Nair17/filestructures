import json

# define list with values
basicList = [[1], ["Town"], [4.6],["lol"]]

# open output file for writing
with open('listfile.txt', 'w') as filehandle:
    json.dump(basicList, filehandle)