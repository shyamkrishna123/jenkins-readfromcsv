#!/bin/bash
file=$1
success_col=$(head -1 $file | tr ',' '\n' | nl |grep -w "success" | tr -d " " | awk -F " " '{print $1}')
#echo"$(head -1 $file | tr ',' '\n' | nl |grep -w "success" | tr -d " " | awk -F " " '{print $1}')"
while IFS="," read -r rec1; do
  # do something... Don't forget to skip the header line!
  arr+=($rec1)
done < <(cut -d "," -f${success_col} $file | tail -n +2)
if [[ $arr == 'false' ]] 
then
  exit 1
else
 exit 0
fi
