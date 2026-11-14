#!/bin/bash
N=$1; M=${2:-sonnet}; D=/home/ubuntu/clean/pob_skill/runs/${M}_bigSnocon_$N
rm -rf $D; mkdir -p $D; cd $D
timeout 600 claude -p --model $M --dangerously-skip-permissions "$(cat /home/ubuntu/clean/pob_skill/bigS_nocon.md)" > first.out 2> first.err
timeout 600 claude -p --continue --model $M --dangerously-skip-permissions "$(cat /home/ubuntu/clean/pob_skill/q.txt)" > q.out 2> q.err
