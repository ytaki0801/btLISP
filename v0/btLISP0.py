from blutils0 import *
from sys import argv

#### same specification of btLISP0
def ev(s, e):
    if not isinstance(s, list):
        try: return {**e, **G}[s]
        except (KeyError, TypeError): return s
    elif s[0] == 'quote': return s[1]
    elif s[0] == 'if': return ev(s[2], e) if ev(s[1], e) else ev(s[3], e)
    elif s[0] == 'lambda': return s + [e]
    else:
        f, a = ev(s[0], e), ev(s[1], e)
        return f(a) if callable(f) else ev(f[2], {**f[3], f[1][0]: a})

sewrite(ev(seread(None if len(argv) < 2 else argv[1]), {})); print()

