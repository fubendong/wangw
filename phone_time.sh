#!/bin/bash

for ((i=1;i<5;i++));do
        {
				sleep 3
				nohup python phone_get.py  >log/phone$i  &
                #sleep 3;echo 1>>aa && echo "done!"
        } &
done
wait
