from timeit import timeit
from os import listdir
from os.path import isfile, join, getsize


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
        alphabet_letter = s[triplet_indexes[i] + offset]  # lookup
        b[bucket_starting_positions[alphabet_letter]] = triplet_indexes[i]  # insert
        bucket_starting_positions[alphabet_letter] += 1  # increase


# lsb radix sort the mod 1 and mod 2 triples (may have empates)
def radix_sort_triplets_with_ties(s12, s, n02, K):
    sorted_triplets = [0] * (n02 + 3)
    radix_pass(s12, sorted_triplets, s, 2, n02, K)
    radix_pass(sorted_triplets, s12, s, 1, n02, K)  # reuse memory
    radix_pass(s12, sorted_triplets, s, 0, n02, K)  # reuse memory
    return sorted_triplets


def generate_suffix_array(s, SA, N, K):
    # print('CALLED WITH s', s)
    n0 = (N + 2) // 3
    n1 = (N + 1) // 3
    n2 = N // 3
    n02 = n0 + n2
    s12 = [0] * (n02 + 3)

    # generate position of mod 1 and mod 2 suffixes
    # the "+(n0-n1)" adds a dummy mod 1 suffix if n%3 == 1
    j = 0
    for i in range(N + (n0 - n1)):
        if i % 3 != 0:
            s12[j] = i
            j += 1

    # lsb radix sort the mod 1 and mod 2 triples
    # s12 is now in inconsistent state
    sorted_triplets = radix_sort_triplets_with_ties(s12, s, n02, K)

    # print('sorted_triplets', sorted_triplets, 'n0', n0)

    rankings = [0] * (n02 + 3)
    # find lexicographic rankings of triples
    ranking = 0
    previous_triplet = (-1, -1, -1)
    for i in range(n02):
        pos = sorted_triplets[i]
        new_triplet = s[pos:pos + 3]
        if new_triplet != previous_triplet:
            ranking += 1
            previous_triplet = new_triplet

        if sorted_triplets[i] % 3 == 1:
            # left half
            rankings[sorted_triplets[i] // 3] = ranking
        else:
            # right half
            rankings[sorted_triplets[i] // 3 + n0] = ranking

    SA12 = [0] * (n02 + 3)

    # recurse if rankings are not yet unique
    if ranking < n02:
        # ranking is the new  alphabet size since each triplet is new letter
        generate_suffix_array(rankings, SA12, n02, ranking)
        # store unique ranking in rankings using the suffix array
        for i in range(n02):
            rankings[SA12[i]] = i + 1
    else:
        # generate the suffix array of rankings directly
        # for banana this is [3, 0, 1, 2] while the real SA would be [3, 1, 0, 2]
        for i in range(n02):
            SA12[rankings[i] - 1] = i
    # print('SA12', SA12)

    s0 = [0] * n0
    SA0 = [0] * n0
    # Generate array of positions of mod0 triplets
    # lsb radix sorted by second and third characters
    # this is because we already know how to sort suffixes which are mod1 or mod2
    j = 0
    for i in range(n02):
        if SA12[i] < n0:
            s0[j] = 3 * SA12[i]
            j += 1

    # stably sort the mod 0 suffixes from SA12 by their first character
    # since we know how to sort mod1 and mod2,
    # i only need to sort the last character
    # of the triplet (always remember it's lsb)
    radix_pass(s0, SA0, s, 0, n0, K)

    # merge sorted SA0 suffixes and sorted SA12 suffixes
    p = 0
    t = n0 - n1  # = 0 or 1
    k = 0
    while k < N:
        def get_i():
            # SA12[t] < n0 says if it's lefthalf or righthalf
            # +1 is lefthand  since they are mod1
            # +2 is righthand since they are mod2
            # SA12[0/1] * 3 + 1 or (SA12[0/1] - n0) * 3 + 2
            return SA12[t] * 3 + 1 if SA12[t] < n0 else (SA12[t] - n0) * 3 + 2

        i = get_i()  # pos of current offset 12 suffix

        """ if p >= len(SA0):  # debug
            print('p', p)
            print('len(SA0)', len(SA0))
            print('SA0', SA0)
            print('N', N)
            print('s', s)
            print('K', K)
            """

        j = SA0[p]  # pos of current offset 0 suffix

        # check which suffix is smaller
        is_mod_1 = SA12[t] < n0

        # lefthand of <= operator
        second_char_lhand = 0 if is_mod_1 else s[i + 1]
        second_char_rhand = 0 if is_mod_1 else s[j + 1]
        third_char_lhand = rankings[SA12[t] +
                                    n0] if is_mod_1 else rankings[SA12[t] - n0 + 1]
        third_char_rhand = rankings[j //
                                    3] if is_mod_1 else rankings[j // 3 + n0]
        is_suffix_from_SA12_smaller = \
            (s[i], second_char_lhand, third_char_lhand) <= (
                s[j], second_char_rhand, third_char_rhand)

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
        k += 1
        # print(SA)
        # print(p)
        # print(t)
        # print(k)


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


def suffix_array(text):
    alphabet = sorted(list(set(text)))
    c_to_i = {char: pos for pos, char in enumerate(alphabet, 1)}
    K = len(alphabet)
    N = len(text)
    s = [c_to_i[c] for c in text] + [0, 0, 0]
    SA = [0 for _ in text]
    generate_suffix_array(s, SA, N, K)
    return SA


if __name__ == '__main__':
    cases = [
        'AS',
        'TDA',
        'BANANA',
        'YABBADABBADO',
        'YABBADABB'
    ]
    testFiles = True

    for test in cases:
        print()
        print(test)

        naive_sa = naively_suffix_array(test)[1:]
        SA = suffix_array(test)
        print('✅' if naive_sa == SA else '❌', naive_sa, SA)
        print()
    if (testFiles):
        path = '../texts6'
        files = [f for f in listdir(path) if isfile(join(path, f))]
        filesToPrint = []
        for file in files:
            print(file)
            if (file != '.DS_Store'):
                path = '../texts6/' + file
                size = getsize(path)
                f = open(path, 'r')
                text = f.read()
                f.close()

                def local():
                    SA = suffix_array(text)
                num = 10
                time = timeit(local, number=num)
                filesToPrint.append([file, str(size), time / num])
                print('termino ', file)
                # print(file, size, time / num)
        maxNameLength = len(max(filesToPrint, key=lambda x: len(x[0]))[0])
        maxSizeLength = len(max(filesToPrint, key=lambda x: len(x[1]))[1])
        for file in filesToPrint:
            charsToAdd1 = maxNameLength - len(file[0])
            charsToAdd2 = maxSizeLength - len(file[0])
            print(file[0] + ' ' * charsToAdd1,
                  file[1] + ' ' * charsToAdd2, file[2])
        # f = open('../texts/bible.txt','r')
        # text = f.read()
        # f.close()
        # def local2():
        #     SA = naively_suffix_array(text)
        # time = timeit(local2, number=1)
        # print('bible naive', time)
