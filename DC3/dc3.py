def radix_pass(triplet_indexes, b, s, offset, N, K):
    bucket_sizes = [0] * (K + 1)
    bucket_starting_positions = [0] * (K + 1)

    # count occurrences
    # meaning bucketsize per alphabet letter
    # if banana and, a = [1,2,4,5] + offset2
    # then c = [2, 1, 0, 1]
    # since the strings are
    # $: [NA$, A$$]
    # A: [ANA]
    # B: []
    # N: [NAN]
    for i in range(N):
        alphabet_letter = s[triplet_indexes[i] + offset]
        bucket_sizes[alphabet_letter] += 1

    # Set bucket_starting_positions
    #[2,1,0,1] generates
    #[0,2,3,3] this are the positions where each bucket starts
    accum = 0
    for i, size in enumerate(bucket_sizes):
        bucket_starting_positions[i] = accum
        accum += size

    # inserts each string in the starting position for the bucket
    # once it inserts a string, the starting position is increased
    for i in range(N):
        alphabet_letter = s[triplet_indexes[i] + offset] #lookup
        b[bucket_starting_positions[alphabet_letter]] = triplet_indexes[i] #insert
        bucket_starting_positions[alphabet_letter] += 1 #increase


def suffix_array(s, SA, N, K):
    print('CALLED WITH s', s)
    n0 = (N + 2) // 3
    n1 = (N + 1) // 3
    n2 = N // 3
    n02 = n0 + n2
    s12 = [0] * (n02 + 3)
    SA12 = [0] * (n02 + 3)
    s0 = [0] * n0
    SA0 = [0] * n0

    # generate position of mod 1 and mod 2 suffixes
    j = 0
    for i in range(N + (n0 - n1)):
        if i % 3 != 0:
            s12[j] = i
            j += 1

    # lsb radix sort the mod 1 and mod 2 triples
    radix_pass(s12, SA12, s, 2, n02, K)
    radix_pass(SA12, s12, s, 1, n02, K)
    radix_pass(s12, SA12, s, 0, n02, K)

    # find lexicographic names of triples
    name = 0
    c0 = -1
    c1 = -1
    c2 = -1
    for i in range(n02):
        if s[SA12[i] + 0] != c0 or s[SA12[i] + 1] != c1 or s[SA12[i] + 2] != c2:
            name += 1
            c0 = s[SA12[i] + 0]
            c1 = s[SA12[i] + 1]
            c2 = s[SA12[i] + 2]
        if SA12[i] % 3 == 1:
            # ;eft half
            s12[SA12[i] // 3] = name
        else:
            # right half
            s12[SA12[i] // 3 + n0] = name

    # recurse if names are not yet unique
    if name < n02:
        suffix_array(s12, SA12, n02, name)
        # store unique names in s12 using the suffix array
        for i in range(n02):
            s12[SA12[i]] = i + 1
    else:
        # generate the suffix array of s12 directly
        for i in range(n02):
            SA12[s12[i] - 1] = i

    # stably sort the mod 0 suffixes from SA12 by their first character
    j = 0
    for i in range(n02):
        if SA12[i] < n0:
            s0[j] = 3 * SA12[i]
            j += 1
        radix_pass(s0, SA0, s, 0, n0, K)

    # merge sorted SA0 suffixes and sorted SA12 suffixes
    p = 0
    t = n0 - n1
    for k in range(N):
        def get_i():
            return SA12[t] * 3 + 1 if SA12[t] < n0 else (SA12[t] - n0) * 3 + 2

        i = get_i()  # pos of current offset 12 suffix

        if p >= len(SA0):  # debug
            print('p', p)
            print('len(SA0)', len(SA0))
            print('SA0', SA0)
            print('N', N)
            print('s', s)
            print('K', K)
        j = SA0[p]  # pos of current offset 0 suffix

        # check which suffix is smaller
        cond = SA12[t] < n0
        second_a = 0 if cond else s[i + 1]
        second_b = 0 if cond else s[j + 1]
        third_a = s12[SA12[t] + n0] if cond else s12[SA12[t] - n0 + 1]
        third_b = s12[j // 3] if cond else s12[j // 3 + n0]
        is_suffix_from_SA12_smaller = \
            (s[i], second_a, third_a) <= (s[j], second_b, third_b)

        # merge step
        if is_suffix_from_SA12_smaller:
            SA[k] = i
            t += 1
            if t == n02:  # done -- only SA0 suffixes left
                k += 1
                while p < n0:
                    SA[k] = SA0[p]
                    p += 1
                    k += 1
        else:
            SA[k] = j
            p += 1
            if p == n0:  # done -- only SA12 suffixes left
                k += 1
                while t < n02:
                    SA[k] = get_i()
                    t += 1
                    k += 1


def naively_suffix_array(source):
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


if __name__ == '__main__':
    cases = [
        'TDA',
        'BANANA',
        'YABBADABBADO'
    ]

    for test in cases:
        print()
        print(test)
        alphabet = sorted(list(set(test)))
        c_to_i = {char: pos for pos, char in enumerate(alphabet, 1)}
        K = len(alphabet)
        N = len(test)
        s = [c_to_i[c] for c in test] + [0, 0, 0]
        SA = [0 for _ in test]

        naive_sa = naively_suffix_array(test)
        suffix_array(s, SA, N, K)
        print('??' if s == SA else '?', s, SA)
        print()
