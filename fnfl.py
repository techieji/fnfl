from functools import reduce
import re
from random import randint

PIPE = re.compile(r'\@.*(|>[^\(\)\[\]\{\}]*)*')
OPERATOR = re.compile(r'@\(.*\)')

# Features:
# PIPE:     @x |> y
# LAMBDA:   _ + 2
# OPERATOR: @(+)

def process_pipe(line):
    elems = map(str.strip, line.split('|>'))
    return reduce(lambda acc, n: n.replace('&', acc), elems)

def process_operator(_op):
    op = _op[2:-1]
    return f"(lambda l, r='': eval('{{l}}{op}{{r}}'.format(l=l, r=r)))"

s = ''

def repeat_sub(regex, fn):
    def f(s):
        n = 1
        while n != 0:
            s, n = re.subn(regex, lambda m: fn(m.group(0)), s)
            return s
    return f

pipefy = repeat_sub(PIPE, process_pipe)
operatorify = repeat_sub(OPERATOR, process_operator)

print(operatorify('@(.access)'))
