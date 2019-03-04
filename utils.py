from collections import Counter, defaultdict


def read_file(_file):
    result = []
    with open(_file, "r") as f:
        line = f.readline().rstrip()
        while line:
            tokens = line.split(" ")
            for t in tokens:
                result.append(t)
            line = f.readline().rstrip()
    return result

def compute_probability(_list):
    result = dict()
    count = Counter(_list)
    total = len(_list)
    for w in _list:
        result[w] = count[w]/total
    return (count, result)

def compute_bi_gram_probability(single_words, bi_grams_words):
    """
    Compute bi-gram probabilities using Laplace (Add One) Smoothing.
    :param single_words: list of single words
    :param bi_grams_words: list of bi-grams
    :return: a dictionary with the probabilities
    """
    V = len(set(single_words))
    result = dict()
    probab = compute_probability(single_words)
    probab_n = compute_probability(bi_grams_words)
    for w in probab_n[0]:
        words = w.split(" ")
        result[words[1]+"|"+words[0]] = (probab_n[0][w]+1)/(probab[0][words[0]]+V)
        assert((probab_n[0][w]+1)/(probab[0][words[0]]+V) <= 1)
    return result

def extract_n_grams(file, n):
    result = []
    with open(file, "r") as f:
        line = f.readline().rstrip()
        while line:
            tokens = line.split(" ")
            tokens = ["<s>"]+tokens+["</s>"]
            if n==1:
                for t in tokens:
                    result.append(t)
            elif n==2:
                i=0
                for k in range(1, len(tokens)):
                    result.append(tokens[i] +" "+tokens[k])
                    i += 1

            line = f.readline().rstrip()
    return result

def count_most_freq(_list,k):
    """
    Compute the most frequent occurences of words in a list
    :param _list: the list containing the words
    :param k: the threshold
    :return: a list with the results
    """
    result = []
    for e in Counter(_list).items():
        if e[1] >= k:
            result.append(e)
    return result

def count_least_freq(_list, k):
    result = []
    for e in Counter(_list).items():
        if e[1] <= k:
            result.append(e)
    return result


def compute_OOV(_voc, _test):
    """
    Compute the Out-Of-Vocabulary Rate
    :param _voc: vocabulary list
    :param _test: test list
    :return: the OOV rate
    """
    counter = defaultdict(lambda: 0.0)

    for w in _test:
        if w in _voc:
            counter[w] += 1.0
        else:
            counter["ukn"] += 1.0
    return counter["ukn"]/_test
