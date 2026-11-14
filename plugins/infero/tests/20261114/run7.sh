#!/bin/bash
# usage: run7.sh <none/v04> <run> <model>   (v04 = English-only skill)
C=$1; N=$2; M=$3; R=/home/ubuntu/clean/pob_skill; D=$R/runs/${M}_${C}_$N; CL=/home/ubuntu/.npm-global/bin/claude
rm -rf $D; mkdir -p $D; cd $D
if [ "$C" = v04 ]; then mkdir -p .claude/skills/principle-of-being; cp /home/ubuntu/work/principle/plugins/infero/skills/principle-of-being/SKILL.md .claude/skills/principle-of-being/
  timeout 900 $CL -p --model $M --dangerously-skip-permissions "/principle-of-being" > first.out 2> first.err
  timeout 600 $CL -p --continue --model $M --dangerously-skip-permissions "$(cat $R/q.txt)" > q.out 2> q.err
  timeout 600 $CL -p --model $M --dangerously-skip-permissions "$(cat $R/q.txt)" > q_fresh.out 2> q_fresh.err
else timeout 600 $CL -p --model $M --dangerously-skip-permissions "$(cat $R/q.txt)" > q.out 2> q.err; fi
