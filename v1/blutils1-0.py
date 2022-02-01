####
#### S-expression input/output utilities
####

from re import sub
def seread(file=None):
    def ccut(s): i = s.find(';'); return s if i < 0 else s[:i]
    s = ''
    if file:
        with open(file) as cf:
            s = ''.join([ccut(x.rstrip()) for x in cf.readlines()])
    else:
        try:
            l = ccut(input().rstrip());
            while True: s += l; l = ccut(input().rstrip());
        except EOFError: pass
    s = sub(r'\s+', ',', s).replace('(', '[').replace(')', ']')
    return eval(sub(r'([a-zA-Z]+)', r'"\1"', s))

def sewrite(s):
    def ls(x):
        r = list(x); d = r[1:]; sewrite(r[0])
        if not atom(d) and d: print(' ', end=''); ls(list(d))
    if atom(s): print(s, end='')
    else:
        r = list(s)
        if not r: print('()', end='')
        else: print('(', end=''); ls(r); print(')', end='')

####
#### basic functions in btLISP
####

def idx(e, ls, r):
    return [] if not ls else (r if e == ls[0] else idx(e, ls[1:], r+1))

def atom(x):
    return not isinstance(x, list) or x == None or isinstance(x, bool)

G = {
  'C': lambda x: lambda y: [x] + y,
  'H': lambda x: x[0],
  'T': lambda x: x[1:],
  'E': lambda x: lambda y: x == y,
  'A': lambda x: atom(x),
  'I': lambda x: lambda y: idx(x, y, 0),
  'R': lambda x: seread(),
  'cons': lambda x: lambda y: [x] + y,
  'car' : lambda x: x[0],
  'cdr' : lambda x: x[1:],
  'eq'  : lambda x: lambda y: x == y,
  'atom': lambda x: atom(x),
  'idx' : lambda x: lambda y: idx(x, y, 0),
  'read': lambda x: seread(),
  'intp': lambda x: isinstance(x, int),
  'add' : lambda x: lambda y: x + y,
  'sub' : lambda x: lambda y: x - y,
  'mul' : lambda x: lambda y: x * y,
  'div' : lambda x: lambda y: x // y,
  'rem' : lambda x: lambda y: x % y,
  'lt'  : lambda x: lambda y: x < y,
  'gt'  : lambda x: lambda y: x > y
}

