def lessOrEqual2(a, b):
    return a[0] < b[0] or (a[0] == b[0] and a[1] <= b[1])

def lessOrEqual3(a, b):
  return a[0] < b[0] or (a[0] == b[0] and lessOrEqual2(a[1:], b[1:]))

# sort a[0..n-1] to b[0..n-1] with keys in 0..K from r
def radixPass(a, b, s, offset, K):
    occurrences = [0] * (K + 1)
    n = len(a)
    for i in range(offset, n + offset):
        occurrences[s[a[i]]] += 1
    accum = 0
    for i in range(K + 1):
        t = occurrences[i]
        occurrences[i] = accum
        accum += t
    # this magic sorts the array
    for i in range(offset, n + offset):
        b[occurrences[s[a[i]]] = i
        occurrences[s[i]] += 1

# find the suffix array SA of s[0..n-1]
# require s[n]=s[n+1]=s[n+2]=0, n>=2
def suffixArray(s, SA, K):
    n = len(s)
    n0=(n+2)/3
    n1=(n+1)/3
    n2=n/3
    n02=n0+n2
    s12 = [0] * (n02 +3)
    SA12 = [0] * (n02 +3)
    s0 = [0] * n0
    SA0 = [0] * n0

    # generate positions of mod 1 and mod  2 suffixes
    # the "+(n0-n1)" adds a dummy mod 1 suffix if n%3 == 1
    # s12 = s without the characters at positions i%3 == 0
    j = 0
    for i in range(n + (n0 - n1)):
        if i%3 != 0:
            s12[j] = i
            j += 1

    # lsb radix sort the mod 1 and mod 2 triples
    radixPass(s12, SA12, n02, K)
    radixPass(SA12, s12, n02, K)
    radixPass(s12, SA12, n02, K)

    name = 0
    c0 = -1
    c1 = -1
    c2 = -1
    for i in range(n-2):
