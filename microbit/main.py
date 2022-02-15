#
# main.py:
# This is a test version of btLISP VM on micro:bit.
# You may compile and run btLISP codes like the following:
#
# <sample files>
# bl-comp.blSECD: VM code derived from bl-comp.scm
# reverse-read-sample.scm: sample btLISP code to execute
# input.txt: S-expression input to read in the above sample btLISP code
#
# <after connecting micro:bit to your PC through USB>
# * You can get ufs by using pip.
# $ ufs put main.py
# $ ufs put bl-comp.blSECD
# $ ufs reverse-read-sample.scm
# $ ufs put input.txt
# (restart micro:bit and display the result on LED)
#

from microbit import *

# One token input function with look-ahead caching
## Due to fit for 25 times limit of recursions on micro:bit,
## there is no funcall call to get token.
sinput = ''; sipos = 0; LH = False
def get_token():
    global sipos, LH
    if not LH: sipos += 1; c = sinput[sipos - 1]
    else: lh = LH; LH = False; c = lh
    t = []
    while True:
        if c in ' \n\r\x1a':
            if not LH: sipos += 1; ct = sinput[sipos - 1]
            else: lh = LH; LH = False; ct = lh
            while ct in ' \n\r\x1a':
                if not LH: sipos += 1; ct = sinput[sipos - 1]
                else: lh = LH; LH = False; ct = lh
            LH = ct
            if not t:
                if not LH: sipos += 1; c = sinput[sipos - 1]
                else: lh = LH; LH = False; c = lh
            else: return ''.join(t)
        elif c == '(':
            if not LH: sipos += 1; ct = sinput[sipos - 1]
            else: lh = LH; LH = False; ct = lh
            while ct in ' \n\r\x1a':
                if not LH: sipos += 1; ct = sinput[sipos - 1]
                else: lh = LH; LH = False; ct = lh
            LH = ct
            return c
        elif c == ')':
            if not t: return c
            else: LH = c; return ''.join(t)
        else:
            t = t + [c]
            if not LH: sipos += 1; c = sinput[sipos - 1]
            else: lh = LH; LH = False; c = lh

# Simple S-expression parser
## Due to fit for 25 times limit of recursions on micro:bit,
## tail recursions are translated to iterations.
def slist():
    r = []
    while True:
        t = get_token()
        if   t == ')': return r
        elif t == '(': h = slist(); r += [h]
        else: r += [t]

def sread():
    t = get_token()
    return slist() if t == '(' else t

def fread(file):
    global sinput, sipos
    with open(file) as f: sinput = f.read()
    sipos = 0;
    return sread()

def sstring(s):
    def ls(x):
        r = sstring(x[0]); d = x[1:]
        while d: r += ' ' + sstring(d[0]); d = d[1:]
        return r;
    if isinstance(s, str): return s
    else: return '()' if not s else '(' + ls(s) + ')'

READFILE = '' ## to switch a file to read
G = {
  'cons'  : lambda x: lambda y: [x] + y,
  'car'   : lambda x: x[0],
  'cdr'   : lambda x: x[1:],
  'eq?'   : lambda x: lambda y: x == y,
  'pair?' : lambda x: isinstance(x, list),
  'read'  : lambda x: fread(READFILE),
  'write' : lambda x: sstring(x),
  '+'     : lambda x: lambda y: str(int(x) + int(y)),
}

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

# Firstly reverse-read-sample.scm is compiled by using VM codes of compiler.
S, E, C, D = [], [], [], []
C = fread('bl-comp.blSECD')
READFILE = 'reverse-read-sample.scm'
r = C[0]; C = C[1:]
while r != 'stp': OP[r](); r = C[0]; C = C[1:]

## Secondly generated VM codes derived from reverse-read-sample.scm is executed
## by using read with 'input.txt'
sinput = S[0]; sipos = 0;
S, E, C, D = [], [], sread(), []
READFILE = 'input.txt'
r = C[0]; C = C[1:]
while r != 'stp': OP[r](); r = C[0]; C = C[1:]

## The result is stored in the top of the S working stack
while True: display.scroll(str(S[0])); sleep(2000)

