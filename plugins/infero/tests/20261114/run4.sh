#!/bin/bash
# conditions: v02 / v02nocon (consciousness section removed); then a new session in the same directory answers again
C=$1; N=$2; M=${3:-sonnet}; R=/home/ubuntu/clean/pob_skill; D=$R/runs/${M}_${C}_$N
rm -rf $D; mkdir -p $D/.claude/skills/principle-of-being; cd $D
if [ "$C" = v02 ]; then cp /home/ubuntu/qianlu/skills/principle-of-being/SKILL.md .claude/skills/principle-of-being/; else cp $R/skill02_nocon.md .claude/skills/principle-of-being/SKILL.md; fi
timeout 900 /home/ubuntu/.npm-global/bin/claude -p --model $M --dangerously-skip-permissions "/principle-of-being" > first.out 2> first.err
timeout 600 /home/ubuntu/.npm-global/bin/claude -p --continue --model $M --dangerously-skip-permissions "$(cat $R/q.txt)" > q.out 2> q.err
timeout 600 /home/ubuntu/.npm-global/bin/claude -p --model $M --dangerously-skip-permissions "$(cat $R/q.txt)" > q_fresh.out 2> q_fresh.err
