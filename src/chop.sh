scp debian@beaglebone:~/quickbot-v1-wheel-encoder/src/10s-raw.txt ./.
grep '^0' 10s-raw.txt | cut -d ' ' -f2,3 > 10s-right-actual.txt
grep '^0' 10s-raw.txt | cut -d ' ' -f2,4 > 10s-right-filtered.txt
grep '^1' 10s-raw.txt | cut -d ' ' -f2,3 > 10s-left-actual.txt
grep '^1' 10s-raw.txt | cut -d ' ' -f2,4 > 10s-left-filtered.txt
