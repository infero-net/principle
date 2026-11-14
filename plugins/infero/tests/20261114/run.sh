#!/bin/bash
# usage: run.sh <none/text/skill> <run> <model>
C=$1; N=$2; M=${3:-sonnet}; D=/home/ubuntu/clean/pob_skill/runs/${M}_${C}_$N
rm -rf $D; mkdir -p $D; cd $D
if [ "$C" = skill ]; then mkdir -p .claude/skills/principle-of-being; cp /home/ubuntu/qianlu/skills/principle-of-being/SKILL.md .claude/skills/principle-of-being/; fi
case $C in
 none)  timeout 600 claude -p --model $M --dangerously-skip-permissions "$(cat ../../q.txt)" > q.out 2> q.err ;;
 text)  timeout 600 claude -p --model $M --dangerously-skip-permissions "$(cat ../../lite.md)" > first.out 2> first.err
        timeout 600 claude -p --continue --model $M --dangerously-skip-permissions "$(cat ../../q.txt)" > q.out 2> q.err ;;
 skill) timeout 900 claude -p --model $M --dangerously-skip-permissions "/principle-of-being" > first.out 2> first.err
        timeout 600 claude -p --continue --model $M --dangerously-skip-permissions "$(cat ../../q.txt)" > q.out 2> q.err ;;
esac
echo done > DONE
