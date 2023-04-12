import re
#r'([-+]?\d*)[ ]*([a-zA-Z]\d+)'
#r'(([-+]?\d*)[ ]*([a-zA-Z]\d+)[ ]*([=][-+]?\d+))([=]([-+]?\d+))'
#patron = r'([-+]?\d*)[ ]*([a-zA-Z]\d+)(?:[ ]*([-+])\s*([0-9]+)[ ]*)?(?:[ ]*([=])[ ]*([-+]?\d+))?'
def extract_coeffs(x):
    pattern = r'([-+]?\d*)[ ]*([a-zA-Z]\d+)'
    coeffs = []

    for match in re.findall(pattern, x):
        print(match)
        coeff_str, var = match 
        print(coeff_str)
        coeff = int(coeff_str) if coeff_str not in ['','+','-'] else 1 if(coeff_str!='-') else -1
        coeffs.append(coeff)

    return coeffs

coeffs = extract_coeffs("2x1 + 3x2 -x3 =1")
print(coeffs)


