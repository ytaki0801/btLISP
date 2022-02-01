from blutils import *
from sys import argv
from collections import deque

S, E, C, D = deque(), deque(), deque(), deque()

def P(): S.appendleft(E[C.popleft()][0])
def F(): S.appendleft(deque([C.popleft(), E]))
def V():
    t = C.popleft()
    try: S.appendleft(G[t])
    except (KeyError, TypeError): S.appendleft(t)
def A():
    global S, E, C;
    f, a = S.popleft(), S.popleft()
    if callable(f): S.appendleft(f(a))
    else:
        D.appendleft(deque([S, E, C]))
        S = deque([]); C = deque(f[0]); E = deque([[a]] + list(f[1]))
def R():
    global S, E, C;
    r = D.popleft(); S = deque([S[0]] + list(r[0])); E = r[1]; C = r[2]
def Y():
    global C;
    t, e = C.popleft(), C.popleft(); D.appendleft(C);
    if S.popleft(): C = deque(t)
    else:           C = deque(e)
def J(): global C; C = D.popleft()

OP = {'P': P, 'F': F, 'V': V, 'A': A, 'R': R, 'Y': Y, 'J': J }
C = deque(seread(None if len(argv) < 2 else argv[1]))
r = C.popleft()
while r != 'B': OP[r](); r = C.popleft()
sewrite(S.popleft()); print()

