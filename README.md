# btLISP: a Pure LISP compiler with a SECD-style virtual machine to bootstrap

This project is aimed to define a minimum specification of a LISP self-compiler implementation and a SECD-style virtual machine for fun, education or research of [bootstrapping](https://en.wikipedia.org/wiki/Bootstrapping_(compilers)).

See the shell scripts in v0 and v1 directories for details to bootstrap. Currently the implementation language is only Python but other languages may supposed in future.

# vm

A minumum size of SECD-style virtual machine, including basic list functions and simple S-expression input and output functions to share with a bootstrap interpreter

# v0

A LISP compiler written by own language with minimum specification to bootstrap by a bootsrap interpreter and the virtual machine

# v1

Two LISP compilers with same and more syntax and functions, which are written by v0 specification and v1 specification


## License

(C) 2022 TAKIZAWA Yozo

The codes in this repository are licensed under [CC0, Creative Commons Zero v1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/)

