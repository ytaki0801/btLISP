//
// blSECD.c:
// A SECD-style Virtual Machine with Scheme-subset Built-ins
//
// (C) 2022 TAKIZAWA Yozo
// This code is licensed under CC0.
// https://creativecommons.org/publicdomain/zero/1.0/
//

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//
// Basic List Processors including Simple S-expression parser
//

// static memory allocation for conscells and symbols
typedef int32_t node_t;
#define NMAX 200000
#define CMAX 200000
#define SMAX 5000
#define SLEN 32
node_t node[NMAX]; node_t nnum = 1;
node_t cell[CMAX][2]; node_t cnum = 1;
char symb[SMAX][SLEN]; node_t snum = 1;

// each node includes positive index number for conscells
// or negative index number for symbols
node_t cons(node_t a, node_t d) {
  node_t r = nnum;
  cell[cnum][0] = a; cell[cnum][1] = d; node[nnum] = cnum;
  cnum++; nnum++; return r;
}
node_t ssym(const char *str) {
  node_t r = nnum;
  strcpy(symb[snum], str); node[nnum] = -snum;
  snum++; nnum++; return r;
}
#define gsym(s) symb[-node[s]]

// basic list processing functions
// T value is defined as !(NIL)
#define NIL 0
#define car(s)  cell[node[s]][0]
#define cdr(s)  cell[node[s]][1]
#define null(s) (s == NIL)
#define pair(s) (node[s] > 0)
#define nland(a, b) null(a) && null(b)
#define nlnor(a, b) !(null(a) || null(b)) && !(pair(a)) && !(pair(b))
#define eqsym(a, b) !(strcmp(gsym(a), gsym(b)))
#define eq(a, b) (nland(a, b) ? !(NIL) : nlnor(a, b) ? eqsym(a, b) : NIL)

// Simple S-expression output function
node_t swrite(node_t s) {
  node_t r = s;
  if (pair(s)) {
    printf("("); swrite(car(s));
    if (pair(cdr(s)))
      for (node_t n = cdr(s); n != NIL; n = cdr(n)) {
        printf(" "); swrite(car(n));
      }
    printf(")");
  } else {
    // NIL is "()" and T is not defined as a symbol
    if (null(s)) printf("()"); else printf("%s", gsym(s));
  }
  return r;
}

// One token input function with look-ahead caching
char LH = 0, lh;
char TOKEN[SLEN]; node_t tnum = 0;
#define lhset(x) LH = x
#define getc1(f, c) lh = LH; lhset(0); c = lh ? lh : getc(f)
#define spp(c) (c == 32 || 9 <= c && c <= 13)
#define elp(c) (c == 10 || c == 13)
#define smp(c) (c == ';')
#define lpp(c) (c == '(')
#define rpp(c) (c == ')')
void skipsp(FILE *f) {
  char c; getc1(f, c); while (spp(c)) { getc1(f, c); } lhset(c);
}
void skipcm(FILE *f) {
  char c; getc1(f, c); while (!elp(c)) { getc1(f, c); }
}
node_t tstr() {
  TOKEN[tnum] = NIL; node_t r = ssym(TOKEN);
  tnum = 0; return r;
}
node_t cstr(char c) {
  char s[2]; s[0] = c; s[1] = NIL; node_t r = ssym(s);
  tnum = 0; return r;
}
node_t get_token(FILE *f) {
  char c; getc1(f, c); tnum = 0;
  while (1) {
    if (smp(c)) { skipcm(f); getc1(f, c);
    } else if (spp(c)) {
      skipsp(f); if (tnum == 0) { getc1(f, c); } else return tstr();
    } else if (lpp(c)) { skipsp(f); return cstr(c);
    } else if (rpp(c)) {
      if (tnum == 0) return cstr(c); else { lhset(c); return tstr(); }
    } else { TOKEN[tnum++] = c; getc1(f, c); }
  }
}

// Simple S-expression parser
node_t slist(FILE *f) {
  node_t t = get_token(f);
  if (rpp(gsym(t)[0])) return NIL;
  else if (lpp(gsym(t)[0])) {
    node_t h = slist(f); return cons(h, slist(f)); }
  else return cons(t, slist(f));
}
node_t sread(FILE *f) {
  node_t t = get_token(f); return lpp(gsym(t)[0]) ? slist(f) : t;
}

//
// A SECD-style Virtual Machine
//

// utility functions
#define sym2int(s) (node_t)(atoi(gsym(s)))
node_t int2sym (int n) {
    char str[SLEN]; sprintf(str, "%d", n); return ssym(str);
}
node_t lref(node_t e, node_t n) {
  if (null(e)) return NIL;
  else {
    for (node_t p = sym2int(n); p > 0; p--) e = cdr(e);
    return car(e);
  }
}
node_t apd(node_t a, node_t b) {
  return null(a) ? b : cons(car(a), apd(cdr(a), b));
}
node_t add(node_t a, node_t b) {
  int a1 = sym2int(a), b1 = sym2int(b); return int2sym(a1 + b1);
}

// stack definitions
#define PUSH(s, VAL) s = cons(VAL, s)
#define POP(VAR, s)  VAR = car(s); s = cdr(s)

int main(int argc, char* argv[]) {
#ifdef MEMCHECK
  printf("allocated memory = %ld\n",
          sizeof(node) + sizeof(cell) + sizeof(symb));
  printf("node = %ld, cell = %ld, symb = %ld\n",
          sizeof(node), sizeof(cell), sizeof(symb));
#endif

  node[NIL] = NIL;
  node_t S = NIL, E = NIL, C = NIL, D = NIL;

  // read code from stdin or a file
  if (argc < 2) C = sread(stdin);
  else {
    FILE *fp;
    if ((fp = fopen(argv[1], "r")) == NULL) {
      printf("%s is not found.\n", argv[1]); return 1;
    }
    C = sread(fp); fclose(fp);
  }
#ifdef CODECHECK
swrite(C); printf("\n");
#endif
#ifdef MEMCHECK
  printf("used memory = %d\n",
         (nnum - 1) * 4 + (cnum - 1) * 4 * 2 + (snum - 1) * SLEN);
  printf("node = %d, cell = %d, symb = %d\n",
         (nnum - 1) * 4, (cnum - 1) * 4 * 2, (snum - 1) * SLEN);
  printf("nnum = %d, cnum = %d, snum = %d\n",
         (nnum - 1), (cnum - 1), (snum - 1));
#endif

  // symbols of instructions
  node_t LDV = ssym("ldv"), LDF = ssym("ldf"), LDC = ssym("ldc");
  node_t APP = ssym("app"), RTN = ssym("rtn"), BTF = ssym("btf");
  node_t JTF = ssym("jtf"), STP = ssym("stp");
  // symbols of built-in functions
  node_t CONS = ssym("cons"), CAR = ssym("car"), CDR = ssym("cdr");
  node_t EQ = ssym("eq?"), PAIR = ssym("pair?"), SR = ssym("read");
  node_t SW = ssym("write"),  ADD = ssym("+");

  // run code
  node_t r, t, f, a; POP(r, C);
  while (!eq(r, STP)) {
    if      (eq(r, LDV)) { POP(r, C); PUSH(S, car(lref(E, r))); }
    else if (eq(r, LDF)) { POP(r, C); PUSH(S, cons(r, cons(E, NIL))); }
    else if (eq(r, LDC)) { POP(r, C); PUSH(S, r); }
    else if (eq(r, BTF)) {
      POP(t, C); POP(f, C); PUSH(D, C); POP(r, S); if (r) C = t; else C = f;
    }
    else if (eq(r, JTF)) { POP(C, D); }
    else if (eq(r, APP)) {
      POP(f, S); POP(a, S);
      if (!pair(f)) {
        // exec built-in functions
        if      (eq(f, CONS)) { POP(r, S); PUSH(S, cons(a, r)); POP(t, C); }
        else if (eq(f, EQ))   { POP(r, S); PUSH(S, eq(a, r));   POP(t, C); }
        else if (eq(f, ADD))  { POP(r, S); PUSH(S, add(a, r));  POP(t, C); }
        else if (eq(f, CAR))  { PUSH(S, car(a)); }
        else if (eq(f, CDR))  { PUSH(S, cdr(a)); }
        else if (eq(f, PAIR)) { PUSH(S, pair(a)); }
        else if (eq(f, SR))   { PUSH(S, sread(stdin)); }
        else if (eq(f, SW))   { PUSH(S, swrite(a)); }
      } else {
        // call a closure
        PUSH(D, cons(S, cons(E, cons(C, NIL))));
        S = NIL; E = cons(cons(a, NIL), car(cdr(f))); C = car(f);
      }
    } else if (eq(r, RTN)) {
      POP(r, D); a = car(S); S = car(r); PUSH(S, a);
      E = car(cdr(r)); C = car(cdr(cdr(r)));
    }
    POP(r, C);
  }

#ifdef MEMCHECK
  printf("used memory = %d\n",
         (nnum - 1) * 4 + (cnum - 1) * 4 * 2 + (snum - 1) * SLEN);
  printf("node = %d, cell = %d, symb = %d\n",
         (nnum - 1) * 4, (cnum - 1) * 4 * 2, (snum - 1) * SLEN);
  printf("nnum = %d, cnum = %d, snum = %d\n",
         (nnum - 1), (cnum - 1), (snum - 1));
#endif

  return 0;
}

