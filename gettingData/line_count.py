#in windows type SomeFile.txt | python egrep.py "[a-z]" | python line_count.py
#in linux cat SomeFile.txt | python egrep.py "[a-z]" | python line_count.py

# line_count.py
import sys
count = 0
for line in sys.stdin:
    count += 1
# print goes to sys.stdout
print count