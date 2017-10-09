def compare(s, pattern, startingPos):
    i = 0
    patternLength = len(pattern)
    textLength = len(s)
    # print('comparing:', s[startingPos + i], pattern[i])
    # print('length', patternLength)
    while (i < patternLength and startingPos + i < textLength  and s[startingPos + i] == pattern[i]):
        # print('char:', startingPos + i, s[startingPos + i])
        i += 1
    if i == len(pattern):
        return 0
    return -1 if startingPos + i == textLength or s[startingPos + i] < pattern[i] else 1


def recursiveSearch(s, SA, pattern, startingPos, endingPos, leftSide):
    original = endingPos if leftSide else startingPos
    # if leftSide:
        # print('recurse', 'original', original, 'startingPos', startingPos, 'endingPos', endingPos)

    while startingPos <= endingPos:
        # if leftSide:
            # print('recurse 2', 'original', original, 'startingPos', startingPos, 'endingPos', endingPos)
        midpoint = (startingPos + endingPos) // 2
        comp = compare(s, pattern, SA[midpoint])
        if (comp == 0):
            if (leftSide):
                endingPos -= 1
            else:
                startingPos += 1
        elif (comp > 0):
            endingPos = midpoint - 1
        else:
            startingPos = midpoint + 1

    return original - endingPos if leftSide else startingPos - original


def findAllOccurrences(s, SA, pattern):
    if (pattern == ''):
        return []
    starting = 0
    ending = len(s) - 1
    found = False

    while starting <= ending:
        midpoint = (starting + ending) // 2
        # print('midpoint', midpoint)
        comp = compare(s, pattern, SA[midpoint])
        # print('comp', comp)
        if (comp == 0):
            leftSide = midpoint - \
                recursiveSearch(s, SA, pattern, 0, midpoint - 1, True)
            rightSide = midpoint + \
                recursiveSearch(s, SA, pattern, midpoint + 1, len(s) - 1, False) + 1
            # print('leftSide', leftSide)
            return SA[leftSide: rightSide]
        elif (comp > 0):
            ending = midpoint - 1
        else:
            starting = midpoint + 1

    return []


def main():
    strings = ['na', 'a', 'ana', 'bana', 'ban', 'baa', '$']
    s = 'banana'
    SA = [5, 3, 1, 0, 4, 2]
    for pattern in strings:
        res = findAllOccurrences(s, SA, pattern)
        print(pattern, res)
    
if __name__ == '__main__':
    main()
