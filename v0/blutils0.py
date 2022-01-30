####
#### S-expression input/output utilities
####

from re import sub
def seread(file=None):
    s = ''
    if file:
        with open(file) as cf:
            s = ''.join([x.rstrip() for x in cf.readlines()])
    else:
        try:
            l = input().rstrip()
            while True: s += l; l = input().rstrip()
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
  'cons': lambda x: lambda y: [x] + y,
  'car' : lambda x: x[0],
  'cdr' : lambda x: x[1:],
  'eq'  : lambda x: lambda y: x == y,
  'atom': lambda x: atom(x),
  'idx' : lambda x: lambda y: idx(x, y, 0),
  'read': lambda x: seread()
}

