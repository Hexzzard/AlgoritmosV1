import re

str = "5x1 + 3.2x2 + 20.67x4 <=1"
str = """maximize 2x1 -3x2 +3x3 = Z
subject to
1.2x1 +23x2 +20x3>= 15
22x1 -15x2 <= 100
12x1 <= 21
11x1 +23x2 +5x3 <= 60"""


lines = str.strip().split('\n')
print(lines)
pattern = r'([-+]?\d*\.?\d+)\s*([a-zA-Z]\d+)|=\s*([-+]?\d*\.?\d+)|([<>])'
vars = len(re.findall(pattern, lines[0]))
print(vars)