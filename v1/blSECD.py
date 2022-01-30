from blutils import *
from sys import argv
from collections import deque

S, E, C, D = deque(), deque(), deque(), deque()

def LD(): S.appendleft(E[C.popleft()][0])
def LF(): S.appendleft(deque([C.popleft(), E]))
def LV():
    t = C.popleft()
    try: S.appendleft(G[t])
    except (KeyError, TypeError): S.appendleft(t)
def AP():
    global S, E, C;
    f, a = S.popleft(), S.popleft()
    if callable(f): S.appendleft(f(a))
    else:
        D.appendleft(deque([S, E, C]))
        S = deque([]); C = deque(f[0]); E = deque([[a]] + list(f[1]))
def RT():
    global S, E, C;
    r = D.popleft(); S = deque([S[0]] + list(r[0])); E = r[1]; C = r[2]
def SL():
    global C;
    t, e = C.popleft(), C.popleft(); D.appendleft(C);
    if S.popleft(): C = deque(t)
    else:           C = deque(e)
def JI(): global C; C = D.popleft()

OP = { 'LD': LD, 'LF': LF, 'LV': LV, 'AP': AP, 'RT': RT, 'SL': SL, 'JI': JI }
C = deque(seread(None if len(argv) < 2 else argv[1]))
r = C.popleft()
while r != 'ST': OP[r](); r = C.popleft()
sewrite(S.popleft()); print()

