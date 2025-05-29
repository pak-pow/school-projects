# VINCENT S.
"""ACTIVITY #2"""

import re

# Open and read file
with open("regex_sum_42.txt", "r") as file:
    lines = file.readlines()

"""Display lines that start with Python"""

for line in lines:
    if re.match("^Python", line):
        print(line.strip())

print("")

"""Extract numbers and compute sum"""

num_list = [int(num) for line in lines for num in re.findall(r"\d+", line)]
print(f"The sum of all numbers is {sum(num_list)}")
print(f"The highest number is {max(num_list)}")

"""Count all vowels"""

vowel_count = sum(len(re.findall(r"[aeiouAEIOU]", line)) for line in lines)
print(f"The total vowel count is {vowel_count}")

"""Count occurrences of Python"""

python_count = sum(len(re.findall(r"\bPython\b", line)) for line in lines)
print(f"Python word count is {python_count}")
