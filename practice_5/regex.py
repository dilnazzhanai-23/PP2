import re

# Write a Python program that matches a string that has an 'a' followed by zero or more 'b's
s1 = input()
if re.fullmatch(r'ab*', s1):
    print("Match")
else:
    print("No match")

#Write a Python program that matches a string that has an 'a' followed by two to three 'b'
s2 = input()
if re.fullmatch(r'ab{2,3}', s2):
    print("Match")
else:
    print("No match")

# Write a Python program to find sequences of lowercase letters joined with a underscore.
s3 = input()
matches3 = re.findall(r'[a-z]+(?:_[a-z]+)+', s3)
print("Matches:", matches3)

# Write a Python program to find the sequences of one upper case letter followed by lower case letters.
s4 = input()
matches4 = re.findall(r'[A-Z][a-z]+', s4)
print("Matches:", matches4)

# Write a Python program that matches a string that has an 'a' followed by anything, ending in 'b'.
s5 = input()
if re.fullmatch(r'a.*b', s5):
    print("Match")
else:
    print("No match")

# Write a Python program to replace all occurrences of space, comma, or dot with a colon.
s6 = input()
result6 = re.sub(r'[ ,.]', ':', s6)
print("Result:", result6)

# Write a python program to convert snake case string to camel case string.
s7 = input()
def snake_to_camel(s):
    return re.sub(r'_([a-z])', lambda m: m.group(1).upper(), s)
print("CamelCase:", snake_to_camel(s7))

# Write a Python program to split a string at uppercase letters.
s8 = input()
parts8 = re.split(r'(?=[A-Z])', s8)
print("Parts:", parts8)

# Write a Python program to insert spaces between words starting with capital letters.
s9 = input()
result9 = re.sub(r'([A-Z])', r' \1', s9).strip()
print("Result:", result9)

# Write a Python program to convert a given camel case string to snake case.
s10 = input()
result10 = re.sub(r'([A-Z])', lambda m: '_' + m.group(1).lower(), s10)
if result10.startswith('_'):  
    result10 = result10[1:]
print("Snake_case:", result10)