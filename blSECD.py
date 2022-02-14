from sys import argv
from re import sub

def sread(file=None):
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
    return eval(sub(r'([a-zA-Z0-9\?\+\-]+)', r'"\1"', s))

def swrite(s):
    def ls(x):
        r = list(x); d = r[1:]; swrite(r[0])
        if isinstance(d, list) and d: print(' ', end=''); ls(list(d))
    if isinstance(s, str): print(s, end='')
    else:
        r = list(s)
        if not r: print('()', end='')
        else: print('(', end=''); ls(r); print(')', end='')

G = {
  'cons'  : lambda x: lambda y: [x] + y,
  'car'   : lambda x: x[0],
  'cdr'   : lambda x: x[1:],
  'eq?'   : lambda x: lambda y: x == y,
  'pair?' : lambda x: isinstance(x, list),
  'read'  : lambda x: sread(),
  'write' : lambda x: swrite(x),
  '+'     : lambda x: lambda y: str(int(x) + int(y)),
}

S, E, C, D = [], [], [], [] 

def LDV(): global S, C; i = C[0]; C = C[1:]; S += [E[int(i)][0]]
def LDF(): global S, C; f = C[0]; C = C[1:]; S += [[f, E]]
def LDC():
    global S, C
    r = C[0]; C = C[1:]
    try: S += [G[r]]
    except (KeyError, TypeError): S += [r]
def APP():
    global S, E, C, D
    f, a = S.pop(), S.pop()
    if callable(f): S += [f(a)]
    else: D += [[S, E, C]]; S = []; C = f[0]; E = [[a]] + f[1]
def RTN():
    global S, E, C, D
    r = D.pop(); S = r[0] + [S[0]]; E = r[1]; C = r[2]
def BTF():
    global S, C, D;
    t = C[0]; C = C[1:]; e = C[0]; C = C[1:]; D += [C]
    C = t if S.pop() else e
def JTF(): global C, D; C = D.pop()

OP = {'ldv': LDV, 'ldf': LDF, 'ldc': LDC, 'app': APP, 'rtn': RTN,
      'btf': BTF, 'jtf': JTF }
C = sread(None if len(argv) < 2 else argv[1])
r = C[0]; C = C[1:]
while r != 'stp': OP[r](); r = C[0]; C = C[1:]

