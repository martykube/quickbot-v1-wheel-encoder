scp debian@beaglebone:~/quickbot-v1-wheel-encoder/src/schmitt-1.txt ./.
grep '^0' schmitt-1.txt | cut -d ' ' -f2,3 > schmitt-right-actual.txt
grep '^0' schmitt-1.txt | cut -d ' ' -f2,4 > schmitt-right-filtered.txt
grep '^1' schmitt-1.txt | cut -d ' ' -f2,3 > schmitt-left-actual.txt
grep '^1' schmitt-1.txt | cut -d ' ' -f2,4 > schmitt-left-filtered.txt
