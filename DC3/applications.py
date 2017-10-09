def compare(s, pattern, startingPos, textLength, patternLength):
    i = 0
    # print('comparing:', s[startingPos + i], pattern[i])
    # print('length', patternLength)
    while (i < patternLength and startingPos + i < textLength  and s[startingPos + i] == pattern[i]):
        # print('char:', startingPos + i, s[startingPos + i])
        i += 1
    if i == patternLength:
        return 0
    return -1 if startingPos + i == textLength or s[startingPos + i] < pattern[i] else 1


def recursiveSearch(s, SA, pattern, startingPos, endingPos, leftSide, textLength, patternLength):
    original = endingPos if leftSide else startingPos
    # if leftSide:
        # print('recurse', 'original', original, 'startingPos', startingPos, 'endingPos', endingPos)
    times = 0
    while startingPos <= endingPos:
        times += 1
        # if leftSide:
            # print('recurse 2', 'original', original, 'startingPos', startingPos, 'endingPos', endingPos)
        midpoint = (startingPos + endingPos) // 2
        comp = compare(s, pattern, SA[midpoint], textLength, patternLength)
        if (comp == 0):
            if (leftSide):
                endingPos = midpoint - 1
            else:
                startingPos = midpoint + 1
        elif (comp > 0):
            endingPos = midpoint - 1
        else:
            startingPos = midpoint + 1

    # print('recursed', times)
    return original - endingPos if leftSide else startingPos - original


def findAllOccurrences(s, SA, pattern):
    if (pattern == ''):
        return 0, 0
    textLength = len(s)
    patternLength = len(pattern)
    starting = 0
    ending = textLength - 1
    found = False

    while starting <= ending:
        midpoint = (starting + ending) // 2
        # print('midpoint', midpoint)
        comp = compare(s, pattern, SA[midpoint], textLength, patternLength)
        # print('comp', comp)
        if (comp == 0):
            leftSide = midpoint - \
                recursiveSearch(s, SA, pattern, 0, midpoint - 1, True, textLength, patternLength)
            rightSide = midpoint + \
                recursiveSearch(s, SA, pattern, midpoint + 1, textLength - 1, False, textLength, patternLength) + 1
            # print('leftSide', leftSide)
            return leftSide, rightSide
        elif (comp > 0):
            ending = midpoint - 1
        else:
            starting = midpoint + 1

    return 0, 0


def main():
    strings = ['na', 'a', 'ana', 'bana', 'ban', 'baa', '$']
    s = 'banana'
    SA = [5, 3, 1, 0, 4, 2]
    for pattern in strings:
        res = findAllOccurrences(s, SA, pattern)
        print(pattern, res)
    
if __name__ == '__main__':
    main()
