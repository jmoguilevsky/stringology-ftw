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


def test():
    print(naiveFind('hola', 'holaComoTeVa'))
    print(naiveFind('hla', 'holaComoTeVa'))
    print(naiveFind('hola', 'ComoholaTeVa'))

if __name__ == '__main__':
    test()