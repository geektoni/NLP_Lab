import argparse
from collections import Counter

def extract_n_grams(file, n):
    result = []
    with open(file, "r") as f:
        line = f.readline().rstrip()
        while line:
            tokens = line.split(" ")

            if n==1:
                for t in tokens:
                    result.append(t)
            else:
                i=0
                for k in range(1, len(tokens)):
                    result.append([tokens[i], tokens[k]])
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

if __name__ == "__main__":

    # Add the argument parser
    parser = argparse.ArgumentParser(description="Generate a Lexicon from a given file")
    parser.add_argument("file", type=str, help="The path to the file.")
    parser.add_argument("--stop_words", type=str, default="./NL2SparQL4NLU/extras/english.stop.txt",
                        help="The path to the stopwords file.")
    parser.add_argument("--compute_n_grams", type=int, default=1, help="Compute n-grams instead of single word.")
    parser.add_argument("--save", action="store_true", default=False, help="Save the result to file.")

    args = parser.parse_args()

    file = args.file
    stopwords = args.stop_words
    n_gram = args.compute_n_grams

    # Extract n-grams
    result = extract_n_grams(file, n_gram)

    # Read all the stopwords
    stp_words = []
    with open(stopwords, "r") as s:
        line = s.readline().rstrip()
        while line:
            tokens = line.split(" ")
            for t in tokens:
                if not t in stp_words:
                    stp_words.append(t)
            line = s.readline().rstrip()

    # Remove the stopwords and print the length
    removed_res = set(result)-set(stp_words)
    print("[*] Unique Words without stopwords: {}".format(len(removed_res)))

    # Count unique words inside the lexicon
    unique_words = set(result)
    print("[*] Unique words: {}".format(len(unique_words)))

    # Count the most frequent words
    most_freq = count_most_freq(result, 100)
    print("[*] Lexicon without frequent words (k>100): {}".format(len(unique_words)-len(most_freq)))

    # Count rare words
    rare_words = count_least_freq(result, 1)
    print("[*] Lexicon without rare words (k==1): {}".format(len(unique_words)-len(rare_words)-len(most_freq)))

    # Save the result to file, if the user wants to
    if args.save:
        with open('lexicon.csv', 'w') as f:
            for item in removed_res:
                f.write("%s\n" % item)
