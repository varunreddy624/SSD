# !/bin/bash
mkdir temp_activity
cd temp_activity
touch temp{1..50}.txt
ls temp{1..25}.txt | sed 'p;s/\.txt/\.md/' | xargs -n2 mv
ls temp{1..50}.* | sed 'p;s/\./\\_modified./' | xargs -n2 mv
zip txt_compressed.zip *.txt
