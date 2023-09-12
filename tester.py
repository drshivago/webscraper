import re

log_file = open("log.txt", 'r')
counter = 0
for j in log_file:

    if re.search("-740.jpg*", j):
        print(j)
        counter += 1
print(counter)
