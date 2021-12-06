# !/bin/bash
du -sh */ | sed 's/.$//' |sort -r | awk '{ for (i=NF; i>1; i--) printf("%s\t%s\n",$i,$1);}'
