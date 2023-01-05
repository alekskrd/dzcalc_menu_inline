from fractions import Fraction as Fr
from datetime import datetime


def calc_fraction_main(string):
    a, move, b = string.split()

    if move == '+':
        result = Fr(a) + Fr(b)
    elif move == '-':
        result = Fr(a) - Fr(b)
    elif move == '*':
        result = Fr(a) * Fr(b)
    elif move == '/':
        result = Fr(a) / Fr(b)
    else:
        return 'вы ввели некорректные данные'
    with open('log_calc.txt', 'a') as output_file:
        data = datetime.now().strftime('%Y.%m.%d %H:%M:%S  ')
        output_file.writelines(f'{data} {a} {move} {b} = {result}\n')
    return f'Результат равен {result}'
