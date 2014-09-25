#!/bin/bash

for ((i=2;i<5;i++));do
        {
				sleep 3
				nohup python update.py  >log/update$i  &
                #sleep 3;echo 1>>aa && echo "done!"
        } &
done
wait
