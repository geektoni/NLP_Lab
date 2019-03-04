import argparse
from utils import *

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

    # Compute n-gram probabilities
    print(compute_bi_gram_probability(result, extract_n_grams(file, 2)))

    # Save the result to file, if the user wants to
    if args.save:
        with open('lexicon.csv', 'w') as f:
            for item in result:
                f.write("%s\n" % item)
        with open('vocabulary.csv', 'w') as f:
            for item in set(result):
                f.write("%s\n" % item)
