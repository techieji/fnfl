from functools import reduce
import re

PIPE = re.compile(r'\@.*(|>[^\(\)\[\]\{\}]*)*')

s = '"test" |> &.upper() |> print(&)'

def process_expr(line):
    elems = map(str.strip, line.split('|>'))
    return reduce(lambda acc, n: n.replace('&', acc), elems)

s = '''
def fn(x):
    v = @x |> &.upper() \
           |> &.split() \
           |> print(&)  \
    return v
'''

print(re.sub(PIPE, lambda m: process_expr(m.group(0)[1:]), s))
