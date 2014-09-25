#!/bin/bash

for ((i=1;i<3;i++));do
        {
				sleep 3
				nohup python tb.py  >log/fubendong$i  &
                #sleep 3;echo 1>>aa && echo "done!"
        }
done
wait
