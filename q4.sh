# !/bin/bash
integerToRoman () {
    ans=""
    num=$1
    while [ $num -gt 0 ]
    do
        if [ $num -eq 4 -o $num -eq 9 ]
        then
            ans="${ans}I"
            num=$((num+1))
        fi
        if [ $num -le 3 ]
        then
            for (( i=0; i<$num; i++ ))
            do
                ans="${ans}I"
            done
            break
        elif [ $num -ge 5 -a $num -le 8 ]
        then
            ans="${ans}V"
            num=$((num%5))
        elif [ $num -ge 10 -a $num -le 39 ]
        then
            c=$((num/10))
            for (( i=0; i<$c; i++ ))
            do
                ans="${ans}X"
            done
            num=$((num%10))
        elif [ $num -ge 40 -a $num -le 49 ]
        then
            ans="${ans}XL"
            num=$((num%40))
        elif [ $num -ge 50 -a $num -le 89 ]
        then
            ans="${ans}L"
            num=$((num%50))
        elif [ $num -ge 90 -a $num -le 99 ]
        then
            ans="${ans}XC"
            num=$((num%90))
        elif [ $num -ge 100 -a $num -le 399 ]
        then
            c=$((num/100))
            for (( i=0; i<$c; i++ ))
            do
                ans="${ans}C"
            done
            num=$((num%100))
        elif [ $num -ge 400 -a $num -le 499 ]
        then
            ans="${ans}CD"
            num=$((num%400))
        elif [ $num -ge 500 -a $num -le 899 ]
        then
            ans="${ans}D"
            num=$((num%500))
        elif [ $num -ge 900 -a $num -le 999 ]
        then
            ans="${ans}CM"
            num=$((num%900))
        else
            c=$((num/1000))
            for (( i=0; i<$c; i++ ))
            do
                ans="${ans}M"
            done
            num=$((num%1000))
        fi
    done
    echo $ans
}
romanToInteger () {
	res1=0
    	a=$1
        n=${#a}
        for (( i=0; i<$n; i++ )); do
            b=${a:$i:1}
            c=$((i+1))
            if [ "$b" = "I" -o "$b" = "X" -o "$b" = "C" ] && [ $c -lt $n ]
            then
                d=${a:$c:1}
                if [ "$b" = "I" ]
                then 
                    if [ "$d" = "V" -o "$d" = "X" ]
                    then
                        res1=$((res1-1))
                    else
                        res1=$((res1+1))
                    fi
                elif [ "$b" = "X" ]
                then 
                    if [ "$d" = "L" -o "$d" = "C" ]
                    then
                        res1=$((res1-10))
                    else
                        res1=$((res1+10))
                    fi
                else
                    if [ "$d" = "D" -o "$d" = "M" ]
                    then
                        res1=$((res1-100))
                    else
                        res1=$((res1+100))
                    fi
                fi
            else
                if [ "$b" = "I" ]
                then
                    res1=$((res1+1))
                elif [ "$b" = "V" ]
                then
                    res1=$((res1+5))
                elif [ "$b" = "X" ]
                then
                    res1=$((res1+10))
                elif [ "$b" = "L" ]
                then
                    res1=$((res1+50))
                elif [ "$b" = "C" ]
                then
                    res1=$((res1+100))
                elif [ "$b" = "D" ]
                then
                    res1=$((res1+500))
                else
                    res1=$((res1+1000))
                fi
            fi
        done
        echo $res1
}

if [ $# == 1 ]
then
    integerToRoman $1
else
    if [[ $1 =~ ^[0-9]+$ ]]
    then
        res=$(($1 + $2))
        integerToRoman $res
    else
    	res1=$(romanToInteger $1)
    	res2=$(romanToInteger $2)
    	echo $((res1+res2))
    fi
fi

