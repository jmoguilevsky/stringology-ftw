import random

text = []
for i in range(4):
    for c in range(70):
        text += [chr(c + 65)] * 5000
print(''.join(text))
