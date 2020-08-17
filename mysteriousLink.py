import os

try: input = raw_input
except NameError: pass

dragNDrop = ""

if dragNDrop == '':
    fileName = input("Input the file with extension> ")
else:
    fileOnly = dragNDrop.rfind('\\') + 1
    fileName = dragNDrop[fileOnly:]

with open(fileName, 'rU') as f:
  for line in f:
    brexit = line.index('|')
    titleID = line[:brexit]
    name = line[brexit+1:]
    os.system("ez_dlc.py " + titleID.strip())