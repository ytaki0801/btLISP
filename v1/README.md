# v1: extention of v0 specification

## outline of specification

### compilers

* Changed syntax and built-in words to general naming
	* `quote`, `if`, `lambda`
	* `cons`, `car`, `cdr`, `eq`, `atom`, `idx`, read

* Additional syntax
	* `nil` as empty set, integers, `lamda` with multi arguments, `list`
	* `urec`: Unique syntax by using U-combinator. See samples for details.

* `bl-comp1.bl0`: v1 compiler running on v0 interpreter or by compiler with vm
* `bl-comp1.bl1`: v1 compiler running by v1 compiler with vm only

* New built-in functions
	* `intp`, `add`, `sub`, `mul`, `div`, `quo`, `rem`, `lt`, `gt`

* New S-expression input function: comment

Note that conscells with dot notation and association list and global variables may not supported, also in future.

