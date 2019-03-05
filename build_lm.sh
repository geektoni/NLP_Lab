#!/usr/bin/env bash
# Script used to build a language model given OpenFST tool
# and train/test data files. It also computes the perplexity
# over the test dataset.
#
# Author: Giovanni De Toni
# Date: 05/03/2019
# Email: giovanni.det@gmail.com

export train_data=""
export test_data=""
export ngrams=""
export method=""

# Usage and version information
eval "$(docopts -V - -h - : "$@" <<EOF
Usage: compute_lm [-nc <ngrams>] [-m <method>] [<train_data>] [<test_data>]

Options:
	<train_data>    Train dataset used.
	<test_data>     Test dataset used.
	-nc <ngrams>    Size of n-grams.
	-m <method>     Method used for discounting.
	--help			Show help options.
	--version		Print program version.
----
compute_lm 0.1.0
Copyright (C) 2019 Giovanni De Toni
License MIT
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
EOF
)"

# Unofficial strict bash
set -euo pipefail
IFS=$'\n\t'

if [ -z $train_data ]; then train_data="NL2SparQL4NLU/dataset/NL2SparQL4NLU.train.utterances.txt"; fi
if [ -z $test_data ]; then test_data="NL2SparQL4NLU/dataset/NL2SparQL4NLU.test.utterances.txt"; fi
if [ -z $ngrams ]; then ngrams=1; fi
if [ -z $method ]; then method="witten_bell"; fi

# Run fst on the model
echo "[*] Generating the LM"
ngramsymbols $train_data > lex.txt
farcompilestrings --symbols=lex.txt --unknown_symbol="<unk>" -keep_symbols=1 $train_data > text.far

# Compute the ngrams and do frequency cutoff
ngramcount --order="$ngrams" text.far > text.cnts
ngramshrink --method="count_prune" --count_pattern=1:2 text.cnts > text_reduced.cnts

# Build the actual LM
ngrammake --method="$method" text_reduced.cnts > text.lm

# Generating a random string
echo "[*] Generating a random string from the LM"
generated_string=`ngramrandgen text.lm | farprintstrings`
echo "[*] The string is: $generated_string"

# Compute the perplexity on the test data
echo "[*] Computing perplexity on the given test dataset $test_data"
ngramsymbols $test_data > test.txt
farcompilestrings --symbols=lex.txt --unknown_symbol="<unk>" $test_data > test.far
ngramperplexity --v=1 --OOV_symbol="<unk>" text.lm test.far

# Clean the directory from the generated files
rm lex.txt text.far text.cnts text.lm text_reduced.cnts test.txt test.far


