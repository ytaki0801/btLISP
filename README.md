# btLISP: a Pure LISP Self-Compiler with a SECD-style Virtual Machine

This project is aimed to define a minimum specification of a LISP self-compiler implementation and a SECD-style virtual machine for fun, education or research of [bootstrapping](https://en.wikipedia.org/wiki/Bootstrapping_(compilers)).

See the shell scripts for details to bootstrap. Currently Scheme implementation is just supposed to bootstrap because the compiler is written in btLISP itself as a Scheme-subset, but other languages may be supposed to bootstrap btLISP in future. And VM implementation languages are now C and Python only but Scheme may be supposed.

## `bt-comp.scm`: btLISP compiler in btLISP for `blSECD`

The compiler is written in the following syntax in Scheme subset except built-in functions in the VM, called `blSECD`.

* `lambda` with Lisp-1 and lexical scope
* `if`, `quote`

You can bootstrap to self-compile by using any Scheme subset implementations, including [playgrounds on the Web](https://www.tutorialspoint.com/execute_scheme_online.php), like the following. Once you get VM codes derived from `bt-comp.scm`, you do not need a Scheme implementation but a VM only to compile btLISP codes.

```
$ scm bl-comp.scm < bl-comp.scm > bl-comp.blSECD

$ python3 blSECD.py bl-comp.blSECD | python3 blSECD.py
(write ((lambda (x y) (cons x (cdr y))) (quote a) (quote (x y z))))
[Ctrl-D](a y z)

$ cc -o blSECD blSECD.c
$ ./blSECD bl-comp.blSECD | ./blSECD
(write ((lambda (x y) (cons x (cdr y))) (quote a) (quote (x y z))))
(a y z)

$ python3 blSECD.py bl-comp.blSECD < bl-comp.scm > out.blSECD
$ python3 blSECD.py out.blSECD | ./blSECD
(write ((lambda (x y) (cons x (cdr y))) (quote a) (quote (x y z))))
[Ctrl-D](a y z)
$ ./blSECD out.blSECD < bl-comp.scm > out2.blSECD
$ ./blSECD out2.blSECD | python3 blSECD.py
(write ((lambda (x y) (cons x (cdr y))) (quote a) (quote (x y z))))
(a y z)
```

I do not put VM codes derived from `bt-comp.scm` on purpose. Enjoy to bootstrap!

## `blSECD.py`,`blSECD.c`: A SECD-style Virtual Machine implementation

The specification of the VM is a SECD-style but customized to btLISP minimum Scheme-subset as possible.

### Sample Codes

```
(ldc () ldc read app ldc cdr app ldc write app stp)
= (write (cdr (read (current-input-port))))
=> [input](a b c) => [output](b c)

(ldc (x y z) ldc a ldf (ldf (ldv 0 ldc cdr app ldv 1 ldc cons app app rtn) rtn) app app ldc write app stp)
= (write
    ((lambda (x y) (cons x (cdr y)))
     (quote a) (quote (x y z))))
=> [output](a y z)
```

### Instructions

|Stacks|Description|
|:---:|:---:|:---:|
|`S`|stack to work|
|`E`|env to keep closure values|
|`C`|VM codes|
|`D`|stack to dump to recur or branch|

* `ldv`: pop a closure value specified by a C code from E and push it to S
* `ldf`: pop a closure from C and push it with the current E to S
* `ldc`: load a constant value or a built-in function and push it to S
* `app`: pop a function with a value from S to apply
	* if the function is a built-in function:
		* apply and push the result to S
	* if the function is a closure:
		* dump (S E C) to D
		* clear S
		* set the closure body to C
		* set the pair of the value and the closure variable to E
* `rtn`: pop (S E C) from D and set it to the each one to return
	* push the result value in the top of the current S to poped S
* `btf`: pop true and false codes from C to branch
	* dump the current C to D
	* pop a conditional value from C and set the true or false code to C
* `jtf`: pop C from D and push it to C to join
* `stp`: stop vm

Note that closures in the VM are supposed to have just one argument only so you must curry to write lamda expressions with multiple arguments.

### Built-in functions

* `cons`, `car`, `cdr`, `eq?`, `pair?` as Pure-oriented list processing
* `read` with `current-input-port` as standard input port
* `write`, `+` needed to self-compile

Note that the above functions are curried, same as closures in VM, so you must call twice if the function needs two values.

### Other features in VM

* comments between ";" and end of the line
* NO `#t` NOR `#f` as boolean values
* NO dot notation NOR single quotation as quote
* NO global environment

## License

(C) 2022 TAKIZAWA Yozo

The codes in this repository are licensed under [CC0, Creative Commons Zero v1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/)

