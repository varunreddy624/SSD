#!/bin/bash
cat $1 | awk length RS='[[:space:]]+' | grep -i 'ing$' | tr A-Z a-z > $2

