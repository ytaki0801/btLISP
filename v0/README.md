# v0: bootstrap specification

## outline of specification

### interpreter and compiler

* `Q`: `quote`
* `Y`: `if`
* `L`: `lambda` with lexical-scope and just one argument only

### built-in functions

`C`: `cons`
`H`: `car`
`T`: `cdr`
`E`: `eq`
`A`: `atom`
`I`: `idx` to treat positions of closure values in vm
`R`: `read` to input S-expression

Note that the above built-in functions are also curryed same as closures.

