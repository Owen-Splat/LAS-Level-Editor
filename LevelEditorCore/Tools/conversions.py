import numpy as np


def removeTrailingZeros(dec: str) -> str:
    """Removes trailing zeros in float strings"""

    if not dec.isdigit():
        try:
            test = float(dec)
        except TypeError:
            return dec

    dec_list = [c for c in dec]
    dec_list.reverse()
    dec_list_2 = dec_list.copy()

    for d in dec_list_2:
        if d == '0':
            dec_list.remove(d)
        else:
            break

    dec_str = ''
    dec_list.reverse()
    for d in dec_list:
        dec_str += d

    if dec_str.endswith('.'):
        dec_str += '0'

    return dec_str


def strToFloat(value: str) -> (str | np.float32):
    """Converts user inputed text into a float, removing garbage characters in the process

    This also parses commas as decimals in case of typo. If there are multiple, only read the top-most level decimal
    
    May eventually update to perform basic math operations"""

    if not value.isdigit():
        try:
            test = float(value)
        except TypeError:
            return value

    value = ''.join([c for c in value if c in ('.', ',', '+', '-') or c.isdecimal()])
    if ',' not in value and '.' not in value:
        return np.float32(value)

    value = value.replace(',', '.')
    value = value.split('.')
    decimals = value[-1]
    value = [v for v in value if v != decimals]
    value = ''.join(value)
    return np.float32(removeTrailingZeros(f'{value}.{decimals}'))
