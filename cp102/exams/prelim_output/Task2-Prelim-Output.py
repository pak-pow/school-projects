"""REG EX"""

import re

"""Opening the File"""
with open("supercomputer.txt", "r") as file:
    text = file.read()

"""Defining each patterns"""
patterns = {
    "Years": r"\b(1[89]\d{2}|20[0-2]\d)\b",  # Matches years from 1800-2029
    "Hyphenated Words": r"\b\w+-\w+\b",  # Matches words like "high-speed"
    "Acronyms": r"\b[A-Z]{2,}\b",  # Matches all-caps words (CPU, IBM, etc.)
    "Numbers with Commas": r"\b\d{1,3}(?:,\d{3})+\b",  # Matches 1,000+ format
    "All Numbers": r"\b\d+(?:,\d+)?(?:\.\d+)?\b",  # Extracts all numbers
    "Processor Mentions": r"\b(?:Intel|AMD|IBM|NEC)\s[A-Za-z0-9-]+\b"  # Detects processors
}

"""Storing The result"""
results = {}

for category, pattern in patterns.items():
    matches = re.findall(pattern, text)
    results[category] = matches

for category, matches in results.items():
    print(f"{category} ({len(matches)} found):")
    print(matches)
    print("-" * 50)

if results["All Numbers"]:
    all_numbers = []
    for num in results["All Numbers"]:
        all_numbers.append(float(num.replace(",", "")))  # Remove commas & convert

    print(f"Total Count of Numbers: {len(all_numbers)}")
    print(f"Total Sum of Numbers: {sum(all_numbers)}")
    print(f"Max Number: {max(all_numbers)}")
    print(f"Min Number: {min(all_numbers)}")
    print(f"Average Number: {sum(all_numbers) / len(all_numbers):.2f}")