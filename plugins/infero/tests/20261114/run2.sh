#!/bin/bash
# conditions: bigS (the full S pasted as text) / skillS (skill with section 1 replaced by the full S, steps unchanged)
C=$1; N=$2; M=${3:-sonnet}; D=/home/ubuntu/clean/pob_skill/runs/${M}_${C}_$N
rm -rf $D; mkdir -p $D; cd $D
case $C in
 bigS)   timeout 600 claude -p --model $M --dangerously-skip-permissions "$(cat ../../bigS.md)" > first.out 2> first.err ;;
 skillS) mkdir -p .claude/skills/principle-of-being; cp ../../skillS/SKILL.md .claude/skills/principle-of-being/
         timeout 900 claude -p --model $M --dangerously-skip-permissions "/principle-of-being" > first.out 2> first.err ;;
esac
timeout 600 claude -p --continue --model $M --dangerously-skip-permissions "$(cat ../../q.txt)" > q.out 2> q.err
echo done > DONE
