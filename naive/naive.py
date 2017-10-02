def naiveFind(pattern, text):
    if (len(pattern) > len(text)):
        return False

    for i in range(len(text) - len(pattern) + 1):
        if text[i] == pattern[0]:
            j = i
            while (text[j] == pattern[j-i]):
                j += 1
                if (j - i == len(pattern)):
                    return True
    return False


def naivelyMakeSuffixArray(source):
    """
    A naive, slow suffix-array construction algorithm.
    """

    # Construct a list of suffixes of the source string.
    suffixes = []
    for offset in range(len(source) + 1):
        suffixes.append(source[offset:])

    # Sort the suffixes
    suffixes.sort()

    # Calculate the start offset of each suffix, storing them in
    # sorted order into the suffix array.
    suffixArray = []
    for suffix in suffixes:
        offset = len(source) - len(suffix)
        suffixArray.append(offset)

    return suffixArray

def test():
    print(naiveFind('hola', 'holaComoTeVa'))
    print(naiveFind('hla', 'holaComoTeVa'))
    print(naiveFind('hola', 'ComoholaTeVa'))
    print(naivelyMakeSuffixArray('banana'))
    print(naivelyMakeSuffixArray('yabbadabbado'))

if __name__ == '__main__':
    test()