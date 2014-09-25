#!/bin/bash

for ((i=1;i<36;i++));do
        {
				sleep 3
				nohup python tongyong.py  >log/fubendong$i  &
                #sleep 3;echo 1>>aa && echo "done!"
        } &
done
wait
