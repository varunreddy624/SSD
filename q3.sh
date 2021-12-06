#!/bin/bash
sortString(){
	echo $(echo $1 | grep -o . | sort | tr -d "\n" )
}
compgen -c > possibleCommands.txt
sortedIp=$(sortString $1)
awk 'length($1) == '${#sortedIp}' {print $1}' possibleCommands.txt | sort -u > eligibleSortedCommands.txt
flag=0
cat eligibleSortedCommands.txt | while read eachCombination; 
	 do 
	 eachCombinationSorted=$(sortString $eachCombination)
	 if [[ $eachCombinationSorted == $sortedIp ]]
	 then
		 if [[ $flag == 0 ]]
		 then
			 echo -ne YES'\t'$eachCombination
			 flag=1
		 else
		 	echo -ne '\t'$eachCombination
		 fi
	 fi 
 done > possibleCommands.txt
 [ -s possibleCommands.txt ] && cat possibleCommands.txt || echo -n "NO"
