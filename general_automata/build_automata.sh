#!/usr/bin/env bash

export alphabeth=""
export automata=""
export output_alphabeth=""

# Usage and version information
eval "$(docopts -V - -h - : "$@" <<EOF
Usage: build_automata.sh <alphabeth> <automata> <output_alphabeth>

Options:
	<alphabeth>     Alphabeth used.
	<automata>      Automata which has to be used.
----
build_automata 0.1.0
Copyright (C) 2019 Giovanni De Toni
License MIT
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
EOF
)"

# Unofficial strict bash
set -euo pipefail
IFS=$'\n\t'

fstcompile --isymbols=$alphabeth -osymbols=$output_alphabeth $automata | fstrmepsilon | fstdeterminize | fstminimize > automata.fsa

# Draw
fstdraw -isymbols=$alphabeth -osymbols=$output_alphabeth -portrait automata.fsa | dot -Tjpg -Gdpi=500 >automata.jpg
